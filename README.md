# Karty TABOta: WSZYSCY DO BANA! - Puchar PROPLAYERA

Jednoosobowa gra karciana offline na Linuxa, Windowsa i macOS. Python + Qt Quick (PySide6), bez przeglądarki, konta, serwera i telemetrii. Wykorzystuje wszystkie dostarczone ilustracje oraz ten sam `karty-rewers.png` dla każdej zakrytej karty.

Najnowsza iteracja UI: własny kursor (normal/grab/click), podgląd hover także przy wymianie, szczegóły kart na stole tylko po kliknięciu, stały odcień koła i mocniejsze efekty dźwiękowe. Panel rytuału pokazuje wyłącznie już użyty rytuał.

Aktualne poprawki 12 zgłoszeń: [opis zmian i wyniki kontroli](docs/FIXES_2026-10-26.md).
Audyt fabuły NORMAL z 27.10.2026: [10 000 walk, wyniki wszystkich pojedynków i poprawka oznaczenia Ochrony](docs/STORY_AUDIT_2026-10-27.md).
Starsze sekcje „Aktualizacja” poniżej są historią prac; bieżące zachowanie opisuje ten raport.

## Licencja

Kod projektu: [MIT](LICENSE), Copyright (c) 2026 krupar101. Możesz używać,
modyfikować i rozpowszechniać kod, także komercyjnie, zachowując informację
copyright i tekst licencji. Oprogramowanie jest dostarczane bez gwarancji
na warunkach MIT.

Grafiki, muzyka i inne dostarczone materiały nie są objęte MIT na kod.
Zależności i fonty zachowują własne licencje. Zobacz [zakres licencji](LICENSE_SCOPE.md)
oraz [informacje o materiałach i zależnościach](docs/THIRD_PARTY.md).

## Uruchomienie ze źródeł

Potrzebujesz 64-bitowego Pythona 3.10–3.14. Do budowania zalecany Python 3.12. Otwórz terminal w katalogu projektu.

Linux / macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

Jeśli Qt zgłasza problem ze sterownikiem GPU, uruchom `main.py --software` (w gotowej paczce: `./TABOt --software`). Na minimalnej instalacji Ubuntu potrzebne mogą być pakiety `libstdc++6 libpulse0 libegl1 libopengl0 libxcb-cursor0 libxkbcommon-x11-0 libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 libxcb-xinerama0`. Paczka Linuksa korzysta z systemowej biblioteki `libstdc++.so.6`, aby nie blokować ładowania nowszych sterowników Mesa/EGL. Gra skaluje układ do okna; zalecane co najmniej 1280×720.

## Co jest w grze

Przegląd UI, dźwięków i balansu z 26.10.2026: [wyniki i procedury testowe](docs/PLAYTEST.md).
Tło reaguje na muzykę delikatnym widmem i ruchem punktów/okręgów; wyciszenie
muzyki lub ograniczone animacje wyłączają wizualizację. Efekty obejmują także
najeżdżanie na karty, przyciski, tasowanie, cofanie i rytuały.

- Kampania Puchar PROPLAYERA: 20 turniejowych wyzwań, cztery akty, nowe dialogi, gotowe talie, pieczątki zwycięstw i Kronika Turnieju (TaboLOG).
- Samouczek: w turach 1–3 okienka prowadzą przez wybór karty, strefy i zakończenie tury, blokując niezgodne działania; od tury 4 gra daje samodzielnie podejmować decyzje.
- 52 jednostki, 24 wydarzenia, trzy rodzaje żetonów; wszystkie zdolności kart, statusy, Rytuał 20:30, reguły 20 rozpraw i warianty HARD.
- Ukryte plany, jawny podgląd własnych ruchów, cofanie, wybór konkretnych celów, naprzemienne ujawnianie i trzy poziomy AI.
- PROPLAYER z draftem 24 → 18, swobodne pojedynki, kolekcja z zakrytymi nieodkrytymi kartami i wskazówkami odblokowania, filtry, krzywa kosztów i osiem presetów talii.
- Wróżby 1/3/5 z pełnych 52 kart, tasowanie i odcięcie, animowane odkrywanie, autorskie interpretacje, notatki, historia oraz import/eksport JSON.
- Trzy sloty kampanii, zapis bieżącej tury i niezatwierdzonego planu, kopie zapasowe, osobne dane wróżb.
- Oryginalne karty w pełnym podglądzie, animowane reakcje, 26 nagrań OST, syntetyczne dźwięki kart, pełny ekran, tryb ograniczonych animacji.
- Muzyka: 4 motywy ekranów, unikalny motyw każdej z 20 rozpraw i dwa dżingle wyniku; płynne przenikanie przy przełączaniu scen, niezależne suwaki muzyki i dźwięków w Opcjach.
- Nie-tutorialowe rozprawy: modalny WARUNEK ROZPRAWY → jego potwierdzenie → wymiana kart → właściwa rozgrywka. Kolejność zapisywana razem z pojedynkiem.

