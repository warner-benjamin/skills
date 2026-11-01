"""Disposable Codex server and fake inference shared by the opt-in probes."""
import http.server
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from types import SimpleNamespace
import uuid

SCRIPT_DIR = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))
from quiet_polling import CodexRPC, codex_executable


def until(predicate, timeout=12):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        time.sleep(.03)
    raise TimeoutError('probe deadline expired')


class Provider(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def read_request(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        meta = json.loads(self.headers['x-codex-turn-metadata'])
        thread = meta['thread_id']
        with self.server.lock:
            self.server.requests.append({'time': time.monotonic(), 'body': body, 'metadata': meta})
            count = self.server.counts.get(thread, 0) + 1
            self.server.counts[thread] = count
        return body, meta, count

    def reply(self, item):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        response = {'id': 'resp_' + uuid.uuid4().hex, 'object': 'response', 'status': 'in_progress', 'output': []}
        events = [{'type': 'response.created', 'response': response},
                  {'type': 'response.output_item.added', 'output_index': 0, 'item': item},
                  {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
                  {'type': 'response.completed', 'response': {**response, 'status': 'completed', 'output': [item],
                   'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}}]
        try:
            for event in events:
                self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass


def processes(state, worker):
    if os.name == 'nt':
        output = subprocess.check_output(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
            '[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); '
            'Get-CimInstance Win32_Process | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress'],
            encoding='utf-8')
        rows = json.loads(output) or []
        if isinstance(rows, dict):
            rows = [rows]
        return [row['ProcessId'] for row in rows
                if str(SCRIPT_DIR / 'quiet_polling.py').lower() in (row['CommandLine'] or '').lower()
                and str(state).lower() in (row['CommandLine'] or '').lower()
                and ('--worker' in (row['CommandLine'] or '')) == worker]
    found = []
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit():
            continue
        try:
            cmd = (proc / 'cmdline').read_bytes().decode().split('\0')
            if (str(SCRIPT_DIR / 'quiet_polling.py') in cmd and str(state) in cmd
                    and ('--worker' in cmd) == worker):
                found.append(int(proc.name))
        except (OSError, UnicodeError):
            pass
    return found


def run_probe(provider, cases, prefix):
    os.umask(0o077)
    root = Path(tempfile.mkdtemp(prefix=prefix))
    home = root / 'home'; home.mkdir()
    state = root / 'state'; socket = root / 'control/server.sock'
    fixture = http.server.ThreadingHTTPServer(('127.0.0.1', 0), provider)
    (home / 'config.toml').write_text(
        'model_provider="probe"\n[model_providers.probe]\nname="fixture"\n'
        f'base_url="http://127.0.0.1:{fixture.server_port}/v1"\n'
        'wire_api="responses"\nsupports_websockets=false\n'
        '[features]\napps=false\nhooks=false\ngoals=true\n')
    fixture.daemon_threads = True; fixture.requests = []; fixture.counts = {}; fixture.lock = threading.Lock()
    fixture.gate_next = False
    fixture.entered = threading.Event(); fixture.release = threading.Event()
    fixture.goal_entered = threading.Event(); fixture.goal_release = threading.Event()
    threading.Thread(target=fixture.serve_forever, daemon=True).start()
    report = {'root': str(root), 'scope': 'disposable app-server and fake localhost inference; seconds-scale', 'cases': {}}
    threads = []; rpc = process = None
    with (root / 'server.stdout').open('w') as stdout, (root / 'server.stderr').open('w') as stderr:
        try:
            report['version'] = subprocess.check_output([codex_executable(), '--version'], text=True).strip()
            env = {k: v for k, v in os.environ.items() if not k.startswith(('CODEX_', 'OPENAI_'))}
            env['CODEX_HOME'] = str(home)
            process = subprocess.Popen([codex_executable(), 'app-server', '--listen', 'unix://' + str(socket)], cwd=root,
                                       env=env, stdout=stdout, stderr=stderr, start_new_session=os.name != 'nt')
            until(socket.exists)
            rpc = CodexRPC(str(socket))
            config = {'features.goals': True, 'features.apps': False, 'features.hooks': False, 'web_search': 'disabled',
                      'mcp_servers.quiet_polling': {'command': sys.executable,
                          'args': [str(SCRIPT_DIR / 'quiet_polling.py'), '--state-dir', str(state), '--socket', str(socket)],
                          'tool_timeout_sec': 20, 'default_tools_approval_mode': 'approve'}}

            def record_for(thread):
                for file in state.glob('*.json'):
                    record = json.loads(file.read_text())
                    if record['thread_id'] == thread:
                        return record

            def finished(thread, turn):
                page = rpc.call('thread/turns/list', {'threadId': thread, 'limit': 100, 'sortDirection': 'desc'})
                return next((v for v in page['data'] if v['id'] == turn and v['status'] != 'inProgress'), None)

            cases(SimpleNamespace(root=root, state=state, fixture=fixture, rpc=rpc, config=config,
                                  report=report, threads=threads, record_for=record_for, finished=finished))
            report['success'] = True
        except Exception as error:
            report['error'] = repr(error); report['traceback'] = traceback.format_exc()
        finally:
            fixture.release.set(); fixture.goal_release.set()
            # Workers detach from the app-server's process group. Match only this probe's state path.
            for pid in processes(state, worker=True):
                try:
                    os.kill(pid, signal.SIGTERM)
                    until(lambda: pid not in processes(state, worker=True), 5)
                except (FileNotFoundError, ProcessLookupError):
                    pass
                except Exception as error:
                    report.setdefault('cleanup_errors', []).append(repr(error))
            if rpc:
                for thread in threads:
                    try:
                        rpc.call('thread/goal/clear', {'threadId': thread, 'origin': 'automatic'})
                        rpc.call('thread/archive', {'threadId': thread})
                    except Exception as error:
                        report.setdefault('cleanup_errors', []).append(repr(error))
                rpc.close()
            if process and process.poll() is None:
                if os.name == 'nt':
                    subprocess.run(['taskkill.exe', '/PID', str(process.pid), '/T', '/F'],
                                   check=True, stdout=subprocess.DEVNULL)
                else:
                    os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill() if os.name == 'nt' else os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
            fixture.shutdown(); fixture.server_close()
    (root / 'provider.json').write_text(json.dumps(fixture.requests, indent=2) + '\n')
    (root / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'root': str(root), 'success': report.get('success', False), 'error': report.get('error')}), flush=True)
    return 0 if report.get('success') and not report.get('cleanup_errors') else 1
