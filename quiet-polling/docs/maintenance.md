# Scheduled wake tool maintenance

For people installing or changing the server. Agents using the connected tool only need the skill and MCP descriptions.

## Setup

The server has Linux and native Windows implementations, without third-party Python dependencies or API keys. `$myskills` installs the skills and configures this server automatically. Setup requires Python 3.11+ and Codex on `PATH` (`codex.exe` on Windows). The Windows implementation still needs validation on a Windows host.

To register or reload an already installed copy, run:

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/quiet-polling/scripts/setup_mcp.py"
```

On Windows, use PowerShell:

```powershell
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
python (Join-Path $codexRoot 'skills/quiet-polling/scripts/setup_mcp.py')
```

Windows connects through `codex app-server proxy`; verify that the installed Codex exposes this command with `codex app-server proxy --help`. The proxy relays the existing WebSocket protocol to the same app-server. File locks use `LockFileEx`. Timer workers detach from the console and parent job; a host that forbids job breakaway will reject worker startup.

The helper points Codex at the installed script, preserves custom settings, reloads MCP connections through the app-server, and checks tool discovery without scheduling a wake. If Codex is closed, it uses a temporary app-server to write and verify the configuration; the connection loads when Codex next starts. An explicitly disabled server stays disabled. Use `--codex-home PATH` for a different installation.

For manual configuration:

```toml
[mcp_servers.quiet_polling]
command = "python3"
args = ["/absolute/path/quiet-polling/scripts/quiet_polling.py"]
tool_timeout_sec = 30
```

Reload the MCP connection after configuration. Registration returns promptly; its timeout does not cover the timer duration. Native approval rules apply.

The socket defaults to `$CODEX_HOME/app-server-control/app-server-control.sock` (or `~/.codex/...`); override it with `--socket PATH`. State defaults to `~/.local/state/codex-quiet-polling/wakes` on Linux and `%LOCALAPPDATA%/codex-quiet-polling/wakes` on Windows; override it with `--state-dir PATH`. Calls bind to the host-provided chat ID. Each record remains tied to that chat and native server.

## Behavior

With `pause_goal: true`, registration pauses an active goal using `thread/goal/set` with `origin: automatic`. At the deadline, the worker sets its status to `active`. It sends no objective or budget and does not inspect goal history. Later goal edits or another pause do not cancel this attempt. Cancellation leaves the goal paused. An inactive goal is rejected; an absent or complete goal uses ordinary notification delivery.

Ordinary delivery sends `turn/start` with empty `input` and a named `quiet_polling.wake_result` tool output. Codex queues it into active work or starts a turn when idle. A running model sees it at the next request boundary. With `pause_goal: false`, registration and delivery neither inspect nor change the goal. User input, stopping a turn, and MCP request cancellation do not cancel a timer.

`goal_paused` means this timer has a pending resume for a pause it made. It is false once the timer is terminal or uncertain; it does not query the goal's current status. `worker_running` checks a live process lock for pending operations. Terminal records do not probe worker processes.

Workers survive MCP-server exit. There is no supervisor or startup recovery: after a crash, the human decides what to resume. Retrying a pending registration with its original arguments starts a worker at the original deadline without another goal pause. Terminal records are retained so reusing their keys cannot schedule another wake.

Persisted states are `pausing`, `pause_unknown`, `scheduled`, `submitting`, `submitted`, `resumed`, `cancelled`, and `delivery_unknown`. Connection failures leave the timer scheduled and retry every 10 seconds. Once an operation is submitted, an error or lost receipt is reported as uncertain and is not replayed. In-flight markers appear as uncertain when no worker owns the operation; a pause still being registered also appears as `pause_unknown`. Failed initial pauses start no worker. Inspect the chat and goal before human-directed recovery.

Cancellation and submission share a per-timer lock. Worker readiness uses a live OS lock; status probes take shared locks. Registration serializes worker launch. New goal-pausing timers take the per-timer lock first, then a per-chat lock for the goal read and pause; their deadline starts after the goal read. Wall-clock changes, machine sleep, and disconnected servers can delay delivery.

## Validation

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s quiet-polling/tests -v
python3 quiet-polling/tests/native_probe.py
```

On Windows, use `python` instead of `python3` and omit the inline environment assignment. The native probe uses PowerShell to identify only its own timer and MCP processes for cleanup.

The opt-in native probe runs all nine scenarios on one disposable Codex server and deterministic localhost inference fixture. It requires localhost permission and records results in a temporary directory. It covers notifications, active-turn delivery, worker survival, cancellation, and goal pause/resume. These seconds-scale checks do not qualify hours-long operation, machine suspend/resume, or real-model comprehension. Review results belong in `docs/reviews/`, not this operational guide.
