# Weryfikacja po zmianach interfejsu - 25.10.2026

## Testy przeprowadzone

- Testy jednostkowe silnika, logiki tutorialu, legalności otwarcia i zapisu: **50/50 zaliczone**, w tym regresja 20 rozpraw, wymiany ręki, draftu i kompatybilności starych presetów oraz kontrakty QML.
- Symulacja AI-vs-AI: **80/80 ukończonych pojedynków**, bez błędów sprawdzanych warunków; wyniki w `test-artifacts/simulation.json`.
- Kompilacja składniowa Pythona: **bez błędów**.

Testy automatyczne nie potwierdzają jeszcze subiektywnej czytelności i ergonomii planszy.

## Testy wymagające PySide6 / Qt Quick

W aktualnym środowisku nie można ich wykonać: brak dostępnego PySide6, a binaria PySide6 z przekazanego archiwum wymagają GLIBC 2.43 zamiast dostępnej GLIBC 2.41. Instalacja z sieci również jest niedostępna.

Na zgodnej maszynie uruchom:

```bash
python -m pip install -r requirements.txt
python scripts/check_ui.py
python scripts/check_interactions.py
```

Po testach automatycznych sprawdź ręcznie:

- Wymiana 0, 1 i 2 kart, anulowanie zaznaczenia, reakcja na próbę wybrania trzeciej. Każdorazowo musi pozostać w ręce przynajmniej jedna jednostka za ⚡ 1.
- Dostępność ⚡ przy ręce i ⚡ kosztu / ✦ Mocy na jednostkach, wydarzeniach, planszy, przy 1280×720 i przy skalowaniu.
- „Zakończ turę” z pustym oraz wieloakcyjnym planem i poprawne przejście do kolejnej tury.
- Zasady w zakładce Pomoc, rozwijanie szczegółów i nawigacja po TaboLOGu.
- **Przeciąganie:** powoli przeciągnij kartę nad górną część planszy i nad panel po prawej. Obraz musi być zawsze na wierzchu; upuszczenie poza strefą nie może jej zagrać. Sprawdź też przy ograniczonych animacjach.
- **Kolekcja:** niezablokowane fronty są dostępne, nieodblokowane pokazują wyłącznie rewers, numer i pełny warunek (także po najechaniu); klik/prawy klik nie może ujawnić szczegółów. Po nagrodzie ta sama karta musi odkryć front.
- **Tutorial:** w turach 1–3 wymagane są po kolei właściwa karta, strefa i zatwierdzenie; testuj kliknięcie i przeciąganie innych kart, złe strefy, pusty plan, cofnięcie oraz wznowienie zapisu. W turze 4 nie może być blokady innych legalnych ruchów.
- Ekrany planszy, pomocy i kolekcji na Windows, Linux, macOS oraz na małym ekranie, bez zasłoniętych elementów.

## Ryzyka i zakres niepotwierdzony

Brak końcowych testów produkcyjnych 20-rozprawowej kampanii, niezależnych playtestów, 10 000 prób na parę archetypów, podpisów aplikacji oraz rzeczywistych buildów i prób instalacji na Windows/macOS. Brak wersji web/PWA, odnotowany w `docs/DECISIONS.md`.


## Iteracja OST / podgląd kart / warunek rozprawy (26.10.2026)

- **54 testy odkryte:** 53 przechodzą; **1 test integracyjny adaptera jest pominięty**, ponieważ PySide6 nie jest dostępny. Sprawdzono deterministyczne przypisanie 26 utworów, komplet plików, odczyt starych ustawień głośności i kontrakty interfejsu.
- Wszystkie 26 MP3 posiada poprawny strumień odczytywany przez `ffprobe`; długości 7–208 s. To **nie jest test odsłuchowy** ani potwierdzenie płynności przejść w Qt.
- `python -m compileall -q tabota main.py scripts tests` - kod Pythona kompiluje się bez błędów.
- Brak środowiska z PySide6/Qt: **nie wykonano** zrzutów ekranowych, symulowanego kliknięcia w górną/dolną połowę ani testu z odtwarzaczem. Próba instalacji PySide6 z indeksu pakietów nie powiodła się z powodu braku połączenia sieciowego.

