# Stan projektu wobec Game_Design.md

**Przegląd: 25.10.2026.** To ocena zgodności funkcji z GDD, a nie wynik niezależnych playtestów ani certyfikat wydania. Szacunkowo ukończono **około 80–85% zakresu funkcjonalnego wersji 1**. Do gotowego, zweryfikowanego wydania pozostaje więcej pracy (około 60–70% gotowości produkcyjnej), przede wszystkim testy interfejsu i balansu oraz dystrybucja.

| Faza GDD | Ocena | Dostępne w kodzie | Do zrobienia / ograniczenia |
| --- | --- | --- | --- |
| P0 - prototyp i balans | Częściowo | Resolver, AI, testy zasad, symulacje | 30 ręcznych partii i reprezentatywne playtesty archetypów |
| P1 - vertical slice | W dużej mierze | Menu, mapa, tutorial, zapis, plansza, animacje podstawowe | Potwierdzić, że *nowa osoba* rozumie grę bez pomocy |
| P2 - karty i talie | W dużej mierze | 52 jednostki + 24 wydarzenia, testy, żetony, katalog, edycja talii | Wizualne testy każdej interakcji i odczytywalności na małych ekranach |
| P3 - kampania | W dużej mierze | 20 przeciwników, unikalne zasady i remixy, dialogi, nagrody | Pełny ręczny przebieg kampanii i dopracowanie prezentacji |
| P4 - wróżby | W dużej mierze | Rozkłady 1/3/5, oryginalne ilustracje, lokalna historia, notatki, JSON | Testy importu / eksportu z UI i zachowania na docelowych systemach |
| P5 - HARD / polishing | Częściowo | Draft 24→18, AI HARD, statusy, animacje, SFX, redukcja animacji | Długie playtesty, strojenie balansu, wydajność, 60 FPS, dostępność, odsłuch i testy muzyki na docelowych systemach |
| P6 - wydanie | Częściowo | Natywny projekt desktop i konfiguracja buildów CI | Brak wersji web/PWA, brak sprawdzonych buildów Windows/macOS, podpisów i notarization; zweryfikować linuksowy runtime |

## Zmiany w tej iteracji

1. Energia gracza została przeniesiona nad własną rękę; ⚡ jest zawsze symbolem Energii / kosztu.
2. Każda jednostka ma przy ✦ Mocy oddzielny symbol, także na podsumowaniach stref i w szczegółach.
3. Mulligan ma wyraźną instrukcję i zaznaczenie „DO WYMIANY”, licznik 0–2, osobne „Zachowaj rękę” / „Wymień i zacznij”.
4. Główny przycisk w czasie rozgrywki nazywa się „Zakończ turę”. Jego działanie nadal zatwierdza plan, uruchamia odsłonięcie i automatycznie prowadzi do kolejnej tury.
5. Zasady: 7 prostych kroków + opcjonalne szczegóły; nazewnictwo: TABOt (forma podstawowa), karty TABOta, Karciane Rozprawy TABOta.
6. Zasady silnika i format zapisów nie zostały zmienione.

## Zalecana kolejność dalszych prac

1. Uruchomić testy `scripts/check_ui.py` i `scripts/check_interactions.py` z PySide6 na zgodnym systemie oraz sprawdzić ręcznie układ w 1280×720 / 1600×900 / 1920×1080.
2. Przeprowadzić 5–10 testów nauki gry z osobami bez znajomości zasad, ze szczególnym uwzględnieniem wymiany kart, kosztu i przejścia tur.
3. Zautomatyzować serię rzędu 10 000 meczów na **parę archetypów** zgodnie z GDD i stroić balans na podstawie danych, nie samej hipotezy projektowej.
4. Dopracować selekcję celów, sygnalizację źródeł zmian Mocy, 20 ikon warunków i dostępność na małych ekranach.
5. Zweryfikować od zera instalację, zapis i dźwięk na Linux/Windows/macOS oraz zdecydować, czy web/PWA to wymóg wydania, czy świadome odstępstwo od GDD.

