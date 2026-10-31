"""Optional native Codex packaging check; all configuration stays in a temporary home."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CODEX = os.environ.get('EVO_CODEX_BINARY') or shutil.which('codex')


@unittest.skipUnless(CODEX, 'Set EVO_CODEX_BINARY or install Codex CLI for native packaging validation')
class NativePluginTests(unittest.TestCase):
    def test_marketplace_installs_self_contained_explicit_skills(self):
        with tempfile.TemporaryDirectory(prefix='evo-dev-plugin-') as temporary:
            root = Path(temporary)
            package = root / 'package with spaces'
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('.git', '.DS_Store', '__pycache__'))
            codex_home = root / 'codex'
            codex_home.mkdir()
            environment = {**os.environ, 'CODEX_HOME': str(codex_home)}

            def run(*args):
                result = subprocess.run([CODEX, *args], cwd=root, env=environment,
                                        capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return json.loads(result.stdout)

            run('plugin', 'marketplace', 'add', str(package), '--json')
            installed = run('plugin', 'add', 'evo-dev@evo-dev', '--json')
            installed_root = Path(installed['installedPath'])
            self.assertTrue((installed_root / 'plugin.json').is_file())
            manifest = json.loads((installed_root / 'plugin.json').read_text())
            onboarding = manifest['extensions']['com.openai']['onboardingSkill']
            self.assertTrue((installed_root / onboarding).is_file())
            for name in ('evo-setup', 'project-setup'):
                self.assertTrue((installed_root / 'skills' / name / 'SKILL.md').is_file())
                policy = (installed_root / 'skills' / name / 'agents/openai.yaml').read_text()
                self.assertIn('allow_implicit_invocation: false', policy)
            self.assertEqual((installed_root / 'profile/AGENTS.md').read_bytes(), (ROOT / 'profile/AGENTS.md').read_bytes())
            self.assertFalse((codex_home / 'AGENTS.md').exists(), 'Plugin installation must not apply the profile silently')
            listing = run('plugin', 'list', '--json')
            self.assertTrue(any(p['name'] == 'evo-dev' for p in listing['installed']))
            ordinary_prompt = run('debug', 'prompt-input', 'Describe the current repository.')
            self.assertNotIn('# Evo Dev Setup', json.dumps(ordinary_prompt))
            self.assertNotIn('# Evo Project Setup', json.dumps(ordinary_prompt))
            if shutil.which('sh'):
                user = root / 'profile user'
                result = subprocess.run(['sh', str(installed_root / 'setup.sh'), '--profile-only',
                                         '--user-directory', str(user)],
                                        env={k: v for k, v in os.environ.items() if k != 'CODEX_HOME'},
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((user / '.codex/AGENTS.md').read_bytes(), (ROOT / 'profile/AGENTS.md').read_bytes())
                self.assertFalse((user / '.agents').exists(), 'Onboarding must not install duplicate skills')
