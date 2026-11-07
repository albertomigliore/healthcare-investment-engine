"""The browser engine (app/engine.js) must reproduce the Python valuation. Skipped if Node.js isn't installed."""
import shutil
import subprocess

import pytest

from config import settings


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js not installed")
def test_javascript_engine_matches_python():
    app = settings.PROJECT_ROOT / "app"
    if not (app / "data.js").exists():
        pytest.skip("run `python -m src.export_app` first")
    result = subprocess.run(["node", str(app / "engine.test.js")], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