Sterowanie podczas pojedynku: **klik górnej połowy karty** → wybór → klik strefy → wybór celu. **Najechanie na dolną połowę „SZCZEGÓŁY”** pokazuje mniejszy, wyśrodkowany podgląd z ilustracją i opisem. Podgląd nie przechwytuje fokusu i znika po odsunięciu kursora z obszaru „SZCZEGÓŁY”. Przeciąganie jest alternatywą. Prawy klik lub `I` na karcie również otwiera powiększenie, `Tab` / `Shift+Tab` przechodzą po kontrolkach, `Enter` / `Spacja` aktywują, `Esc` zamyka podgląd lub otwiera pauzę, `F11` przełącza pełny ekran. Efekty dobierania nie pozwalają dopisywać ruchów do zatwierdzonego planu.

## Ścieżka dźwiękowa

Pliki w `music/` zostały dostarczone w `Music.zip` i są ładowane z dysku, bez internetu. `M01` to menu i pomoc/ustawienia, `M02` to mapa/briefing/wynik, `M03` to kolekcja i budowanie talii, `M04` to wróżby i historia. `Stage01.mp3`–`Stage20.mp3` odpowiadają rozprawom 01–20; pauza nie przełącza utworu pojedynku. `X02.mp3`/`X03.mp3` są dżinglami zwycięstwa/porażki. Brak dostarczonych plików `X01`/`X04`, więc sygnały rytuału i odkrycia wróżby korzystają z istniejących efektów syntetycznych.

Przejścia muzyki trwają zwykle ok. **1,4 s** i łączą dwa odtwarzacze; przejście do wyniku jest krótsze (**0,32 s**), a podkład podczas dżingla jest automatycznie ściszany i łagodnie przywracany. Oba suwaki w **Opcjach** reagują bez restartu gry i są zapisywane w `settings.json`. Starsze ustawienia działają bez migracji ręcznej. Pętle plików MP3 odtwarzane są przez Qt - końcówki samych nagrań nie zostały jeszcze ręcznie przygotowane do idealnie bezszwowego zapętlenia.

**Przed publiczną dystrybucją** sprawdź prawa do nagrań i warunki licencyjne użytego generatora, a także odsłuchaj wszystkie utwory pod kątem niechcianych wokali i poziomów głośności. Szczegóły: `docs/THIRD_PARTY.md`.

## Budowanie aplikacji dla trzech systemów

Pakiety buduje się **osobnymi interpreterami dla każdego systemu**. Linuxowy Python nie wyprodukuje poprawnego `.exe` ani `.app` przez samo przełączenie flagi. Windowsowy Python i PyInstaller mogą działać lokalnie pod Wine; taki build należy dodatkowo sprawdzić na prawdziwym Windowsie. Konfiguracja projektu i kod są wspólne.

Z aktywnym środowiskiem wirtualnym:

```bash
python -m pip install -r requirements.txt "pyinstaller>=6.16,<7"
python scripts/build.py
```

Opcja `--platform-output` rozdziela wyniki na `dist/linux-x86_64/TABOt/`
i `dist/windows-x86_64/TABOt/`, dzięki czemu lokalne buildy nie nadpisują się:

