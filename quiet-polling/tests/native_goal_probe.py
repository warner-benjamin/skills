#!/usr/bin/env python3
"""Opt-in integration probe using a disposable native server and fake inference.

Needs localhost bind permission and a compatible Codex CLI. Uses seconds-scale
waits and temporary state; never accesses a real model or an existing chat.
"""
import json
import time
import uuid

from native_harness import Provider as BaseProvider, run_probe, until


class Provider(BaseProvider):
    def do_POST(self):
        body, meta, count = self.read_request()
        if count == 1:
            self.server.entered.set()
            self.server.release.wait(12)
            text = json.dumps(body['input'])
            scenario = next(name for name in self.server.scenarios if 'scenario:' + name in text)
            args = {'seconds': 3, 'idempotency_key': scenario}
            item = {'type': 'function_call', 'id': 'fc_' + uuid.uuid4().hex,
                    'call_id': 'call_' + uuid.uuid4().hex, 'name': 'wake_after',
                    'namespace': 'mcp__quiet_polling', 'arguments': json.dumps(args)}
        elif count == 2 and any('scenario:cancel' in json.dumps(x) for x in body['input'] if x.get('role') == 'user'):
            output = next(x['output'] for x in reversed(body['input']) if x.get('type') == 'function_call_output')
            wake = json.loads(output[output.index('{'):])['wake_id']
            item = {'type': 'function_call', 'id': 'fc_' + uuid.uuid4().hex,
                    'call_id': 'call_' + uuid.uuid4().hex, 'name': 'wake_cancel',
                    'namespace': 'mcp__quiet_polling', 'arguments': json.dumps({'wake_id': wake})}
        else:
            if meta.get('turn_trigger') == 'goal':
                self.server.goal_entered.set()
                self.server.goal_release.wait(12)
            item = {'id': 'msg_' + uuid.uuid4().hex, 'type': 'message', 'role': 'assistant',
                    'status': 'completed', 'content': [{'type': 'output_text', 'text': 'fixture done', 'annotations': []}]}
        self.reply(item)


def run_cases(probe):
    root, rpc, fixture = probe.root, probe.rpc, probe.fixture
    config, report, threads = probe.config, probe.report, probe.threads
    record_for, finished = probe.record_for, probe.finished
    fixture.scenarios = ('happy', 'change', 'cancel', 'no_goal')
    def reqs(thread):
        return [r for r in fixture.requests if r['metadata']['thread_id'] == thread]
    for scenario in fixture.scenarios:
        fixture.entered.clear(); fixture.release.clear(); fixture.goal_entered.clear(); fixture.goal_release.clear()
        t = rpc.call('thread/start', {'model': 'gpt-6.1-terra', 'modelProvider': 'probe', 'cwd': str(root),
                     'approvalPolicy': 'never', 'sandbox': 'read-only', 'config': config})['thread']['id']
        threads.append(t)
        turn = rpc.call('turn/start', {'threadId': t, 'input': [{'type': 'text', 'text': 'scenario:' + scenario}]})['turn']['id']
        assert fixture.entered.wait(8)
        if scenario != 'no_goal':
            rpc.call('thread/goal/set', {'threadId': t, 'objective': 'Preserve fixture objective', 'tokenBudget': 1000, 'origin': 'user'})
        fixture.release.set()
        record = until(lambda: record_for(t))
        case = report['cases']['goal_' + scenario] = {'thread': t, 'turn': turn, 'wake_id': record['wake_id']}
        case['turn_completion'] = until(lambda: finished(t, turn))['status']
        record = record_for(t)
        if scenario != 'no_goal':
            assert record.get('goal_pause'), record
            case['goal_after_registration'] = rpc.goal(t)
            assert case['goal_after_registration']['status'] == 'paused'
        before = len(reqs(t)); case['requests_at_finish'] = before
        if scenario == 'change':
            case['human_mutation'] = rpc.call('thread/goal/set', {'threadId': t,
                'objective': 'Human changed objective', 'tokenBudget': 2000, 'origin': 'user'})
        case['goal_before_resume'] = rpc.goal(t)
        if scenario in ('happy', 'change'):
            time.sleep(max(0, min(.5, record['deadline'] - time.time() - .2)))
            case['requests_during_pause'] = len(reqs(t))
            assert case['requests_during_pause'] == before
        expected = 'resumed' if scenario in ('happy', 'change') else 'submitted' if scenario == 'no_goal' else 'cancelled'
        case['record'] = until(lambda: (r if (r := record_for(t))['state'] == expected else None))
        case['goal_at_terminal'] = rpc.goal(t)
        if scenario in ('happy', 'change'):
            assert fixture.goal_entered.wait(8)
            assert case['goal_at_terminal']['status'] == 'active'
            for key in ('objective', 'tokenBudget', 'tokensUsed', 'timeUsedSeconds'):
                assert case['goal_at_terminal'][key] == case['goal_before_resume'][key], (key, case)
            assert not any(x.get('name') == 'wake_result' for r in reqs(t) for x in r['body']['input'])
            rpc.call('thread/goal/set', {'threadId': t, 'status': 'paused', 'origin': 'automatic'})
            fixture.goal_release.set()
        elif scenario == 'no_goal':
            until(lambda: any(x.get('name') == 'wake_result' for r in reqs(t) for x in r['body']['input']))
        else:
            # wake_cancel is terminal immediately; observe through the original deadline.
            time.sleep(max(.3, record['deadline'] - time.time() + .2))
            assert len(reqs(t)) == before, (scenario, len(reqs(t)), before)
            if scenario == 'cancel':
                assert case['goal_at_terminal']['status'] == 'paused'
        case['requests'] = [{'time': r['time'], 'metadata': r['metadata'],
            'wake_inputs': [x for x in r['body']['input'] if x.get('name') == 'wake_result']} for r in reqs(t)]
        rpc.call('thread/goal/clear', {'threadId': t, 'origin': 'automatic'})
        rpc.call('thread/archive', {'threadId': t})
        threads.remove(t)


if __name__ == '__main__':
    raise SystemExit(run_probe(Provider, run_cases, 'native-goal-probe-'))
