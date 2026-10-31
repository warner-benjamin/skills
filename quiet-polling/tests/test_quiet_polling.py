import fcntl
from itertools import count
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from quiet_polling import Service, bound_thread, seconds_value

META = {'threadId': 't'}
OTHER = {'threadId': 'other'}


class RPC:
    def __init__(self):
        self.state = None
        self.messages = []
        self.offline = False
        self.mutations = []

    def __call__(self, socket=None):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def close(self):
        pass

    def goal(self, thread):
        if self.offline:
            raise ConnectionError('offline')
        return {'status': self.state} if self.state else None

    def set_goal_status(self, thread, status):
        self.mutations.append(status)
        self.state = status
        return self.goal(thread)

    def notify(self, thread, output):
        self.messages.append((thread, output))
        return 'wake-turn'


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.rpc = RPC()
        self.s = Service(self.temp.name, socket='/tmp/fixture.sock', rpc_factory=self.rpc)
        self.workers = {}
        self.launched = []
        self.s.launch = self.launch

    def launch(self, wake):
        self.launched.append(wake)
        lock = self.s.store.path(wake).with_suffix('.worker.lock').open('a')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.workers[wake] = lock

    def update_record(self, wake, **changes):
        record = self.s.store.read(wake)
        record.update(changes)
        self.s.store.write(record)

    def stop_worker(self, wake):
        self.workers.pop(wake).close()

    def tearDown(self):
        for lock in self.workers.values():
            lock.close()
        self.temp.cleanup()

    def after(self, seconds=7200, key='test-wake', meta=META, pause_goal=False):
        return self.s.after({'seconds': seconds, 'idempotency_key': key, 'pause_goal': pause_goal}, meta)

    def test_default_pauses_active_goal_and_resumes_without_notification(self):
        self.rpc.state = 'active'
        result = self.s.after({'seconds': 7200, 'idempotency_key': 'default'}, META)
        self.assertTrue(result['goal_paused'])
        self.assertTrue(result['worker_running'])
        self.assertEqual(self.rpc.state, 'paused')
        self.due(result)
        self.s.deliver(result['wake_id'])
        self.s.deliver(result['wake_id'])
        self.assertEqual(self.rpc.state, 'active')
        self.assertEqual(self.rpc.mutations, ['paused', 'active'])
        self.assertFalse(self.rpc.messages)
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'resumed')
        self.assertFalse(self.s.invoke('wake_cancel', {'wake_id': result['wake_id']}, META)['cancelled'])
        retry = self.s.after({'seconds': 7200, 'idempotency_key': 'default'}, META)
        self.assertEqual(retry['state'], 'resumed')
        self.assertFalse(retry['goal_paused'])
        self.assertEqual(self.rpc.mutations, ['paused', 'active'])

    def test_second_timer_cannot_take_over_existing_pause(self):
        self.rpc.state = 'active'
        result = self.after(pause_goal=True)
        with self.assertRaisesRegex(ValueError, 'already inactive'):
            self.after(key='second', pause_goal=True)
        self.assertEqual(len(self.launched), 1)
        self.assertEqual(self.rpc.mutations, ['paused'])
        self.assertEqual(self.after(pause_goal=True)['wake_id'], result['wake_id'])

    def test_cancel_timer_leaves_goal_paused(self):
        self.rpc.state = 'active'
        result = self.after(pause_goal=True)
        self.s.invoke('wake_cancel', {'wake_id': result['wake_id']}, META)
        self.due(result)
        self.s.deliver(result['wake_id'])
        self.assertEqual(self.rpc.state, 'paused')
        self.assertEqual(self.rpc.mutations, ['paused'])
        retry = self.after(pause_goal=True)
        self.assertEqual(retry['state'], 'cancelled')
        self.assertFalse(retry['goal_paused'])

    def test_manual_worker_restart_does_not_pause_again(self):
        self.rpc.state = 'active'
        first = self.after(pause_goal=True)
        self.stop_worker(first['wake_id'])
        self.assertFalse(self.s.invoke('wake_status', {'wake_id': first['wake_id']}, META)['worker_running'])
        second = self.after(pause_goal=True)
        self.assertEqual(first['due_at'], second['due_at'])
        self.assertEqual(self.rpc.mutations, ['paused'])
        self.assertEqual(len(self.launched), 2)

    def test_pause_failure_never_replays_or_starts_worker(self):
        self.rpc.state = 'active'
        def fail(*args):
            self.rpc.state = 'paused'
            raise TimeoutError('pause receipt lost')
        self.rpc.set_goal_status = fail
        result = self.after(pause_goal=True)
        self.assertEqual(result['state'], 'pause_unknown')
        self.assertFalse(result['worker_running'])
        self.rpc.set_goal_status = lambda *args: self.fail('pause replayed')
        self.assertEqual(self.after(pause_goal=True)['state'], 'pause_unknown')

    def test_resume_failure_never_replays(self):
        self.rpc.state = 'active'
        result = self.after(pause_goal=True)
        self.due(result)
        def fail(*args):
            self.rpc.state = 'active'
            raise TimeoutError('resume receipt lost')
        self.rpc.set_goal_status = fail
        self.s.deliver(result['wake_id'])
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'delivery_unknown')
        self.rpc.set_goal_status = lambda *args: self.fail('resume replayed')
        self.s.deliver(result['wake_id'])
        retry = self.after(pause_goal=True)
        self.assertEqual(retry['state'], 'delivery_unknown')
        self.assertFalse(retry['goal_paused'])

    def test_pause_mode_conflict_rejects_retry(self):
        self.after(pause_goal=False)
        with self.assertRaisesRegex(ValueError, 'different pause_goal'):
            self.after(pause_goal=True)

    def test_invalid_pause_mode_rejected_before_mutation(self):
        for value in (None, 0, 'false'):
            with self.assertRaisesRegex(ValueError, 'boolean'):
                self.after(pause_goal=value)
        self.assertFalse(self.rpc.mutations)

    def due(self, result):
        self.update_record(result['wake_id'], deadline=time.time() - 1)

    def test_register_later_wake(self):
        before = time.time()
        result = self.after(18000)
        self.assertEqual(result['state'], 'scheduled')
        self.assertTrue(result['worker_running'])
        self.assertFalse(result['goal_paused'])
        self.assertAlmostEqual(self.s.store.read(result['wake_id'])['deadline'], before + 18000, delta=1)

    def test_retry_new_call_id_preserves_identity_and_deadline(self):
        first = self.after(meta={**META, 'callId': 'first'})
        second = self.after(meta={**META, 'callId': 'retry'})
        self.assertEqual(first['wake_id'], second['wake_id'])
        self.assertEqual(first['due_at'], second['due_at'])
        self.assertEqual(len(self.launched), 1)

    def test_key_conflict_does_not_change_schedule(self):
        first = self.after()
        with self.assertRaisesRegex(ValueError, 'different delay'):
            self.after(18000)
        self.assertEqual(self.s.store.read(first['wake_id'])['due_at'], first['due_at'])

    def test_same_key_is_scoped_to_chat(self):
        self.assertNotEqual(self.after()['wake_id'], self.after(meta=OTHER)['wake_id'])

    def test_unknown_goal_fails_without_registering(self):
        self.rpc.offline = True
        with self.assertRaises(ConnectionError):
            self.after(pause_goal=True)
        self.assertFalse(list(Path(self.temp.name).glob('*.json')))

    def test_deliver_only_when_due_and_once(self):
        result = self.after()
        self.s.deliver(result['wake_id'])
        self.assertFalse(self.rpc.messages)
        self.due(result)
        self.s.deliver(result['wake_id'])
        self.s.deliver(result['wake_id'])
        self.assertEqual(len(self.rpc.messages), 1)
        self.assertEqual(self.rpc.messages[0][1]['event'], 'timer_elapsed')
        self.assertEqual(self.rpc.messages[0][1]['due_at'], result['due_at'])
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'submitted')

    def test_nonpausing_wake_delivers_while_goal_stays_paused(self):
        self.rpc.state = 'paused'
        result = self.after()
        self.due(result)
        self.s.deliver(result['wake_id'])
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'submitted')
        self.assertEqual(self.rpc.state, 'paused')
        self.assertEqual(len(self.rpc.messages), 1)

    def test_connection_failure_before_submission_can_retry(self):
        result = self.after()
        self.due(result)
        with patch.object(self.s, 'rpc_factory', side_effect=ConnectionError('offline')):
            self.s.deliver(result['wake_id'])
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'scheduled')
        self.s.deliver(result['wake_id'])
        self.assertEqual(len(self.rpc.messages), 1)

    def test_uncertain_submission_never_replays(self):
        result = self.after()
        self.due(result)
        def fail(*args):
            raise TimeoutError('receipt lost')
        self.rpc.notify = fail
        self.s.deliver(result['wake_id'])
        self.assertEqual(self.s.store.read(result['wake_id'])['state'], 'delivery_unknown')
        self.rpc.notify = lambda *args: self.fail('replayed')
        self.s.deliver(result['wake_id'])
        self.after(meta={**META, 'callId': 'retry'})
        self.assertEqual(len(self.launched), 1)

    def test_cancel_suppresses_submission(self):
        result = self.after()
        self.due(result)
        cancelled = self.s.invoke('wake_cancel', {'wake_id': result['wake_id']}, META)
        self.assertTrue(cancelled['cancelled'])
        self.s.deliver(result['wake_id'])
        self.assertFalse(self.rpc.messages)
        self.assertEqual(self.after()['state'], 'cancelled')

    def test_cancel_after_submission_cannot_recall(self):
        result = self.after()
        self.due(result)
        self.s.deliver(result['wake_id'])
        self.assertFalse(self.s.invoke('wake_cancel', {'wake_id': result['wake_id']}, META)['cancelled'])

    def test_crash_during_submission_is_uncertain_and_not_resumed(self):
        result = self.after()
        self.update_record(result['wake_id'], state='submitting')
        self.stop_worker(result['wake_id'])
        status = self.s.invoke('wake_status', {'wake_id': result['wake_id']}, META)
        self.assertEqual(status['state'], 'delivery_unknown')
        self.assertFalse(status['worker_running'])
        self.assertEqual(self.after()['state'], 'delivery_unknown')
        self.assertEqual(len(self.launched), 1)

    def test_startup_failure_does_not_claim_registration_is_running(self):
        self.s.launch = lambda wake: None
        with patch('quiet_polling.time.monotonic', side_effect=count(0, 6)):
            with self.assertRaisesRegex(RuntimeError, 'startup not confirmed'):
                self.after()
        records = self.s.invoke('wake_status', {}, META)['wakes']
        self.assertEqual(records[0]['state'], 'scheduled')
        self.assertFalse(records[0]['worker_running'])

    def test_workers_deliver_once_after_shared_probe_releases(self):
        result = self.after()
        wake = result['wake_id']
        self.due(result)
        self.stop_worker(wake)
        with self.s.store.path(wake).with_suffix('.worker.lock').open('a') as probe:
            fcntl.flock(probe, fcntl.LOCK_SH)
            workers = [threading.Thread(target=self.s.worker, args=(wake,)) for _ in range(2)]
            for worker in workers:
                worker.start()
        for worker in workers:
            worker.join(2)
            self.assertFalse(worker.is_alive())
        self.assertEqual(len(self.rpc.messages), 1)
        self.assertEqual(self.s.store.read(wake)['state'], 'submitted')

    def test_other_chat_cannot_inspect_or_cancel(self):
        result = self.after()
        for name in ('wake_status', 'wake_cancel'):
            with self.assertRaises(PermissionError):
                self.s.invoke(name, {'wake_id': result['wake_id']}, OTHER)
        self.assertEqual(self.s.invoke('wake_status', {}, OTHER)['wakes'], [])

    def test_reject_different_server_on_resume(self):
        self.after()
        self.s.socket = '/tmp/other.sock'
        with self.assertRaisesRegex(ValueError, 'different Codex server'):
            self.after()

    def test_validation(self):
        with self.assertRaises(ValueError):
            bound_thread({})
        for value in (-1, 604801, True, float('nan'), float('inf'), '2h', None):
            with self.assertRaises(ValueError):
                seconds_value(value)
        for key in ('', ' ', 'x' * 201, None):
            with self.assertRaises(ValueError):
                self.after(key=key)


if __name__ == '__main__':
    unittest.main()
