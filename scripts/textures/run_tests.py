"""Run project regressions with temporary files confined to the project workspace."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from net import write_json

root = Path(__file__).resolve().parents[2]
scratch = (root / 'work/texture_pipeline_tests').resolve()
assert scratch.is_relative_to(root.resolve())
scratch.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(scratch)
suite = unittest.defaultTestLoader.discover(str(root / 'tests'))
result = unittest.TextTestRunner(verbosity=2).run(suite)
write_json(root / 'verification/texture_tests.json', {
    'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
    'successful': result.wasSuccessful(),
    'temporary_root': scratch.relative_to(root).as_posix(),
    'failed_tests': [str(case) for case, _ in result.failures + result.errors]})
sys.exit(0 if result.wasSuccessful() else 1)
