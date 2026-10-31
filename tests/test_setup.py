"""Installer behavior checks using isolated user directories; no live configuration writes."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def snapshot(directory):
    return {
        p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob('*') if p.is_file()
    }


class InstallerChecks:
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='evo-dev-install-')
        self.addCleanup(self.temporary.cleanup)
        self.user = Path(self.temporary.name) / 'user with spaces'
        self.user.mkdir()
        self.codex = self.user / '.codex'
        self.skill = self.user / '.agents/skills/project-setup'
        self.environment = os.environ.copy()
        self.environment.pop('CODEX_HOME', None)

    def run_setup(self, expected=0):
        result = subprocess.run(
            self.command + [str(self.user)], cwd=self.temporary.name,
            env=self.environment, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def write(self, path, contents):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding='utf-8')

    def test_fresh_install_and_repeat_preserve_unrelated_configuration(self):
        self.write(self.codex / 'config.toml', 'model = "my-existing-model"\n')
        self.write(self.codex / 'auth.json', 'existing credential sentinel')
        self.write(self.user / '.agents/skills/other/SKILL.md', 'existing other skill')
        before = snapshot(self.user)
        self.run_setup()
        for path, digest in before.items():
            self.assertEqual(snapshot(self.user)[path], digest)
        self.assertEqual((self.codex / 'AGENTS.md').read_bytes(), (ROOT / 'profile/AGENTS.md').read_bytes())
        self.assertEqual(snapshot(self.skill), snapshot(ROOT / 'skills/project-setup'))
        installed = snapshot(self.user)
        self.assertIn('UNCHANGED:', self.run_setup())
        self.assertEqual(installed, snapshot(self.user))

    def test_differing_profile_and_customized_skill_are_preserved(self):
        self.write(self.codex / 'AGENTS.md', 'My existing rules\n')
        shutil.copytree(ROOT / 'skills/project-setup', self.skill)
        self.write(self.skill / 'SKILL.md', 'Locally customized skill\n')
        self.write(self.skill / 'local-notes.md', 'Keep extra files too\n')
        before = snapshot(self.user)
        self.assertIn('REVIEW:', self.run_setup(expected=1))
        self.assertEqual(before, snapshot(self.user))

    def test_empty_existing_profile_is_preserved(self):
        self.write(self.codex / 'AGENTS.md', '')
        self.run_setup(expected=1)
        self.assertEqual((self.codex / 'AGENTS.md').read_bytes(), b'')
        self.assertTrue((self.skill / 'SKILL.md').is_file())

    def test_empty_existing_skill_directory_is_preserved(self):
        self.skill.mkdir(parents=True)
        self.assertIn('REVIEW:', self.run_setup(expected=1))
        self.assertEqual(list(self.skill.iterdir()), [])

    def test_codex_home_is_respected(self):
        alternate = Path(self.temporary.name) / 'custom codex home'
        self.environment['CODEX_HOME'] = str(alternate)
        self.run_setup()
        self.assertTrue((alternate / 'AGENTS.md').is_file())
        self.assertFalse(self.codex.exists())
        self.assertTrue((self.skill / 'SKILL.md').is_file())

    def test_alternate_skill_installation_prevents_duplicate(self):
        self.write(self.codex / 'skills/project-setup/SKILL.md', 'Legacy installation')
        self.run_setup(expected=1)
        self.assertFalse(self.skill.exists())
        self.assertEqual((self.codex / 'skills/project-setup/SKILL.md').read_text(), 'Legacy installation')

    def test_override_is_reported_and_preserved(self):
        self.write(self.codex / 'AGENTS.override.md', 'My temporary override')
        self.assertIn('AGENTS.override.md', self.run_setup(expected=1))
        self.assertEqual((self.codex / 'AGENTS.override.md').read_text(), 'My temporary override')

    def test_unexpected_destination_type_is_preserved(self):
        self.write(self.codex / 'AGENTS.md/AGENTS.md', 'A directory, not a profile')
        self.write(self.skill, 'A file, not a skill directory')
        before = snapshot(self.user)
        self.run_setup(expected=1)
        self.assertEqual(before, snapshot(self.user))

    def test_matching_symlink_is_preserved(self):
        self.skill.parent.mkdir(parents=True)
        try:
            self.skill.symlink_to(ROOT / 'skills/project-setup', target_is_directory=True)
        except OSError:
            self.skipTest('Symlink creation unavailable for this user')
        self.run_setup()
        self.assertTrue(self.skill.is_symlink())
        self.assertEqual(self.skill.resolve(), ROOT / 'skills/project-setup')

    def test_broken_symlink_is_preserved(self):
        self.skill.parent.mkdir(parents=True)
        try:
            self.skill.symlink_to(self.user / 'missing-skill', target_is_directory=True)
        except OSError:
            self.skipTest('Symlink creation unavailable for this user')
        self.run_setup(expected=1)
        self.assertTrue(self.skill.is_symlink())
        self.assertFalse((self.user / 'missing-skill').exists())


@unittest.skipUnless(shutil.which('sh'), 'POSIX shell unavailable')
class ShellInstallerTests(InstallerChecks, unittest.TestCase):
    command = ['sh', str(ROOT / 'setup.sh'), '--user-directory']


@unittest.skipUnless(shutil.which('pwsh') or shutil.which('powershell'), 'PowerShell unavailable')
class PowerShellInstallerTests(InstallerChecks, unittest.TestCase):
    command = [shutil.which('pwsh') or shutil.which('powershell') or 'pwsh',
               '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ROOT / 'setup.ps1'), '-UserDirectory']


if __name__ == '__main__':
    unittest.main()