**Ręczny scenariusz akceptacyjny** po `pip install -r requirements.txt`:

1. Menu → mapa → kolekcja → wróżby → pojedynek 01 → pojedynek 20. Sprawdź przypisane motywy, brak przerwania podczas przełączenia, brak resetu muzyki na kliknięciach w obrębie ekranu i brak wycieku dwóch ścieżek po szybkim przejściu tam i z powrotem.
2. Opcje: wycisz/włącz muzykę, przesuń suwak podczas odtwarzania, sprawdź niezależny suwak SFX, wyjdź i włącz ponownie aplikację - ustawienia muszą pozostać zachowane.
3. W nie-tutorialowej rozprawie sprawdź okno **WARUNEK ROZPRAWY**. Nie powinno być aktywnej wymiany pod spodem. Potwierdź → sprawdź wymianę 0–2 kart → rozpocznij. Zakończ proces przed potwierdzeniem i wznowij zapis; przyciski tury nie mogą omijać okna. Po potwierdzeniu i wznowieniu **okno nie może się powtórzyć**.
4. Karty w ręce: najedź na skrajne i środkowe (także przy przewiniętej ręce). Cała górna krawędź i znaczek ⚡ muszą być widoczne nad UI. Kliknij górną połowę - wybór karty. Najedź na dolną - „SZCZEGÓŁY” półprzezroczyście; klik dolnej połowy otwiera pełen podgląd. Testuj też przeciąganie od góry i od dołu oraz prawy klik.
5. Zajrzyj do 2–3 pojedynków po załadowaniu starszego zapisu. Nie może się pojawić nowy modal w połowie rozgrywki. Testuj 1280×720 i ekran pełny.
6. Odsłuchaj dżingle X02 i X03 oraz każdy motyw Stage01–20, w tym koniec pętli. `X03.mp3` trwa około 12 s (dłużej niż sugerowane 4–7 s w planie OST) - ocenić, czy należy go skrócić przed wydaniem.

Uruchom ponadto `python scripts/check_ui.py` i `python scripts/check_interactions.py` na środowisku z działającym Qt; skrypt interakcji został dostosowany do podziału karty na połowy oraz kolejności okien na starcie.


## Przegląd błędów z logu gracza i animacji (26.10.2026)

| Wpis w logu | Ocena | Działanie |
| --- | --- | --- |
| `Battle.qml:308:9: Unable to assign [undefined] to bool` | **Błąd QML** w poprzedniej wersji | Usunięto osobną kopię karty, która bindowała `selected || exchange` bez wartości domyślnej. Nowe komponenty mają wartości logiczne. |
| `Main.qml`, `Card.qml`, `Menu.qml`: `Cannot read property 'state' of null` | **Błędy QML**, widoczne pod koniec sesji | Zmieniono kolejność niszczenia obiektów Qt: najpierw scena QML, potem silnik; API pozostaje przy życiu podczas usuwania sceny. |
| `[mp3float] Could not update timestamps for skipped/discarded samples` | Ostrzeżenia dekodera FFmpeg MP3, nie wyjątek logiki gry | Pliki pozostają oryginalne; sprawdzić czy nie występują słyszalne przerwy na granicach pętli. |
| `qt.multimedia.ffmpeg ... nonfree and unredistributable` | Informacja o konfiguracji FFmpeg biblioteki Qt na uruchomionym systemie | Dla dystrybucji trzeba osobno sprawdzić zgodność/licencję używanego buildu FFmpeg. |
| `Stream #0:1: Video: mjpeg ... attached pic` | Okładka osadzona w tagach MP3 | Prawidłowa metadana; nie oznacza odtwarzania wideo podczas gry. |

**Nowy scenariusz graficzny:** najedź na kartę w ręce od góry, później od dołu (również w przewiniętej ręce). Przez cały czas widać dokładnie jedną kartę bez rozjazdu animacji; pod spodem nie powinien pozostać animowany duplikat. Nakładka „SZCZEGÓŁY” ma pojawić się od razu po najechaniu i płynnie rozjaśnić, nawet jeśli kursor jest w górnej połowie. Kliknięcie góra/dół zachowuje różne działania. Sprawdź też przeciąganie nad panel i powrót karty do ręki po nieudanym upuszczeniu. Po wyjściu do terminala nie powinno być `TypeError` ani `Unable to assign [undefined] to bool`.