## Środowisko kontroli tej iteracji

- `python -m unittest discover -s tests -v`: przechodzi 40 testów (36 oryginalnych i 4 nowych testów kontraktu UI).
- `python scripts/simulate.py --games 100 --difficulty normal`: przechodzi 80 pojedynków (2 na każdy z 20 bossów w dwóch wariantach; parametr `--games` jest w tym skrypcie rozdzielany między 40 przypadków).
- `python -m compileall -q tabota main.py scripts tests`: przechodzi.
- **Nie wykonano testu renderowania Qt** w tym środowisku: brak działającej lokalnej instalacji PySide6; pakiet Qt z dostarczonego Linuksowego buildu wymaga GLIBC 2.43, a system udostępnia GLIBC 2.41. Wymaga ponownej próby na maszynie z odpowiednim Qt/PySide6.

Dostarczony ZIP zawiera kompletny kod źródłowy i 52 grafiki; nie duplikuje katalogu `.venv`, folderu `dist` ani wyników tymczasowych kompilacji ze starego archiwum.


## Iteracja: czytelność kolekcji, przeciągania i wdrożenia gracza (25.10.2026)

- Przeciąganie: zamiast przesuwać kartę wewnątrz `Flickable` rysujemy niezależny obraz karty o wyższym `z` w `Battle.qml`; pole źródłowe zostaje na miejscu. Nie jest potrzebna animacja, gest działa również przy `reduced`.
- Kolekcja: niezdobyte karty dostają tylko rewers, identyfikator oraz warunek zwycięstwa w konkretnej rozprawie. Ich nazwy, efekty, grafiki i koszty są usuwane z danych katalogu, a podgląd jest blokowany w adapterze.
- Początek meczu: każdy nowy deck musi mieć jednostkę ⚡ 1; deterministyczna korekta losowej ręki gwarantuje możliwość pierwszego ruchu po starcie i po wymianie. Taka sama zasada dla rywala.
- Tutorial: pierwsze 3 tury mają krokowe okna i obowiązkowe zagrania sprawdzane zarówno przez UI, jak i `Match.commit`. Od tury 4 znika ograniczenie i pojawia się krótkie zaproszenie do samodzielnej gry.
- Zachowanie zgodności wcześniejszych presetów: zapis pozostaje poprawny, natomiast start nowego pojedynku z talią bez ⚡ 1 zostaje zablokowany do czasu poprawienia talii.
- `python -m unittest discover -s tests -v`: **50/50** testów, w tym dodatkowe próby 20 rozpraw, losowań startowych, mulliganów, rygorów tutorialu, zapisu kroku lekcji oraz testy kontraktowe warstwy QML.
- Testy rzeczywistego przeciągania i ekranów Qt **nadal wymagane** na komputerze z kompatybilnym PySide6; to znane ograniczenie środowiska, nie potwierdzony test graficzny.


## Iteracja: muzyka, czytelność kart i modal reguły (26.10.2026)

- Wszystkie 26 przekazanych utworów OST z `Music.zip` są w `music/`; dopasowane do przeznaczenia zgodnie z dokumentem promptów. 4 utwory do ekranów, osobny motyw dla każdego z 20 przeciwników, dżingle zwycięstwa i porażki.
- Dwa odtwarzacze MP3 realizują płynne przejścia ok. 1,4 s. Przy wyniku przejście skrócone do ok. 0,32 s, a podkład łagodnie ściszany pod dżingiel. Muzyka nie zmienia się na pauzie i nie restartuje się przy odświeżaniu tego samego ekranu. Opcje zawierają wyłącznik muzyki i niezależną głośność muzyki / SFX; stare `settings.json` są poprawne.
- Przy najechaniu karta w ręce ma kopię wizualną nad przyciętym obszarem (nie nad zasłoniętym modalem). Górna połowa jest przeznaczona do wyboru/zagrania, dolna ma półprzezroczystą nakładkę „SZCZEGÓŁY” i otwiera zwykły podgląd karty. Nadal działa prawy klik/I.
- W każdej nie-tutorialowej nowej rozprawie przed wymianą ręki jest osobny modal **WARUNEK ROZPRAWY**. Stan potwierdzenia zapisuje się w `match.flags` (starsze zapisy bez znacznika są traktowane jak już potwierdzone). Adapter blokuje zagrania i wymianę do chwili potwierdzenia.
- Usunięto wskaźnik „LOKALNIE / OFFLINE” z górnego paska.
- **54 testy**: 53 przechodzi, 1 integracyjny test Qt pominięty z powodu niedostępnego PySide6. Brak testów renderowania i odsłuchu Qt w bieżącym środowisku. Patrz `docs/QA.md`.


