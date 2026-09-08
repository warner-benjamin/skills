---
name: quiet-polling
description: Wait quietly for long-running jobs using adaptive polling intervals from 5 to 25 minutes. Use when running or monitoring builds, long-running tests, training, batch processing, remote jobs, or other work expected to take more than several minutes, or when the user requests quiet, infrequent progress checks.
---

# Quiet polling

The user prefers infrequent checks and brief updates to reduce unnecessary model calls, quota usage, and interruptions. Stay silent between scheduled checks; keep working until the job and required follow-up are complete.

Apply this skill to tests only when they are expected to take, or have already run for, more than several minutes.

## Choose the interval

Use intervals of **5 → 10 → 15 → 20 → 25 minutes**, then repeat 25. These are delays between checks, not elapsed-time milestones.

| Minutes | Milliseconds |
| --- | --- |
| 5 | 300000 |
| 10 | 600000 |
| 15 | 900000 |
| 20 | 1200000 |
| 25 | 1500000 |

- Unknown runtime: start at 5 minutes. Known remaining runtime: choose the smallest interval that covers it, capped at 25; an 8-minute job starts at 10.
- Advance one rung whenever a scheduled check finds the job still running. Routine output or early tool returns do not reset or advance the schedule.
- For builds and long-running tests that gate the next step, repeat the 5-minute interval instead of increasing it; completion-aware waits should still return immediately when the job finishes.
- Confirm launch and retain the job ID, interval, and next deadline. Start a fresh schedule for each new job.
- Never schedule more than 25 minutes between checks. This leaves a margin below the documented 30-minute minimum prompt-cache lifetime after a write or reuse.

## Wait with the available tools

Prefer completion-aware waits; follow the current tool's schema and limits:

| Work | Tool | Wake behavior |
| --- | --- | --- |
| Shell session | `write_stdin(session_id, chars="", yield_time_ms)` | Returns on process exit, including failure, or timeout. Ordinary output alone did not wake the tested poll. |
| Yielded exec cell | `functions.wait(cell_id, yield_time_ms)` | Returns on cell completion or timeout; timeout preserves the running cell and returns new buffered output. Requires a running cell ID. |
| Existing agents | `collaboration.wait_agent(timeout_ms)` | Wakes on an agent message before completion, on completion, or at timeout. Messages arrive separately from the wait result; resume waiting if work remains. |
| Remote status API | `clock.sleep(duration_ms)`, then query | Sleeps for the duration; unrelated job completion does not wake it. User input can interrupt it according to the tool contract. |

If a tool cannot wait the full interval, chain supported waits to the deadline using actual elapsed time. Do not add commentary or remote status requests just because an internal wait returned. Avoid busy loops. A wait timeout does not authorize cancelling or restarting the job. Do useful independent work when available, while preserving the next check deadline.

## Communicate sparingly

Give one brief launch update with the initial check interval. At each scheduled check, give a concise status update and the next interval. Do not narrate sleeps, tool retries, heartbeats, or unchanged logs between those checks. If the user wants more details, they will use the side chat option.

React promptly to detected completion, failure, blockers, or user input. Verify terminal status and outputs before reporting success. Otherwise keep waiting; do not end the turn promising to monitor unless persistent monitoring is actually active.