**Testy bez Qt:** 57 testów odkrytych, 56 przechodzi, 1 pominięty (integracyjny PySide6). Rzeczywiste uruchomienie Qt i odsłuch nie są potwierdzone w tym środowisku.


**Nowy test integracyjny Qt:** uruchom `python scripts/check_hover.py`. Sprawdza na działającym Qt ponowne rodzicowanie *tej samej* karty na najechaniu, liczbę komponentów kart, przezroczystość nakładki nad górną i dolną połową, lewy klik góra/dół oraz powrót karty do ręki po opuszczeniu obszaru. Wymaga PySide6 (w tym środowisku **nieuruchomiony**).

## Akceptacja płynnych przejść i kliknięć - 26.10.2026

- 63 testy znalezione przez `unittest`: **62 zaliczone, 1 pominięty** (wymaga Qt). Dodatkowe testy kontraktowe sprawdzają położenie nakładki w animowanym obiekcie karty, brak podziału kliknięcia na kartach na stole oraz kolejność fade ekranu i okien.
- Sprawdzono kompilację składni Python; testy QML renderujące rzeczywisty interfejs są nadal wymagane.
- Na komputerze z PySide6 uruchom `python scripts/check_fades.py` oraz `python scripts/check_hover.py`.
- Test manualny: (1) najedź na kartę w ręce od góry; na półprzezroczystej dolnej połowie napis „SZCZEGÓŁY” ma poruszać się i skalować **razem z kartą**; (2) kliknij w obie połowy; (3) kliknij własną i wrogą jednostkę na planszy - za każdym razem otrzymujesz podgląd bez nakładki; (4) otwieraj i zamykaj kilka razy podgląd karty, potwierdzenia, zasady i ustawienia; (5) przejdź przez warunek rozprawy i wymianę, upewniając się, że nie widać obu okien jednocześnie; (6) włącz w opcjach „Zmniejszone animacje” i ponów test; (7) zamknij aplikację, upewnij się, że nie pojawiają się błędy QML w logu.

## Wydajność i szybkie szczegóły - 26.10.2026

- Testy `test_turn_performance.py` porównują końcowe stany i wszystkie klatki `prepare_turn()` z poprzednim, sekwencyjnym wykonaniem (20 pojedynków × 2 poziomy × 3 tury), weryfikują niewzruszoność wejścia i tutorial.
- Animacja szczegółów: `tabotaDetailDialog.fadeDuration` = 150 ms, każda strona przejścia osobno. Test ręczny: klikaj kolejne karty szybko, także podczas zanikania, sprawdź, czy zawartość nie miga.
- Profilowanie na Linuksie: `TABOTA_PROFILE_TURNS=1 python3 main.py`; zwracaj uwagę na duże opóźnienia odstępów między klatkami względem 520 ms i koszt sygnału planszy. Jest to diagnostyka, **nie pomiar FPS GPU**.
- Bez działającego Qt w aktualnym środowisku nie można jeszcze potwierdzić braku mikroprzycięć na docelowym sprzęcie.


## Testy nowej fabuły - 26.10.2026

- Potwierdź w grze: prolog zgłoszenia do Pucharu; Nysmo w poczekalni; wyzwania 05 / 10 / 15 z krótką puentą; przejście do 16; wejście do 20 i finałowe zakończenia NORMAL / PROPLAYER.
- W Kronice Turnieju wpisy powinny odpowiadać nowym sytuacjom i dialogom.
- Sprawdź, że wróżby i zapis starszej kampanii zachowują niezależność od nowej narracji.
- Technicznie weryfikować niezmienność 20 talii, parametrów 76 kart, szablonu seedów i funkcji silnika.

## Ekran wyboru celu - geometria i typografia (26.10.2026)

