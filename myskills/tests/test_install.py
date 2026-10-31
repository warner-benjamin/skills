import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location('install', Path(__file__).parents[1] / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTest(unittest.TestCase):
    def test_replaces_top_level_skills_and_follows_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / 'repo'
            source = repository / '.external_resources/upstream'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('upstream skill')
            (repository / 'linked').symlink_to(source, target_is_directory=True)
            local = repository / 'local'
            local.mkdir()
            (local / 'SKILL.md').write_text('updated local skill')
            (local / 'scripts').mkdir()
            (local / 'scripts/run.py').write_text('print("installed helper")')
            home = root / 'home'
            old = home / 'skills/local'
            old.mkdir(parents=True)
            (old / 'obsolete.txt').touch()
            unrelated = home / 'skills/unrelated'
            unrelated.mkdir()
            (unrelated / 'SKILL.md').write_text('keep this')

            installer.install(repository, home)

            self.assertEqual({p.name for p in (home / 'skills').iterdir()}, {'linked', 'local', 'unrelated'})
            self.assertEqual((old / 'SKILL.md').read_text(), 'updated local skill')
            self.assertEqual((old / 'scripts/run.py').read_text(), 'print("installed helper")')
            self.assertFalse((old / 'obsolete.txt').exists())
            self.assertFalse((home / 'skills/linked').is_symlink())
            self.assertEqual((home / 'skills/linked/SKILL.md').read_text(), 'upstream skill')
            self.assertEqual((unrelated / 'SKILL.md').read_text(), 'keep this')
            self.assertTrue((source / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
