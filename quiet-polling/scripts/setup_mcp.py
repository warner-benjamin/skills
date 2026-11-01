#!/usr/bin/env python3
"""Register this installed quiet-polling server and reload Codex's MCP connections."""
import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import tomllib

from quiet_polling import CodexRPC, codex_executable


@contextmanager
def app_server(home):
    socket = home / 'app-server-control/app-server-control.sock'
    if socket.exists():
        with CodexRPC(socket, timeout=30) as rpc:
            yield rpc, True
        return
    # An isolated server supplies Codex's config writer when the app is closed.
    with tempfile.TemporaryDirectory(prefix='quiet-polling-setup-') as tmp:
        # Let Codex create the socket directory with its own Windows ACLs.
        socket = Path(tmp) / 'control/server.sock'
        with (Path(tmp) / 'server.log').open('w') as log:
            process = subprocess.Popen([codex_executable(), 'app-server', '--listen', f'unix://{socket}'],
                                       env={**os.environ, 'CODEX_HOME': str(home)}, cwd=home,
                                       stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 15
                while not socket.exists():
                    if process.poll() is not None:
                        error = (Path(tmp) / 'server.log').read_text().strip()
                        raise RuntimeError(f'Temporary Codex app-server failed to start: {error}')
                    if time.monotonic() >= deadline:
                        raise TimeoutError('Temporary Codex app-server did not start within 15 seconds')
                    time.sleep(.05)
                with CodexRPC(socket, timeout=30) as rpc:
                    yield rpc, False
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def setup(home):
    home.mkdir(parents=True, exist_ok=True)
    config_path = home / 'config.toml'
    config = tomllib.loads(config_path.read_text()) if config_path.exists() else {}
    current = config.get('mcp_servers', {}).get('quiet_polling', {})
    script = str(Path(__file__).resolve().with_name('quiet_polling.py'))
    if current:
        args = list(current.get('args', []))
        matches = [i for i, arg in enumerate(args) if Path(arg).name == 'quiet_polling.py']
        if len(matches) != 1 or not current.get('command'):
            raise ValueError('quiet_polling has a custom launch configuration; update its script path manually')
        args[matches[0]] = script
        values = {'args': args}
    else:
        values = {'command': sys.executable, 'args': [script], 'tool_timeout_sec': 30}
    edits = [{'keyPath': f'mcp_servers.quiet_polling.{key}', 'value': value, 'mergeStrategy': 'replace'}
             for key, value in values.items() if current.get(key) != value]
    with app_server(home) as (rpc, running):
        if edits:
            rpc.call('config/batchWrite', {'filePath': str(config_path), 'edits': edits})
        rpc.call('config/mcpServer/reload', {})
        if current.get('enabled') is False:
            print('quiet_polling registration updated; it remains disabled in your configuration.')
            return
        result = rpc.call('mcpServerStatus/list', {'serverName': 'quiet_polling'})
        server = next((s for s in result['data'] if s['name'] == 'quiet_polling'), None)
        if not server or server.get('toolsError') or len(server['tools']) != 3:
            raise RuntimeError('quiet_polling is registered, but MCP tool discovery failed')
        print('Registered quiet_polling; all three MCP tools are available.')
        print('Reloaded MCP connections in the running app-server.' if running else
              'Codex was not running; the MCP server will load when Codex starts.')


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path,
                        default=Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')))
    args = parser.parse_args()
    setup(args.codex_home.expanduser().resolve())


if __name__ == '__main__':
    main()
