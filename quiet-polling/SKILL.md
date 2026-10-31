---
name: quiet-polling
description: Wait quietly for long-running jobs or schedule a later wake in this chat. Use for builds, long-running tests, training, batch processing, remote jobs, requested infrequent checks, or requests to check back in hours.
---

# Quiet polling

The user prefers infrequent checks and brief updates to reduce unnecessary model calls, quota usage, and interruptions. Stay silent between scheduled checks; keep working until the job and required follow-up are complete.

Stay in the turn with native waits when you need their completion signal or the job depends on the session staying alive. Use `wake_after` for a planned check after ending the turn, such as a requested check in hours or a detached remote job. Apply this to tests only when they are expected to take, or have already run for, more than several minutes.

## Wait for work

While staying in the turn, use the tool that owns the work:

- Shell session: `write_stdin` with its session ID and empty input.
- Running exec cell: `functions.wait` with the cell ID returned by `functions.exec`.
- Existing agents: `collaboration.wait_agent`; messages arrive separately from its wait result. Inspect them and resume waiting if work remains.
- Timer or remote status check within the current turn: `clock.sleep`, then query if needed. Job completion does not wake this timer; user input can interrupt it.

Follow tool and runtime limits, chaining shorter waits to the next check deadline using actual elapsed time. An internal timeout does not itself call for a status query or commentary. Do useful independent work when available.

For unknown runtimes, use delays of **5 → 10 → 15 → 20 → 25 → 30 minutes** between status checks, then repeat 30 minutes. Advance only when a scheduled check finds the job still running; routine output and shorter internal waits do not reset or advance this schedule. For predictable jobs, choose the smallest interval that covers the expected remaining runtime, capped at 30 minutes. For builds and tests that gate the next step, repeat 5 minutes. Completion-aware waits can return sooner; handle completion promptly. Keep the job ID and next check time.

## Resume this chat later

Use `wake_after` to schedule a later check, such as in 1, 5, or 12 hours, up to 24 hours away. Use a new descriptive `idempotency_key` for each new check; reuse a key only to retry the same registration.

Use `pause_goal: true` (the default) when this is the only outstanding wait and there is no other work to do in parallel. This pauses an active goal and resumes it when the timer is due. Otherwise, pass `pause_goal: false` so other work can continue. Choose this automatically from the remaining work. After confirmed registration with `goal_paused: true`, finish the current turn. Later goal changes do not cancel the timer; use `wake_cancel` to stop it.

When woken, perform the planned check and verify the job's state. If another later check is needed, register it with a new key.

Ordinary user input does not cancel a timer. Use `wake_cancel` when it is no longer wanted; if it paused a goal, tell the user the goal remains paused and they can resume it through the goal controls. Use `wake_status` for inspection, not periodic polling. Crashes require human-directed recovery; do not automatically rearm an uncertain pause or delivery.

## Communicate

Give one brief launch or registration update, then report completion, failure, blockers, or meaningful changes. Do not narrate waits or unchanged status. Follow higher-priority runtime update requirements.

A timer firing or a wait timing out does not prove job success or authorize cancellation. Verify terminal status and outputs before reporting success. Do not promise a later wake without a confirmed registration.
