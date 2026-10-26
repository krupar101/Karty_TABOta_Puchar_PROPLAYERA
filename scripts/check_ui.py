"""Render every screen with real Qt Quick. No display server or network needed."""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent.parent
screens = ["menu", "slots", "intro", "map", "briefing", "battle", "pause", "result", "collection", "builder", "fortune", "reading", "history", "settings", "help", "journal", "ending"]


def check(screen):
    with tempfile.TemporaryDirectory(prefix="tabota-ui-") as tmp:
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software", TABOTA_DATA_DIR=tmp, TABOTA_NO_AUDIO="1")
        result = subprocess.run([sys.executable, "main.py", "--demo", "--screen", screen, "--screenshot", f"test-artifacts/{screen}.png"], cwd=root, env=env, capture_output=True, text=True, timeout=40)
        return screen, result.returncode, result.stdout + result.stderr


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, screens))
for screen, code, output in results:
    print(f"{'FAIL' if code else 'PASS'} {screen}")
    if output: print(output.rstrip())
raise SystemExit(int(any(code for _, code, _ in results)))