```bash
python scripts/build.py --platform-output
```

Skrypt zawsze uruchamia najpierw testy. Zależności i katalogi `build/`, `dist/`
oraz `test-artifacts/` nie są wysyłane do repozytorium.

Wynik:

| System kompilacji | Aplikacja |
| --- | --- |
| Linux x86_64 | `dist/TABOt/TABOt` |
| Windows x64 | `dist/TABOt/TABOt.exe` |
| macOS (architektura maszyny budującej) | `dist/TABOt.app` |

Przenoś **cały folder** z aplikacją, łącznie z `_internal`. Komputer odbiorcy nie potrzebuje Pythona ani dostępu do sieci. Na macOS zachowaj bundle `.app`. Podpisywanie Windows/macOS i notarization wymagają własnych certyfikatów wydawcy; projekt ich nie zawiera.

Gotowy workflow `.github/workflows/build.yml` buduje wszystkie trzy platformy po ręcznym uruchomieniu albo tagu `v*`. Artefakty pobierzesz z uruchomienia GitHub Actions. Workflow nie był uruchamiany z tego środowiska i nie publikuje automatycznie wydań. macOS ARM i macOS Intel wymagają odpowiednich runnerów, jeżeli potrzebujesz obu architektur.

Zastosowano folderowy bundle z dynamicznymi bibliotekami Qt. Informacje o zależnościach/licencjach: [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md). Dokumentacja narzędzi: [Qt for Python - wdrażanie](https://doc.qt.io/qtforpython-6/deployment/index.html), [PyInstaller - użycie](https://pyinstaller.org/en/stable/usage.html).

## Testy

```bash
python -m unittest discover -s tests -v
python scripts/check_ui.py
python scripts/simulate.py --games 100 --difficulty normal
```

Testy rdzenia nie wymagają Qt ani ekranu. `check_ui.py` uruchamia rzeczywisty Qt Quick, sprawdza ładowanie wszystkich ekranów i zapisuje PNG do `test-artifacts/`. Testy integracji interfejsu są w `scripts/check_interactions.py`. Stan przeprowadzonych kontroli: [docs/QA.md](docs/QA.md). Balans nadal wymaga ludzkich playtestów; statystyczny raport nie jest deklaracją idealnej równowagi.

## Zapisy i prywatność

- Linux: `$XDG_DATA_HOME/Tabot`, domyślnie `~/.local/share/Tabot`.
- Windows: `%LOCALAPPDATA%/Tabot`.
- macOS: `~/Library/Application Support/Tabot`.

Dane ze starych folderów `tabota` / `TABOta` są kopiowane przy pierwszym uruchomieniu do `Tabot`; oryginał pozostaje kopią zapasową.

`campaign.json`, `readings.json` i `settings.json` to oddzielne pliki. Zapis jest atomowy i zachowuje poprzednią wersję `.bak`. Gra próbuje odzyskać uszkodzony zapis z backupu i pokazuje ostrzeżenie. Nie zapisuje pytań w logu meczu. Opcje pozwalają eksportować/importować dane. Import historii scala wpisy po ID, import kampanii wymaga potwierdzenia zastąpienia slotów. `TABOTA_DATA_DIR` pozwala wskazać osobny katalog, np. do testów lub przenośnego zapisu.

## Architektura i dalsza praca

`tabota/content.py` odczytuje statyczne tabele z dostarczonego `Game_Design.md` (plik jest częścią paczki); `engine.py` zawiera niezależny silnik, AI i draft; `storage.py` zapis/odczyt i wróżby; `bridge.py` połączenie z Qt; `ui/` ekrany QML; `audio.py` lokalny syntezator. Kod zasad nie importuje Qt. Ilustracje źródłowe nie są modyfikowane.

Istotne rozstrzygnięcia niejednoznaczności i różnice względem GDD: [docs/DECISIONS.md](docs/DECISIONS.md). Źródłowy dokument pozostaje nienaruszony.

## Zmiany interfejsu i języka

- ⚡ **Energia** widoczna tuż nad kartami gracza, nie przy przeciwniku; ⚡ oznacza także koszt każdej karty.
- ✦ **Moc** jest wyróżniona ikoną na kartach, punktacji stref, w podglądzie i w krótkim samouczku.
- Wymiana na początku pojedynku wyjaśnia krok po kroku zaznaczanie do 2 kart; zaznaczone mają napis **DO WYMIANY**. Zero zaznaczonych = zachowaj rękę.
- Główny przycisk rozgrywki to **Zakończ turę**: ujawnia oba plany i wykonuje działania. Nie zmienia mechaniki jednoczesnych planów.
- Zakładka **Zasady** zawiera krótkie, proste kroki, a reguły zaawansowane można rozwinąć przyciskiem.
- W tekstach przyjęto **TABOt** jako nazwę w formie podstawowej oraz **karty TABOta**; tytuł gry to **Karty TABOta: WSZYSCY DO BANA!**, a nazwa kampanii to **Puchar PROPLAYERA**. Dane techniczne rozgrywki pozostały bez zmian, natomiast rozdziały fabularne w `Game_Design.md` zostały zaktualizowane.

## Usprawnienia dostępności i tutorialu - kolejna iteracja

- Przeciągana karta unosi się nad **całym** interfejsem stołu (nawet poza ręką) zamiast chować pod przyciętym widokiem. Działa też w trybie ograniczonych animacji.
- Nieodblokowane karty mają w kolekcji wyłącznie **rewers, numer i warunek odblokowania**. Nie ma podglądu ilustracji ani parametrów. Po zdobyciu karta staje się w pełni widoczna.
- Każda poprawna talia wymaga co najmniej jednej jednostki za ⚡ 1. Pierwsze pięć kart (także po wymianie) zawsze pozwala wykonać ruch w turze 1, bez kopiowania czy tracenia kart z talii.
- Pierwsze trzy tury samouczka są teraz interaktywnym, obowiązkowym treningiem z okienkami, podświetleniem i kontrolą dozwolonych działań. Od tury czwartej gracz ćwiczy samodzielnie.
- **Zgodność starych zapisów:** schemat zapisu się nie zmienił. Presety utworzone przed wprowadzeniem zasady taniej jednostki da się nadal wczytać; przed użyciem należy je poprawić, jeśli nie spełniają nowego warunku.

W tym środowisku nie udało się uruchomić testów widoku Qt (brak zgodnej biblioteki PySide6). Testy Pythona i kontrakty komponentów QML zostały uruchomione; sprawdzenie przeciągania na ekranie pozostaje konieczne.

## Poprawa animacji kart i audyt logów - 26.10.2026

- **Jedna karta zamiast dwóch:** `Battle.qml` przenosi oryginalny komponent `handCard` nad przycinaną rękę (`ParentChange`). Najechanie **nie** tworzy już drugiego niezależnego komponentu z własną animacją. Ten sam komponent jest też przesuwany podczas przeciągania.
- **Nakładka „SZCZEGÓŁY”:** płynne zanikanie/pojawianie (200 ms lub 40 ms przy ograniczonych animacjach) po najechaniu **gdziekolwiek** na kartę; kliknięcie górnej połowy wybiera, a dolnej otwiera szczegóły. Prawy klik i klawisz `I` pozostają dostępne.
- **QML podczas zamykania:** w `main.py` najpierw usuwane jest drzewo obiektów Qt Quick, a dopiero potem silnik QML i jego kontekst. Zapobiega to odwołaniom do `api.state` po zniszczeniu `api`.
- **Audyt logu użytkownika:** `Battle.qml:308` zgłaszało przypisanie `undefined` do `bool` z kopii karty; ta ścieżka została usunięta. Seria `TypeError: Cannot read property 'state' of null` pasowała do błędnej kolejności zwalniania zasobów. Komunikaty `mp3float` o znacznikach czasu i `qt.multimedia.ffmpeg` nie są wyjątkami logiki rozgrywki; to komunikaty od dostarczonego przez środowisko dekodera.

Testy bez Qt sprawdzają kontrakty warstw, obsługę kliknięć i porządek zamykania. **Wizualne zachowanie `ParentChange` i czystość logu po wyjściu należy potwierdzić uruchomieniem `python scripts/check_interactions.py` na maszynie z działającym Qt.**


Test interakcji nowej warstwy hover na działającym Qt:

```bash
python scripts/check_hover.py
```

## Aktualizacja: płynne przejścia UI i karty na stole - 26.10.2026

- **Karty w ręce:** półprzezroczysta nakładka „SZCZEGÓŁY” jest teraz wewnątrz tego samego elementu `motion` co karta. Przejmuje jej unoszenie, obrót, powiększenie i animację wejścia - nie pozostaje statyczna przy podnoszeniu karty. Pojawia się niezależnie od części najechanej karty; tylko miejsce kliknięcia określa akcję.
- **Karty już wystawione:** na obu stronach stołu kliknięcie pokazuje szczegóły. Karty gracza leżące w strefach nie mają już podziału góra/dół ani nakładki „SZCZEGÓŁY”. Puste miejsca nadal służą do wybrania strefy.
- **Fade ekranów:** bieżący ekran znika przez 150 ms, nowy pojawia się przez 210 ms. Zmiana źródła `Loader` następuje pomiędzy animacjami; w tym czasie nie można przypadkiem aktywować starego ekranu. Dla ustawienia „Zmniejszone animacje” oba etapy trwają po 20 ms.
- **Fade okienek:** podgląd karty, wybór celu, potwierdzenie, powiadomienie, warunek rozprawy, wymiana ręki i panel tutorialu otrzymały wspólną animację przezroczystości (190 ms / 35 ms). Podczas zanikania okna nie przechwytują wejścia. Potwierdzenie warunku rozprawy musi skończyć znikać **przed** pojawieniem się okna wymiany.
- **Pozostałe przejścia:** rozwijanie dodatkowych zasad, widok „Plan / Log meczu” i elementy fazy wróżby również otrzymały proste zanikanie; tutor dodatkowo łagodnie przesuwa się między kartami a planszą.
- W czasie wygaszania strony zachowywany jest ostatni pełny stan rozgrywki lub wróżby, nawet jeśli adapter już usunął mecz.

Testy bez Qt: `python -m unittest discover -s tests -v`. Testy graficzne Qt: `python scripts/check_fades.py`, `python scripts/check_hover.py`, `python scripts/check_interactions.py`. **Nie udało się uruchomić testów renderowania w dostępnym środowisku z powodu braku PySide6.**

## Optymalizacja płynności po „Zakończ turę” - 26.10.2026

- **Szczegóły karty** otwierają się i zamykają z Fade **150 ms / 150 ms**, także po kliknięciu karty na stole. Otwarcie/zamknięcie korzysta z niewielkiej aktualizacji danych modala, zamiast przebudowywania planszy, kolekcji i kampanii.
- **AI + rozstrzyganie**: wątek roboczy przygotowuje plan rywala, wylicza legalne skutki obu planów i buduje klatki odsłaniania; interfejs otrzymuje dopiero gotowy wynik. Gracz nie może pominąć animacji, zanim wynik rzeczywiście istnieje.
- **Lżejsze animowanie tury**: `api.battleBoard` ma własny sygnał `boardChanged`. Podczas każdej klatki ruchu aktualizuje się wyłącznie stan stołu; nie emituje się globalnego `changed`, które uprzednio powodowało ponowne wiązanie ekranu, panelu szczegółów, mapy, kolekcji, historii wróżb i synchronizacji muzyki. Obliczanie przydatności kart i rytuałów jest pomijane podczas samej animacji (są wtedy niedostępne).
- **Reguły i zapisy pozostają takie same**. `prepare_turn()` to funkcja silnika bez zależności od Qt, porównywana w testach z wcześniejszym wykonaniem sekwencyjnym na 20 rozprawach i obu poziomach trudności.

Sprawdzenie na Twojej maszynie:

```bash
TABOTA_PROFILE_TURNS=1 python3 main.py
```

W terminalu pojawią się czasy obliczenia AI i przygotowania tury, odstępy pomiędzy odsłanianymi ruchami oraz koszt powiadomienia QML. Ostatni pomiar **nie obejmuje całego renderowania GPU**; do potwierdzenia płynności potrzebny jest test w działającym Qt. Dodatkowo: `python scripts/check_fades.py`, `python scripts/check_hover.py`, `python scripts/check_interactions.py`.


## Fabuła Pucharu PROPLAYERA - aktualizacja 26.10.2026

Tabo pokazuje na streamie fizyczne Karty TABOta, a ELTaboBot traktuje jego przechwałki jako zgłoszenie do 20-wyzwaniowego turnieju. Nagrodą jest Złoty Taboret oraz tytuł PROPLAYERA. Bot jest organizatorem i finałowym rywalem, nie antagonistą niszczącym widzów. Kronika Turnieju (TaboLOG) zapisuje pieczątki i anegdoty. Nowe wprowadzenie, 20 kontekstów pojedynków, 120 linii dialogowych, przejścia fabularne między aktami i alternatywny epilog HARD znajdują się w projekcie i aktualnym `Game_Design.md`.

Zasady, kolejność przeciwników, talie, nagrody i stan zapisów pozostały bez zmian. Uwaga: opcjonalne wyzwanie TABO kontra TABO oraz wyjątkowy rewers nie są jeszcze zaimplementowane. Oryginalne MP3 zachowano bez modyfikacji; nowe teksty OST to wskazówki do ewentualnej przyszłej rearanżacji, nie nowe nagrania.

Specyfikacja nowego lore: `docs/LORE_BRIEF.md`.

## Czytelność wyboru celu i zapisu myślników (26.10.2026)

- Ekran "Wybierz cel efektu": opis i tytuł są w osobnej kolumnie po lewej, a miniatura zagrywanej karty po prawej. Lista celów zaczyna się dopiero pod niższym z tych elementów.
- Wysokość każdego kafla celu wynika z rzeczywistej wysokości graficznych kart. Dwa typowe cele mieszczą się w powiększonym panelu; większa liczba celów jest przewijana.
- W tekstach interfejsu, dialogach, nazwach kart i dokumentacji długie myślniki zastąpiono znakiem `-`. Parser dokumentu GDD używa tego samego separatora. Reguły pojedynków, statystyki, talie i odblokowania nie zostały zmienione.
- Wizualna kontrola QML musi zostać wykonana na komputerze z PySide6, szczególnie dla efektów z jednym, dwoma i wieloma celami oraz długimi opisami.

### Optymalizacja przeciągania kart

Podczas gestu przeciągania wykonywana jest tylko animacja QML; obliczenia silnika
następują dopiero po upuszczeniu karty na jedną z legalnych stref. Zmiany planu
zapisują się automatycznie po 650 ms bezczynności lub natychmiast przy
zakończeniu tury, zmianie ekranu i wyjściu. Komputer z PySide6 może wykonać
`python scripts/check_drag.py`, aby sprawdzić ścieżkę interakcji i poznać
orientacyjne opóźnienia dostarczenia zdarzeń myszy.

## Poprawa oznaczeń warunku litery A (26.10.2026)

W wyzwaniu 03 znaczniki `A` i `BEZ A` są teraz umieszczone przy górnej
prawej **krawędzi** karty, zamiast zasłaniać tytuł lub ilustrację. Karty
na stole (52 i 67 px) mają mniejszą wersję nad kosztem, a karty w ręce
mają czytelny napis na prawym brzegu. Znacznik nie wychodzi poza szerokość
karty, więc nie zakrywa sąsiednich jednostek. Ikona Ochrony ma osobną
pozycję, gdy występuje razem ze znacznikiem; czerwony X Wyciszenia
pozostaje celowo widoczny przez ilustrację, aby statusu nie przeoczyć.

Układ nie zmienia zasad, kosztów, Mocy ani warunków efektów. Dodatkowy test
`tests/test_badge_placement.py` sprawdza geometrię dla szerokości
52, 67, 90, 98, 120, 132 i 388 px. Ostateczna ocena wizualna nadal wymaga Qt.
