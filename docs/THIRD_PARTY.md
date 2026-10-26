# Materiały i zależności

## Dostarczone materiały

`Game_Design.md`, `karty-front/*.png`, `karty-rewers.png`: materiały dostarczone do projektu przez użytkownika. Nie zmieniono oryginalnych grafik ani treści dokumentu. To nie jest deklaracja nowej licencji ani przeniesienia praw do wizerunków, ilustracji i znaków. Zastosowanie tych materiałów w dystrybucji pozostaje na zasadach uzgodnionych przez ich właścicieli.

## Zależności

- Python: PSF License - https://docs.python.org/3/license.html
- Qt / PySide6 / Shiboken6: LGPLv3/GPLv3 lub licencja komercyjna, zależnie od modułu i użytej dystrybucji - https://doc.qt.io/qtforpython-6/licenses.html
- PyInstaller (narzędzie budowania): GPL z wyjątkiem dotyczącym bundlowanych aplikacji - https://pyinstaller.org/en/stable/license.html
- pyinstaller-hooks-contrib oraz altgraph: licencje dostępne w dystrybucjach narzędzi budujących.

Pakiet aplikacji używa Qt Core/Gui/Widgets/Qml/Quick/QuickControls2/Multimedia. Biblioteki są dynamiczne, w folderze pakietu, a nie statycznie linkowane do kodu gry. Przed publicznym wydaniem dołącz właściwe teksty licencji dystrybuowanych zależności i wymagane informacje o ich źródłach. Podpisy/certyfikaty wydawcy nie są przechowywane w repozytorium.

Font jest wybierany przez Qt z systemu użytkownika. Dźwięki interfejsu i kart są syntezowane lokalnie przez `tabota/audio.py`.

## Muzyka dostarczona przez użytkownika

Folder `music/`: 26 plików MP3 z przekazanego `Music.zip`: cztery motywy ogólne `M01–M04`, 20 motywów pojedynków `Stage01–Stage20` oraz dwa dżingle `X02/X03`. Nazwy uporządkowano, nagrań nie zmodyfikowano. Projektowy opis przeznaczenia utworów pochodzi z przekazanego pliku `docs/OST_PROMPTS.md` (kopia przekazanego dokumentu).

**Nie potwierdzono praw do komercyjnej dystrybucji** ani warunków konkretnego planu Suno. Do publikacji niezbędna jest weryfikacja uprawnienia właściciela projektu do wykorzystywania i redystrybucji każdego nagrania, a także ewentualnych wymaganych atrybucji. Sam plik promptów nie jest licencją na muzykę.

Qt Multimedia może wymagać na systemie docelowym dostępnego backendu dekodowania MP3; przed wydaniem sprawdź dekodowanie oraz pętle na wszystkich trzech platformach.
