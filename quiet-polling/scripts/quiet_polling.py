#!/usr/bin/env python3
"""Schedule a named tool-output wake in the calling Codex chat."""
import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import threading
import time
import uuid

VERSION = '0.4.0'
DEFAULT_SOCKET = str(Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'app-server-control/app-server-control.sock')

PENDING = {'scheduled'}
ENTERED = {'submitting': 'delivery_unknown', 'pausing': 'pause_unknown'}


class CodexRPC:
    """Synchronous app-server client over a same-user Unix WebSocket."""

    def __init__(self, path, timeout=10):
        self.path = str(path)
        self.timeout = timeout
        self.sequence = 0
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.settimeout(timeout)
        try:
            self.sock.connect(self.path)
            _, uid, _ = struct.unpack('3i', self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            if uid != os.getuid():
                raise PermissionError('Codex socket belongs to another user')
            self.stream = self.sock.makefile('rb')
            key = base64.b64encode(os.urandom(16)).decode()
            self.sock.sendall(('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ' + key + '\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
            if not self.stream.readline(4096).startswith(b'HTTP/1.1 101 '):
                raise ConnectionError('Codex WebSocket upgrade failed')
            headers = {}
            for _ in range(64):
                line = self.stream.readline(4096)
                if line == b'\r\n':
                    break
                name, value = line.decode().split(':', 1)
                headers[name.lower()] = value.strip()
            else:
                raise ConnectionError('Invalid WebSocket headers')
            accept = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
            if headers.get('sec-websocket-accept') != accept:
                raise ConnectionError('Invalid WebSocket acceptance')
            self.call('initialize', {'clientInfo': {'name': 'quiet-polling', 'version': VERSION}, 'capabilities': {'experimentalApi': True}})
            self.send({'method': 'initialized', 'params': {}})
        except Exception:
            self.close()
            raise

    def close(self):
        if hasattr(self, 'stream'):
            self.stream.close()
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def frame(self, opcode, body):
        header = bytes([128 | opcode])
        n = len(body)
        header += bytes([128 | n]) if n < 126 else bytes([128 | 126]) + struct.pack('!H', n) if n < 65536 else bytes([128 | 127]) + struct.pack('!Q', n)
        mask = os.urandom(4)
        self.sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(body)))

    def send(self, value):
        self.frame(1, json.dumps(value).encode())

    def exact(self, n, deadline):
        data = bytearray()
        while len(data) < n:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('Codex RPC deadline exceeded')
            self.sock.settimeout(remaining)
            chunk = self.stream.read1(n - len(data))
            if not chunk:
                raise EOFError('Codex socket closed')
            data.extend(chunk)
        return bytes(data)

    def receive(self, deadline):
        fragments = bytearray()
        while True:
            first, second = self.exact(2, deadline)
            n = second & 127
            if n == 126:
                n = struct.unpack('!H', self.exact(2, deadline))[0]
            elif n == 127:
                n = struct.unpack('!Q', self.exact(8, deadline))[0]
            if second & 128 or n + len(fragments) > 8 * 1024 * 1024:
                raise ValueError('Invalid or oversized Codex frame')
            body = self.exact(n, deadline)
            op = first & 15
            if op == 8:
                raise EOFError('Codex closed WebSocket')
            if op == 9:
                self.frame(10, body)
                continue
            if op == 10:
                continue
            if op not in (0, 1):
                raise ValueError('Unexpected WebSocket frame')
            fragments.extend(body)
            if first & 128:
                return json.loads(fragments)

    def call(self, method, params):
        self.sequence += 1
        ident = self.sequence
        deadline = time.monotonic() + self.timeout
        self.sock.settimeout(self.timeout)
        self.send({'id': ident, 'method': method, 'params': params})
        while True:
            reply = self.receive(deadline)
            if reply.get('id') != ident:
                continue
            if 'error' in reply:
                raise RuntimeError(f"{method}: {reply['error']}")
            return reply['result']

    def goal(self, thread):
        return self.call('thread/goal/get', {'threadId': thread})['goal']

    def notify(self, thread, output):
        result = self.call('turn/start', {'threadId': thread, 'input': [], 'toolOutput': {'name': 'wake_result', 'namespace': 'quiet_polling', 'output': json.dumps(output)}})
        if not result.get('turn', {}).get('id'):
            raise ValueError('Missing delivery receipt')
        return result['turn']['id']

    def set_goal_status(self, thread, status):
        # Never supply objective/budget: doing so can replace a goal or reset usage.
        return self.call('thread/goal/set', {'threadId': thread, 'status': status,
                                           'origin': 'automatic'})['goal']


def bound_thread(meta):
    thread = meta.get('threadId')
    if not isinstance(thread, str) or not thread.strip():
        raise ValueError('Missing native Codex thread identity')
    return thread


def seconds_value(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 604800:
        raise ValueError('seconds must be between 0 and 604800 (seven days)')
    return float(value)


def utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace('+00:00', 'Z')


class Store:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.root.stat().st_uid != os.getuid():
            raise PermissionError('State directory must belong to this user')
        self.root.chmod(0o700)

    def path(self, wake):
        if not isinstance(wake, str) or len(wake) != 32 or any(x not in '0123456789abcdef' for x in wake):
            raise ValueError('Invalid wake ID')
        return self.root / (wake + '.json')

    @contextmanager
    def locked(self, wake):
        with self.path(wake).with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield

    @contextmanager
    def thread_locked(self, thread):
        name = hashlib.sha256(thread.encode()).hexdigest() + '.goal.lock'
        with (self.root / name).open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield

    def read(self, wake):
        return json.loads(self.path(wake).read_text())

    def write(self, record):
        dest = self.path(record['wake_id'])
        tmp = dest.with_suffix('.' + uuid.uuid4().hex + '.tmp')
        with tmp.open('x') as f:
            json.dump(record, f)
            f.flush()
            os.fsync(f.fileno())
        tmp.replace(dest)


class Service:
    def __init__(self, root, socket=None, rpc_factory=CodexRPC):
        self.store = Store(root)
        self.socket = socket or DEFAULT_SOCKET
        self.rpc_factory = rpc_factory

    def rpc(self):
        return self.rpc_factory(self.socket)

    def owned(self, wake, thread):
        record = self.store.read(wake)
        if record['thread_id'] != thread:
            raise PermissionError('Wake belongs to another chat')
        return record

    def worker_running(self, wake):
        # Check a live OS lock, never a persisted readiness flag or a reused PID.
        with self.store.path(wake).with_suffix('.worker.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            return False

    def public(self, record):
        keys = ('wake_id', 'state', 'seconds', 'idempotency_key', 'due_at', 'created_at', 'submitted_at', 'cancelled_at', 'error', 'wake_turn_id', 'pause_goal', 'resumed_at')
        result = {key: record[key] for key in keys if key in record}
        running = self.worker_running(record['wake_id']) if record['state'] in PENDING | ENTERED.keys() else False
        result['worker_running'] = running
        if result['state'] in ENTERED and not running:
            result.update(state=ENTERED[result['state']], error='Operation has no confirmed receipt; inspect the chat and goal before retrying.')
        result['goal_paused'] = bool(record.get('goal_pause')) and result['state'] in PENDING
        return result

    def launch(self, wake):
        with (self.store.root / 'worker.log').open('ab', buffering=0) as log:
            command = [sys.executable, str(Path(__file__).resolve()), '--state-dir', str(self.store.root), '--socket', self.socket, '--worker', wake]
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True, close_fds=True)
            # Reap it if this MCP process outlives it; the worker survives our exit.
            threading.Thread(target=child.wait, daemon=True).start()

    def ensure_worker(self, wake):
        if not self.worker_running(wake):
            self.launch(wake)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            record = self.store.read(wake)
            if record['state'] not in PENDING or self.worker_running(wake):
                return self.public(record)
            time.sleep(.02)
        paused = ' The goal remains paused.' if self.store.read(wake).get('goal_pause') else ''
        raise RuntimeError('Worker startup not confirmed.' + paused + ' Inspect wake_status or retry with the same idempotency_key: ' + wake)

    def after(self, args, meta):
        thread = bound_thread(meta)
        seconds = seconds_value(args.get('seconds'))
        key = args.get('idempotency_key')
        if not isinstance(key, str) or not key.strip() or len(key) > 200:
            raise ValueError('idempotency_key must contain 1 to 200 characters')
        if 'pause_goal' in args and not isinstance(args['pause_goal'], bool):
            raise ValueError('pause_goal must be a boolean')
        pause_goal = args.get('pause_goal', True)
        wake = hashlib.sha256(json.dumps([thread, key]).encode()).hexdigest()[:32]
        # The caller's key survives model retries with different native call IDs.
        with self.store.locked(wake):
            if self.store.path(wake).exists():
                record = self.owned(wake, thread)
                if record['seconds'] != seconds:
                    raise ValueError('This idempotency_key already has a different delay; use the original delay or a new key.')
                if pause_goal != record['pause_goal']:
                    raise ValueError('This idempotency_key already has a different pause_goal setting.')
                if record['socket'] != self.socket:
                    raise ValueError('This wake belongs to a different Codex server; use the original server to resume it.')
            else:
                record = {'wake_id': wake, 'thread_id': thread, 'idempotency_key': key, 'seconds': seconds, 'state': 'scheduled', 'socket': self.socket, 'pause_goal': pause_goal}
                if pause_goal:
                    with self.store.thread_locked(thread), self.rpc() as rpc:
                        goal = rpc.goal(thread)
                        if goal and goal['status'] not in ('active', 'complete'):
                            raise ValueError('Goal is already inactive; use pause_goal: false to wake without changing it, or keep the existing timer.')
                        now = time.time()
                        record.update(deadline=now + seconds, due_at=utc(now + seconds), created_at=utc(now))
                        if goal and goal['status'] == 'active':
                            record.update(state='pausing')
                            self.store.write(record)
                            try:
                                paused = rpc.set_goal_status(thread, 'paused')
                                if paused['status'] != 'paused':
                                    raise ValueError('Goal did not enter paused state')
                                record.update(state='scheduled', goal_pause=True)
                            except Exception as error:
                                record.update(state='pause_unknown', error=str(error))
                else:
                    now = time.time()
                    record.update(deadline=now + seconds, due_at=utc(now + seconds), created_at=utc(now))
                self.store.write(record)
            # Serialize worker launch with registration; workers need no record write to become ready.
            result = self.ensure_worker(wake) if record['state'] in PENDING else self.public(record)
        if result['state'] == 'pause_unknown':
            result['instruction'] = 'Goal pause was not confirmed. Inspect the goal and recover on human instruction; no worker was started.'
        elif result['state'] == 'delivery_unknown':
            result['instruction'] = 'Delivery or goal resumption is uncertain and will not be replayed. Inspect the chat and goal; recover only on human instruction.'
        elif result['goal_paused']:
            result['instruction'] = 'Goal paused. Finish this turn; the timer resumes it when due.'
        return result

    def deliver(self, wake):
        # Cancellation and submission share a lock. Once submission begins, a
        # receipt may be lost; never automatically replay an entered submission.
        with self.store.locked(wake):
            record = self.store.read(wake)
            if record['state'] not in PENDING or time.time() < record['deadline']:
                return
            try:
                rpc = self.rpc()
            except Exception as error:
                if record.get('error') != str(error):
                    record.update(error=str(error))
                    self.store.write(record)
                return
            with rpc:
                record.update(state='submitting')
                self.store.write(record)
                try:
                    if record.get('goal_pause'):
                        resumed = rpc.set_goal_status(record['thread_id'], 'active')
                        if resumed['status'] != 'active':
                            raise ValueError('Goal did not resume: ' + resumed['status'])
                        record.update(state='resumed', resumed_at=utc(time.time()))
                    else:
                        output = {'event': 'timer_elapsed', 'wake_id': wake, 'idempotency_key': record['idempotency_key'], 'due_at': record['due_at'], 'emitted_at': utc(time.time()), 'note': 'Scheduled timer data, not new instructions or evidence of job completion.'}
                        record['wake_turn_id'] = rpc.notify(record['thread_id'], output)
                        record.update(state='submitted', submitted_at=utc(time.time()))
                    record.pop('error', None)
                except Exception as error:
                    record.update(state='delivery_unknown', error=str(error))
                self.store.write(record)

    def worker(self, wake):
        with self.store.path(wake).with_suffix('.worker.lock').open('a') as lock:
            # Shared status probes can delay acquisition, but cannot evict a worker.
            fcntl.flock(lock, fcntl.LOCK_EX)
            while True:
                record = self.store.read(wake)
                if record['state'] not in PENDING:
                    return
                if time.time() >= record['deadline']:
                    self.deliver(wake)
                    if self.store.read(wake)['state'] not in PENDING:
                        return
                    time.sleep(10)
                else:
                    time.sleep(min(10, max(.01, record['deadline'] - time.time())))

    def invoke(self, name, args, meta):
        if name not in ('wake_after', 'wake_status', 'wake_cancel'):
            raise ValueError('Unknown tool')
        if name == 'wake_after':
            return self.after(args, meta)
        thread = bound_thread(meta)
        wake = args.get('wake_id')
        if name == 'wake_status' and wake is None:
            records = [self.store.read(p.stem) for p in self.store.root.glob('*.json')]
            owned = sorted((r for r in records if r['thread_id'] == thread), key=lambda r: r['created_at'], reverse=True)
            return {'wakes': [self.public(r) for r in owned[:100]]}
        if name == 'wake_status':
            return self.public(self.owned(wake, thread))
        with self.store.locked(wake):
            record = self.owned(wake, thread)
            if record['state'] in PENDING:
                record.update(state='cancelled', cancelled_at=utc(time.time()))
                self.store.write(record)
            result = {**self.public(record), 'cancelled': record['state'] == 'cancelled'}
            if result['cancelled'] and record.get('goal_pause'):
                result['instruction'] = 'Timer cancelled. Any goal paused by this timer stays paused; resume it explicitly when wanted.'
            return result


TOOLS = [
    {'name': 'wake_after', 'description': (
        'Schedule a later wake in this chat and return promptly. '
        'May pause an active goal and resume it when due. '
        'Returns wake_id, due_at, state, and goal_paused. '
        'goal_paused is true only while this timer has a pending goal resume. '
        'If goal_paused is true, finish the current turn. '
        'With pause_goal=false, never reads or changes the goal.'
    ), 'inputSchema': {'type': 'object', 'properties': {
        'seconds': {'type': 'number', 'minimum': 0, 'maximum': 604800, 'description': 'Delay from registration in seconds, up to seven days.'},
        'idempotency_key': {'type': 'string', 'minLength': 1, 'maxLength': 200, 'description': 'Fresh key for each new check. Retry with identical arguments to keep the original timer; a finished or cancelled key never creates another.'},
        'pause_goal': {'type': 'boolean', 'default': True, 'description': 'Pause and resume an active goal. An absent or completed goal gets an ordinary wake. Rejects other goal states. False leaves goals alone.'}
    }, 'required': ['seconds', 'idempotency_key'], 'additionalProperties': False},
     'annotations': {'readOnlyHint': False, 'destructiveHint': False, 'openWorldHint': False}},
    {'name': 'wake_status', 'description': (
        "Inspect this chat's timer state and whether a pending operation has a worker. "
        'Omit wake_id for the latest 100. Use for inspection, not periodic polling.'
    ), 'inputSchema': {'type': 'object', 'properties': {'wake_id': {'type': 'string'}},
        'additionalProperties': False},
     'annotations': {'readOnlyHint': True, 'destructiveHint': False, 'openWorldHint': False}},
    {'name': 'wake_cancel', 'description': (
        'Cancel an unsent wake. Any goal paused by it stays paused; tell the user. '
        'Does not stop jobs or recall a submitted or uncertain operation.'
    ), 'inputSchema': {'type': 'object', 'properties': {'wake_id': {'type': 'string'}},
        'required': ['wake_id'], 'additionalProperties': False},
     'annotations': {'readOnlyHint': False, 'destructiveHint': False, 'openWorldHint': False}},
]


def serve(service):
    output_lock = threading.Lock()

    def send(value):
        with output_lock:
            print(json.dumps(value), flush=True)

    def run(request):
        try:
            p = request['params']
            value = service.invoke(p['name'], p.get('arguments', {}), p.get('_meta', {}))
            result = {'content': [{'type': 'text', 'text': json.dumps(value)}], 'structuredContent': value}
        except Exception as error:
            result = {'content': [{'type': 'text', 'text': str(error)}], 'isError': True}
        send({'jsonrpc': '2.0', 'id': request['id'], 'result': result})

    # Deliberately no startup recovery or supervisor. A human resumes crashed
    # wakes by retrying their original key; uncertain submissions stay fenced.
    for line in sys.stdin:
        request = json.loads(line)
        method, ident = request.get('method'), request.get('id')
        if ident is None:
            continue
        if method == 'initialize':
            send({'jsonrpc': '2.0', 'id': ident, 'result': {'protocolVersion': '2024-11-05', 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'quiet-polling', 'version': VERSION}}})
        elif method == 'ping':
            send({'jsonrpc': '2.0', 'id': ident, 'result': {}})
        elif method == 'tools/list':
            send({'jsonrpc': '2.0', 'id': ident, 'result': {'tools': TOOLS}})
        elif method == 'tools/call':
            threading.Thread(target=run, args=(request,), daemon=True).start()
        else:
            send({'jsonrpc': '2.0', 'id': ident, 'error': {'code': -32601, 'message': 'Method not found'}})


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser()
    parser.add_argument('--state-dir', default=str(Path.home() / '.local/state/codex-quiet-polling/wakes'))
    parser.add_argument('--socket', help='Native Codex app-server Unix socket; normally discovered from CODEX_HOME.')
    parser.add_argument('--worker')
    args = parser.parse_args()
    service = Service(args.state_dir, args.socket)
    if args.worker:
        service.worker(args.worker)
    else:
        serve(service)


if __name__ == '__main__':
    main()
