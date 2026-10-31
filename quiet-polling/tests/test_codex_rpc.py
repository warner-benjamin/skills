import json
from pathlib import Path
import socket
import sys
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from quiet_polling import CodexRPC


class TransportTests(unittest.TestCase):
    def setUp(self):
        client, self.peer = socket.socketpair()
        self.rpc = CodexRPC.__new__(CodexRPC)
        self.rpc.sock = client
        self.rpc.stream = client.makefile('rb')
        self.rpc.sequence = 0
        self.rpc.timeout = .1

    def tearDown(self):
        self.rpc.close()
        self.peer.close()

    def test_fragmented_response_with_ping(self):
        body = json.dumps({'id': 1, 'result': {'ok': True}}).encode()
        self.peer.sendall(bytes([1, 5]) + body[:5] + b'\x89\x01p'
                          + bytes([128, len(body) - 5]) + body[5:])
        self.assertEqual(self.rpc.call('probe', {}), {'ok': True})

    def test_received_reply_survives_delay_after_decoding(self):
        body = json.dumps({'id': 1, 'result': {'accepted': True}}).encode()
        self.peer.sendall(bytes([129, len(body)]) + body)
        loads = json.loads
        with patch('quiet_polling.time.monotonic', return_value=0) as clock:
            def decode_then_deschedule(data):
                reply = loads(data)
                clock.return_value = self.rpc.timeout + 1
                return reply
            with patch('quiet_polling.json.loads', side_effect=decode_then_deschedule):
                self.assertEqual(self.rpc.call('probe', {}), {'accepted': True})

    def test_partial_progress_does_not_extend_deadline(self):
        body = json.dumps({'id': 1, 'result': {'ok': True}}).encode()
        stop = threading.Event()

        def send_slowly():
            self.peer.sendall(bytes([129, len(body)]))
            for byte in body:
                if stop.wait(.02):
                    return
                self.peer.sendall(bytes([byte]))

        sender = threading.Thread(target=send_slowly)
        sender.start()
        try:
            with self.assertRaises(TimeoutError):
                self.rpc.call('probe', {})
        finally:
            stop.set()
            sender.join(2)


class WireTests(unittest.TestCase):
    def test_native_notification_uses_named_tool_output(self):
        rpc = CodexRPC.__new__(CodexRPC)
        calls = []
        def call(method, params):
            calls.append((method, params))
            return {'turn': {'id': 'turn', 'status': 'inProgress'}}
        rpc.call = call
        self.assertEqual(rpc.notify('t', {'event': 'timer_elapsed'}), 'turn')
        method, params = calls[0]
        self.assertEqual(method, 'turn/start')
        self.assertEqual(params['input'], [])
        self.assertEqual(params['toolOutput']['name'], 'wake_result')
        self.assertEqual(json.loads(params['toolOutput']['output'])['event'], 'timer_elapsed')

    def test_goal_mutation_preserves_objective_and_budget_parameters(self):
        rpc = CodexRPC.__new__(CodexRPC)
        calls = []
        rpc.call = lambda method, params: calls.append((method, params)) or {'goal': {'status': params['status']}}
        self.assertEqual(rpc.set_goal_status('t', 'active')['status'], 'active')
        self.assertEqual(calls, [('thread/goal/set', {'threadId': 't', 'status': 'active', 'origin': 'automatic'})])


if __name__ == '__main__':
    unittest.main()
