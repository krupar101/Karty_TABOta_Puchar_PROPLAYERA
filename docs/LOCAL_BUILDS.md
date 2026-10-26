# Lokalne buildy Linux i Windows

Data: 26.10.2026. Obie paczki powstały na komputerze z Bazzite 44 x86_64.
Nie uruchamiano GitHub Actions i nie publikowano binariów w GitHub Releases.

| Wariant | Środowisko budowania | Plik startowy |
| --- | --- | --- |
| Linux x86_64 | Python 3.14, PySide6 6.11.2, PyInstaller 6.22.3 | `dist/linux-x86_64/TABOt/TABOt` |
| Windows x64 | Windows Python 3.12.10, PySide6 6.11.2, PyInstaller 6.22.3 pod Wine 11 | `dist/windows-x86_64/TABOt/TABOt.exe` |

Każda wersja zawiera własny interpreter i biblioteki. Przenoś cały katalog
`TABOt`, razem z `_internal`, grafikami i muzyką. Użytkownik końcowy nie musi
instalować Pythona. Archiwa i ich sumy SHA-256 są w katalogu `dist/`.

Przed każdym buildem przeszły 94 testy w odpowiednim interpreterze. Dodatkowo
sprawdzane są uruchomienie i renderowanie planszy z gotowych paczek.
Windowsowy plik jest prawdziwym programem PE x64, ale jego test wykonano pod
Wine, nie na osobnym komputerze z Windowsem. Linux był budowany na bieżącym
systemie; zgodność ze starszymi dystrybucjami wymaga osobnej weryfikacji.

## Powtórzenie buildu Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt 'pyinstaller>=6.16,<7'
.venv/bin/python scripts/build.py --platform-output
```

## Powtórzenie buildu Windows na tym komputerze

Osobny prefiks `build/windows/prefix` zawiera Pythona w `C:\Python312`, pakiety
Windows i Microsoft Visual C++ Runtime. Nie zmienia prefiksów zainstalowanych
gier. Wykorzystany lokalny GE-Proton 11 zawiera bibliotekę ICU wymaganą przez
Qt 6.11; starszy Wine 10 jej nie udostępniał. Biblioteki `libvkd3d*.dll`
z GE-Proton 11 skopiowano do `system32` tylko tego prefiksu. Nie są częścią
paczki gry dla Windows.

```bash
env WINEPREFIX="$PWD/build/windows/prefix" WINEDEBUG=-all \
    WINEDLLOVERRIDES='winemenubuilder.exe=d' PYTHONUTF8=1 \
    "$HOME/.local/share/Steam/compatibilitytools.d/GE-Proton11-11-x86_64/files/bin/wine" \
    'C:\Python312\python.exe' scripts/build.py --platform-output
```

Na prawdziwym Windowsie wystarczy zainstalować zależności w Pythonie i uruchomić
`python scripts/build.py --platform-output` bez Wine.

Instalatory pobrano z oficjalnych źródeł: [Python 3.12.10](https://www.python.org/downloads/release/python-31210/)
oraz [Microsoft Visual C++ Runtime](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist).
PyInstaller działa w interpreterze platformy docelowej; nie jest kompilatorem
krzyżowym ([dokumentacja](https://pyinstaller.org/en/stable/)).

## Pliki lokalne i repozytorium

Kod, zasoby, testy oraz dokumentacja trafiają do repozytorium. `.venv/`,
`build/`, `dist/`, `test-artifacts/` i lokalne pliki konfiguracyjne są ignorowane.
Logi bieżącego budowania: `test-artifacts/build-linux.log` oraz
`test-artifacts/build-windows.log`. Zrzuty gotowych aplikacji:
`test-artifacts/packaged-linux-battle.png` i
`test-artifacts/packaged-windows-battle.png`.