## Korekta powiększania karty i logu (26.10.2026)

- Wcześniejsze nakładanie drugiej karty do podglądu zostało zastąpione **przeniesieniem tego samego komponentu** `Card` poza `Flickable` za pomocą `ParentChange`. Podczas przeciągania wykorzystywana jest również ta sama karta, bez odrębnego animowanego replikatu.
- Nakładka „SZCZEGÓŁY” płynnie animuje przezroczystość podczas najechania na dowolną część karty; wyłącznie miejsce kliknięcia decyduje o wyborze lub inspekcji.
- Usunięto przyczynę przypisania `undefined` do `bool` i poprawiono kolejność zamykania QML/API, na którą wskazywały `TypeError` użytkownika. Ostrzeżenia związane z mp3float nie stanowią wyjątku aplikacji.
- Testy statyczne i jednostkowe przechodzą, renderowania Qt w tym środowisku nadal nie zweryfikowano. Szczegóły w `docs/QA.md`.

## Kolejna iteracja: globalne animacje i rozdzielenie funkcji kart (26.10.2026)

- Nakładka szczegółów porusza się z animowaną oryginalną kartą w ręce - jest dzieckiem elementu `motion`.
- Karty na stole mają prostą interakcję: kliknięcie = szczegóły; podział góra/dół zachowano tylko dla kart w ręce.
- `FadeBox.qml` definiuje wspólne pojawianie/znikanie okien, w tym widoku reguły, wymiany i tutorialu. Interfejs nie przechwytuje kliknięć podczas zamykania okien, a warunek rozprawy kończy fade out zanim zacznie się wymiana ręki.
- Ekrany mają wyjście/zmianę zawartości/wejście; dodatkowe animacje dotyczą zakładki dziennika, zaawansowanych zasad i kroków wróżby.
- `python -m unittest discover -s tests`: 62 zaliczone, 1 pominięty z powodu braku kompatybilnego PySide6. Wizualne potwierdzenie pozostaje konieczne.


## Rewizja fabularna: Puchar PROPLAYERA (26.10.2026)

- Tytuł gry: **Karty TABOta: WSZYSCY DO BANA!**; kampania: **Puchar PROPLAYERA**.
- Nowy prolog, stawka Złotego Taboretu, 20 turniejowych sytuacji i 120 kwestii sześciu rodzajów; ELTaboBot jest organizatorem i finałowym rywalem.
- Nowe nazwy aktów, kroniki, wyzwań, ekranów wyników, opisów nagród, pierwszego i finałowego stolika oraz alternatywne zakończenie HARD.
- Między aktami w istniejącym ekranie wyniku i briefingu wyświetlane są krótkie scenki (bez nowego systemu rozgrywki).
- **Mechanika bez zmian:** 20 par talii, 52+24 karty i 3 żetony, nagrody, tury, rytuały i unikalne WR-y, w tym harmonogram glitchu finałowego, zostały zachowane.
- Opcjonalna lustrzana walka TABO vs TABO i wyjątkowy rewers nadal **nie są wdrożone**.
- Stare zapisy i odblokowania działają na tych samych identyfikatorach. Nazwy scen są wyłącznie prezentacyjne.
- Pliki muzyczne pozostają bez zmian. Prompty OST dostosowano tekstowo jako materiał na przyszłość.
- Pozostaje ręczny smoke test graficzny nowego prologu, ekranów aktów i epilogów na działającym Qt.
