"""Build using this interpreter's OS (Windows Python also works under Wine)."""
import argparse
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("--platform-output", action="store_true",
                    help="Keep Linux/Windows artifacts in separate dist/build directories.")
args = parser.parse_args()
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
command = [sys.executable, "-m", "PyInstaller", "--noconfirm", "tabota.spec"]
destination = root / "dist"
if args.platform_output:
    arch = platform.machine().lower()
    if arch == "amd64": arch = "x86_64"
    target = f"{platform.system().lower()}-{arch}"
    destination /= target
    command += ["--distpath", str(destination), "--workpath", str(root / "build" / target)]
subprocess.run(command, cwd=root, check=True)
print("Build ready in", destination)