1. Otwórz kartę Tabarzak - Brat Krwi przy dwóch własnych celach w strefie ZAPLECZE. Nagłówek, opis efektu i ilustracja zagrywanej karty nie mogą na siebie nachodzić.
2. Każda karta celu powinna w całości mieścić się w swoim kaflu. Przy dwóch celach obie opcje powinny być widoczne bez przewijania przy standardowym oknie.
3. Otwórz wybór celu wrogiej karty, wybór dwóch celów jednocześnie oraz wybór strefy dla Rytuału. Sprawdź ich obramowania, kliknięcia i przewijanie.
4. W trybie zmniejszonych animacji oraz po przełączeniu okna na mniejszy rozmiar sprawdź, czy przycisk Anuluj pozostaje dostępny.
5. W tekstach gry nie powinien pojawiać się znak długiego myślnika (em dash); zamiast niego używany jest zwykły łącznik `-`.

## Lekki drag & drop i opóźnienie przy upuszczaniu - 26.10.2026

- Nie uruchamiamy `selectCard()` ani odświeżania globalnego interfejsu w chwili rozpoczęcia przeciągania. Karta jest nadal **tym samym obiektem** `Card` podnoszonym nad `Flickable`; nie powstaje drugi asset.
- W czasie ruchu myszy aktualizowane są wyłącznie współrzędne tego obiektu w obrębie `Battle.qml`. Jednorazowe `mapFromItem()` przy rozpoczęciu zapamiętuje punkt chwycenia, zapobiegając skokowi karty. Możliwości zagrania w poszczególnych strefach są obliczane wraz ze stanem planszy i pokazywane bez wywoływania Pythona w ruchu.
- Upuszczenie poza trzema strefami nie wywołuje akcji silnika. Upuszczenie w strefie jest odroczone do kolejnego obiegu zdarzeń (`Qt.callLater`) - ruch myszy i zwolnienie przycisku kończą się przed aktualizacją stanu.
- W zwykłej sytuacji po zagraniu odświeżany jest tylko stan bitwy, bez przebudowy katalogu kart, TaboLOGu, mapy i historii wróżb. Wybór wielu celów nadal wyświetla graficzne okno z aktualnymi kartami.
- Zapis zmienionego planu następuje po 650 ms bez kolejnego zagrania. Wyjście, nawigacja, ręczne zatwierdzenie tury lub inne wymuszone zapisy zapisują stan od razu, więc ostatni ruch nie zostaje pominięty przy normalnym zamknięciu.
- `python -m unittest discover -s tests -q` - obejmuje też próbę prawidłowego/niedozwolonego upuszczenia karty w samouczku i odtworzenie zaplanowanego ruchu z pliku po zapisie.
- **Na maszynie z działającym PySide6** uruchomić `python scripts/check_drag.py`. Sprawdzić zarówno normalne, jak i ograniczone animacje, błędną strefę, upuszczenie poza planszą, przeciąganie z dołu karty, podgląd szczegółów i karty wymagające wyboru celu. Przy wielu kartach na stole wykonać próbę w turach 5-6. Brak lokalnego środowiska z kompatybilnym PySide6 uniemożliwia weryfikację FPS w tym kontenerze.

## Znaczniki litery A / BEZ A (26.10.2026)

1. Uruchom wyzwanie 03 i sprawdź pięć kart w ręce oraz po kilka kart obu stron na CZACIE; znacznik w prawym górnym brzegu nie może przykrywać nazwy ani `⚡`.
2. Ułóż w strefie pięć małych kart obok siebie: znacznik z jednej karty nie może nachodzić na kartę sąsiednią. Sprawdź też podniesienie / przeciągnięcie karty.
3. Sprawdź jednoczesną **Ochronę** (zielony romb) i `A` / `BEZ A` oraz **Wyciszenie** (czerwony X). Tych oznaczeń nie wolno ze sobą mylić.
4. Zagraj wyzwania 01, 02 i 04 - poza warunkiem litery A znaczniki `A` / `BEZ A` nie powinny się pojawiać.
5. Przetestuj rozdzielczości 1280x720, 1600x900 i 1920x1080 oraz opcję ograniczonych animacji.

Kontrola bez Qt: `python -m unittest discover -s tests -q` (nowy plik
`tests/test_badge_placement.py`). Położenia elementów w działającym
renderowaniu wymagają weryfikacji na komputerze z PySide6.
