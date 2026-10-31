#!/usr/bin/env python3
"""Install this repository's top-level skills and configure quiet-polling."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def install(repository, codex_home):
    destination = codex_home / 'skills'
    sources = sorted(p for p in repository.iterdir()
                     if not p.name.startswith('.') and (p / 'SKILL.md').is_file())
    if not sources:
        raise ValueError(f'No top-level skills found in {repository}')
    for source in sources:
        target = destination / source.name
        if (source.resolve() == target.resolve() or source.resolve() in target.resolve().parents
                or target.resolve() in source.resolve().parents):
            raise ValueError(f'Installation would overwrite or copy into the source: {source}')
    destination.mkdir(parents=True, exist_ok=True)
    for source in sources:
        target = destination / source.name
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        print(f'Installed {source.name}', flush=True)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--codex-home', type=Path,
                        default=Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')))
    args = parser.parse_args()
    home = args.codex_home.expanduser().resolve()
    destination = install(args.repo.expanduser().resolve(), home)
    subprocess.run([sys.executable, str(destination / 'quiet-polling/scripts/setup_mcp.py'),
                    '--codex-home', str(home)], check=True)


if __name__ == '__main__':
    main()
