# PyInstaller onedir bundle: Qt libraries remain dynamically linked and replaceable.
from pathlib import Path
import sys

root = Path(SPECPATH)
datas = [(str(root / "cursor"), "cursor"), (str(root / "ikona.png"), "."), (str(root / "Game_Design.md"), "."),
         (str(root / "karty-front"), "karty-front"),
         (str(root / "karty-rewers.png"), "."),
         (str(root / "music"), "music"),
         (str(root / "tabota/ui"), "tabota/ui"),
         (str(root / "docs"), "docs"),
         (str(root / "README.md"), "."),
         (str(root / "LICENSE"), "."),
         (str(root / "LICENSE_SCOPE.md"), ".")]
a = Analysis([str(root / "main.py")], pathex=[str(root)], binaries=[], datas=datas,
             hiddenimports=["PySide6.QtQuick", "PySide6.QtQuickControls2", "PySide6.QtMultimedia"],
             hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="TABOt", debug=False,
          bootloader_ignore_signals=False, strip=False, upx=False, console=False,
          disable_windowed_traceback=False, argv_emulation=False, target_arch=None,
          codesign_identity=None, entitlements_file=None,
          icon=str(root / "ikona.ico") if sys.platform == "win32" else None)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="TABOt")
if sys.platform == "darwin":
    app = BUNDLE(coll, name="TABOt.app", icon=str(root / "ikona.icns"), bundle_identifier="pl.tabota.game",
                 info_plist={"CFBundleShortVersionString": "1.0.0", "NSHighResolutionCapable": True})
