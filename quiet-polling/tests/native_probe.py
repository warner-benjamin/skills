#!/usr/bin/env python3
"""Opt-in native smoke test: disposable app-server, fake inference, no credentials.

Needs permission to bind localhost and launch Codex. This runs seconds-scale
cases; it does not test real-model behavior or production-duration waiting.
"""
import json
import time
import uuid
import os
from pathlib import Path
import signal

from native_harness import Provider as BaseProvider, processes, run_probe, until


class Provider(BaseProvider):
    def do_POST(self):
        body, meta, count = self.read_request()
        if self.server.gate_next:
            self.server.gate_next = False
            self.server.entered.set()
            self.server.release.wait(10)
        if meta.get('turn_trigger') == 'goal':
            # Throttle fixture goal continuations while waiting for timer delivery.
            time.sleep(.1)
        if count == 2 and any('busy' in json.dumps(x) for x in body['input'] if x.get('role') == 'user'):
            self.server.entered.set()
            self.server.release.wait(10)
        if count == 1:
            user = next(x for x in reversed(body['input']) if x.get('role') == 'user')
            scenario = next(x for x in ('survive', 'cancel', 'goalafter', 'busy', 'paused') if x in json.dumps(user))
            args = {'seconds': 3, 'idempotency_key': scenario, 'pause_goal': False}
            item = {'type': 'function_call', 'id': 'fc_' + uuid.uuid4().hex,
                    'call_id': 'call_' + uuid.uuid4().hex, 'name': 'wake_after',
                    'namespace': 'mcp__quiet_polling', 'arguments': json.dumps(args)}
        elif count == 2 and any('cancel' in json.dumps(x) for x in body['input'] if x.get('role') == 'user'):
            output = next(x['output'] for x in reversed(body['input']) if x.get('type') == 'function_call_output')
            job = json.loads(output[output.index('{'):])['wake_id']
            item = {'type': 'function_call', 'id': 'fc_' + uuid.uuid4().hex,
                    'call_id': 'cancel_' + uuid.uuid4().hex, 'name': 'wake_cancel',
                    'namespace': 'mcp__quiet_polling', 'arguments': json.dumps({'wake_id': job})}
        else:
            item = {'id': 'msg_' + uuid.uuid4().hex, 'type': 'message', 'role': 'assistant',
                    'status': 'completed', 'content': [{'type': 'output_text', 'text': 'fixture done', 'annotations': []}]}
        self.reply(item)


def run_cases(probe):
    root, state, rpc, fixture = probe.root, probe.state, probe.rpc, probe.fixture
    config, report, threads = probe.config, probe.report, probe.threads
    record_for, finished = probe.record_for, probe.finished
    def outputs(thread):
        return [(index, req['metadata'], item) for index, req in enumerate(fixture.requests)
                if req['metadata']['thread_id'] == thread for item in req['body']['input']
                if item.get('name') == 'wake_result']
    for scenario in ('survive', 'cancel', 'goalafter', 'busy', 'paused'):
        t = rpc.call('thread/start', {'model': 'gpt-6.1-terra', 'modelProvider': 'probe', 'cwd': str(root),
                     'approvalPolicy': 'never', 'sandbox': 'read-only', 'config': config})['thread']['id']
        threads.append(t)
        fixture.entered.clear(); fixture.release.clear()
        if scenario == 'paused':
            fixture.gate_next = True
        turn = rpc.call('turn/start', {'threadId': t, 'input': [{'type': 'text', 'text': scenario}]})['turn']['id']
        if scenario == 'paused':
            assert fixture.entered.wait(8)
            rpc.call('thread/goal/set', {'threadId': t, 'objective': 'Remain paused during fixture delivery',
                     'tokenBudget': 10000, 'status': 'paused', 'origin': 'user'})
            assert rpc.goal(t)['status'] == 'paused'
            fixture.release.set()
        record = until(lambda: record_for(t))
        case = report['cases'][scenario] = {'thread': t, 'turn': turn, 'wake_id': record['wake_id']}
        if scenario == 'busy':
            assert fixture.entered.wait(8)
            case['record'] = until(lambda: (v if (v := record_for(t))['state'] == 'submitted' else None))
            assert case['record']['wake_turn_id'] == turn
            assert not outputs(t), 'A model request started before the held request returned'
            fixture.release.set()
            case['notice'] = until(lambda: outputs(t))[0]
            assert case['notice'][1]['turn_id'] == turn
            case['completion'] = until(lambda: finished(t, turn))
            case['same_turn_delivery'] = True
        else:
            case['completion'] = until(lambda: finished(t, turn))
            if scenario == 'paused':
                case['goal_before_delivery'] = rpc.goal(t)
                assert case['goal_before_delivery']['status'] == 'paused'
                assert record_for(t)['state'] == 'scheduled'
                case['record'] = until(lambda: (v if (v := record_for(t))['state'] == 'submitted' else None))
                case['notice'] = until(lambda: outputs(t))[0]
                case['wake_completion'] = until(lambda: finished(t, case['record']['wake_turn_id']))
                case['goal_after_delivery'] = rpc.goal(t)
                for field in ('status', 'objective', 'tokenBudget'):
                    assert case['goal_after_delivery'][field] == case['goal_before_delivery'][field], case
                assert not any(req['metadata'].get('turn_trigger') == 'goal'
                               for req in fixture.requests if req['metadata']['thread_id'] == t)
                case['delivered_without_resuming_goal'] = True
            elif scenario == 'survive':
                pids = processes(state, worker=False)
                assert len(pids) == 1, pids
                case['mcp_server_pid'] = pids[0]
                os.kill(pids[0], signal.SIGTERM)
                until(lambda: not Path('/proc', str(pids[0])).exists())
                case['record'] = until(lambda: (v if (v := record_for(t))['state'] == 'submitted' else None))
                case['notice'] = until(lambda: outputs(t))[0]
            elif scenario == 'cancel':
                case['record'] = record_for(t)
                assert case['record']['state'] == 'cancelled'
                time.sleep(max(0, record['deadline'] - time.time()) + 1)
                assert not outputs(t)
                case['observed_past_deadline'] = True
            else:
                rpc.call('thread/goal/set', {'threadId': t, 'objective': 'Remain active during fixture delivery', 'tokenBudget': 10000})
                case['record'] = until(lambda: (v if (v := record_for(t))['state'] == 'submitted' else None))
                case['notice'] = until(lambda: outputs(t))[0]
                assert rpc.goal(t)['status'] == 'active'
                case['goal_requests'] = sum(req['metadata'].get('turn_trigger') == 'goal' for req in fixture.requests if req['metadata']['thread_id'] == t)
                assert case['goal_requests'] > 0
                rpc.call('thread/goal/clear', {'threadId': t})
        if 'notice' in case:
            delivered = json.loads(case['notice'][2]['output'])
            assert case['notice'][2]['namespace'] == 'quiet_polling'
            assert delivered['event'] == 'timer_elapsed'
            assert delivered['wake_id'] == record['wake_id']
            assert delivered['idempotency_key'] == scenario
            assert delivered['due_at'] == record['due_at']
        rpc.call('thread/goal/clear', {'threadId': t, 'origin': 'automatic'})
        rpc.call('thread/archive', {'threadId': t})
        threads.remove(t)


def all_cases(probe):
    run_cases(probe)
    from native_goal_probe import Provider as GoalProvider, run_cases as goal_cases
    probe.fixture.RequestHandlerClass = GoalProvider
    goal_cases(probe)


if __name__ == '__main__':
    raise SystemExit(run_probe(Provider, all_cases, 'quiet-native-probe-'))
