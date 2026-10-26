# Karty TABOta: WSZYSCY DO BANA!
## Kompletny Game Design Document (GDD), scenariusz, księga zasad i specyfikacja interfejsu

**Wersja dokumentu:** 1.1 (Puchar PROPLAYERA) - 26 października 2026  
**Format:** single-player, 2D, PC (Windows/Linux/macOS), web, bez obowiązkowego backendu.  
**Tryby:** Puchar PROPLAYERA - FABUŁA (gotowe talie), Puchar PROPLAYERA - HARD (draft i własne talie), Wróżby z kart TABOta.  
**Postać gracza:** TaboRETRO. **Ton:** retro, surrealistyczny, czarny humor i przekomarzanie się czatu; żarty z lore bez upokarzania prawdziwych ludzi.  
**Status:** projekt koncepcyjno-produkcyjny; nazwy istniejących 52 kart sprawdzone z dostarczonym ZIP-em. Liczby są pierwszą zbalansowaną *hipotezą projektową*, a nie wynikiem prawdziwych playtestów.  
**Zalecana długość:** kampania FABUŁA 4–6 h; wariant HARD dodatkowe 5–9 h w zależności od powtórek; wróżby bez limitu. 

> **Logline:** Tabo pokazuje na streamie fizyczne Karty TABOta i żartuje, że nie może przegrać we własną grę. ELTaboBot uznaje to za zgodę na udział w absurdalnym **Pucharze PROPLAYERA**. Aby zdobyć Złoty Taboret i tytuł PROPLAYERA, trzeba pokonać dwudziestu rywali z własnej społeczności.

> **Rozdzielenie prawdy od fikcji.** Istniejące fakty/nazwy/powiedzonka przywołane z TaboLore, materiałów streamowych i oryginalnej talii są wskazane w źródłach na końcu. **Wszystkie rozmowy, pojedynki, umiejętności, liczby, teksty nowych kart i fabuła kampanii są autorską propozycją**, NIE autentycznymi wypowiedziami osób. Głosy aktorskie nagrywać wyłącznie za zgodą zainteresowanych; do prototypu wystarczą napisy i krótkie dźwięki.

---

# 1. Filary projektu i zakres

1. **Poznaj w 2 minuty, opanuj po wielu partiach.** Trzy strefy, sześć tur, punkty widoczne przez cały czas; dodatkowe reguły przeciwników dokładane po jednej.
2. **Każda walka opowiada żart.** Postacie nie są tylko portretami - każda zmienia regułę meczu w przewidywalny, oznaczony na ekranie sposób.
3. **Obie strony grają fair.** Identyczne ograniczenia talii, kosztów i wiedzy o kartach; specjalna zasada pola z reguły działa symetrycznie, ale przeciwnik buduje pod nią talię.
4. **Jeden fizyczny TABOt, dwie funkcje.** 52 oryginalne ilustracje i ich znaczenia nietknięte w Wróżbach; jako typy kart bojowych z odrębnymi statystykami w pojedynkach.
5. **Wyrafinowana animacja, skromna produkcja.** Efekty 2D, animowane reakcje kursora, świetne dźwięki, mało nowych ilustracji, napisy jako pełnowartościowa alternatywa dla głosówek.
6. **Bez mikropłatności i wymuszonych powtórek.** Karty otrzymuje się za postęp, dodatkowe wyzwania i odkrywanie sekretów. Wszystkie da się zdobyć offline.

**Poza zakresem v1:** multiplayer, serwerowa synchronizacja, sklep, ranking online, kolekcjonerskie paczki RNG, generatywna interpretacja wróżb, pełne 3D, kosztowna produkcja cutscenek. **Opcjonalne po premierze:** tryb wyzwań dziennych offline, turniej, zapis w chmurze po świadomej zgodzie.

## 1.1. Dlaczego model 18 kart?

- Jedna talia pojedynkowa ma **18 fizycznych instancji**; maksymalnie **2 kopie** dowolnego typu (bez wyjątku również dla najmocniejszych).
- Właściciel musi odblokować **typ** karty; w walce może wykorzystać 2 kopie odblokowanego typu, nie potrzebuje kupować lub odblokowywać osobno każdej kopii. To redukuje grind.
- W pierwszej ręce jest 5 kart; na początku tur 2–6 dochodzi 1; zatem zwykle obejrzymy co najmniej 10/18 kart, zanim wliczymy dobieranie z efektów. To pozwala na planowanie, ale nie na stuprocentowe kombinacje.
- Po sześciu turach gracze wydają łącznie maksymalnie 21 Energii i przeciętnie zagrywają 7–9 kart, co mieści się w 12 slotach stref.
- Własna talia ma od 12 do 18 **kart jednostek** i od 0 do 6 **kart wydarzeń** (łącznie dokładnie 18). Dzięki temu nawet „spell deck” musi wystawiać punkty.
- Losowość = potasowanie i dobieranie, nigdy ukryte rzuty kością decydujące o sile kart. Efekty opisują dokładnie, co zrobią.

## 1.2. Poziomy trudności / kampanie

| Tryb | Kiedy | Skład talii | Ręka | AI | Cel |
|---|---|---|---|---|---|
| **FABUŁA (Normal)** | Od razu | Automatycznie zestawione, rosnące w siłę 18 kart na konkretną misję; gracz może obejrzeć, ale nie edytować | Losowana w zwykłych meczach; w tutorialu i wybranych lekcjach skryptowana | uczące, potem średnie | Wygodna przygoda i nauka wszystkich systemów |
| **PROPLAYER (Hard)** | Po ukończeniu Fabularnej; opcjonalnie wcześniejsze odblokowanie w ustawieniach dla weteranów | Przed KAŻDYM pojedynkiem 24-kartowa oferta draftu: wybierz dokładnie 18, maks. 2 kopie, min. 12 jednostek; lub wczytaj własną talię | Zawsze losowana | lepsze planowanie bez podglądania przyszłości | Druga kampania z remixami zasad i osobnymi nagrodami |
| **Swobodna rozgrywka** | Po tutorialu | Gotowy archetyp lub własny deck z odblokowanych typów | Losowana | Easy/Normal/Hard | Rewanże i trening |
| **Wróżby** | Od pierwszego uruchomienia | Niezależna stała talia 52 unikatowych kart | 1/3/5 bez powtórek | - | Zabawna, lokalna historia wróżb |

**Uwaga interpretacyjna:** „narzucone karty w każdej turze” nie powinny oznaczać, że gra stale decyduje za gracza, co zagrywa. W NORMAL **z góry ustalona jest pełna talia**, lecz gracz wybiera swoje ruchy; tylko tutorial i kilka pokazowych momentów mają ułożone wcześniej rozdanie. W HARD draft odbywa się **przed meczem**, nie co turę - inaczej decyzja z 18 kart stałaby się nieczytelna i przeciągała partię.

---

# 2. Pełny regulamin pojedynku - wersja 1.0

## 2.1. Cel i plansza

Dwie strony (Tabo u dołu, oponent u góry) mają po 3 rzędy/strefy: **STREAM**, **CZAT**, **ZAPLECZE**. Każda ze stron ma maksymalnie **4 miejsca na jednostki w każdej strefie**. Łączna liczba zajętych pól = maks. 12 kart jednostek na stronę. Karty wydarzeń po wykonaniu trafiają na stos odrzuconych i nie zajmują slotu. Żetony utworzone przez karty zajmują slot, mają moc i można je usunąć, ale nie są dobierane ani traktowane jak karta z kolekcji.

W każdej strefie liczona jest suma **aktualnej Mocy** własnych jednostek + wyłożonych znaczników punktowych niezwiązanych z jednostką. Strefę wygrywa strona z większą liczbą punktów. Po zakończeniu 6. tury osoba wygrywająca co najmniej **2 strefy** wygrywa mecz. Przy remisie w liczbie zdobytych stref rozstrzyga **suma punktów z 3 stref**. Jeśli i ona jest równa: remis, gracz może bez konsekwencji powtórzyć mecz; w HARD remis nie zalicza postępu. Żadnego punktowania za nadwyżkę czy „overkill” poza tym tie-breakiem.

**Priorytet:** najpierw liczba zdobytych stref, potem suma punktów. Przykład: Tabo 9:8, 8:7, 2:30 → wygrywa **2 strefy** mimo sumy 19:45. Remis w konkretnej strefie nie zalicza jej żadnej stronie.

## 2.2. Talia, ręka, koszt, tura

- 18 kart w talii. Maks. 2 kopie typu; 12–18 jednostek i 0–6 wydarzeń. Żadnego limitu frakcji. Karty oryginalne i nowe wydarzenia mają osobne `card_id`.
- **Start:** obie strony tasują niezależnie deterministycznym RNG z zapisanego `seed`, dobierają po 5 kart. Każda może jednorazowo wymienić **0–2 karty** (mulligan); zwrócone trafiają do talii i zostają przetasowane, zanim dobierze zamienniki.
- **Tura 1:** 1 Energia na całą turę; tura 2: 2; ... tura 6: 6. Na początku każdej tury energia odnawia się do pełnego limitu, niewydana przepada. Nikt nie może wydać więcej niż 6 w turze. Energia NIE przechodzi do następnej tury.
- Na początku tur 2–6 dobierz 1 kartę. Efekty „dobierz” wykonują się od razu; limit ręki **10**. Jeśli dociąg przekroczy 10 kart, nowa karta trafia jawnie na stos odrzuconych (interfejs pokazuje „RĘKA PEŁNA”). Pusta talia = brak dociągu, bez kar zdrowotnych.
- Karty rozgrywamy **w turach jednoczesnych z ukrytym planem**. Gracz układa ruchy, może je cofnąć przed zatwierdzeniem. AI planuje swoją listę ruchów bez znajomości ręki gracza. Po potwierdzeniu oba plany ujawniają się, po czym jednostki i wydarzenia rozpatrywane są **naprzemiennie**: pierwszeństwo gracza w turach nieparzystych, przeciwnika w parzystych. W obrębie planu zachowujemy kolejność kliknięć. Ta zasada uniemożliwia AI reagowanie na tajne ruchy bieżącej tury.
- Po rozpatrzeniu efektów Wejścia aktualizowane są Aury i wyświetlana aktualna punktacja. Efekty Finału uruchamiają się dopiero po turze 6, po odświeżeniu Aur.
- Wydarzenia są typu **Zagranie**: wybór jednej dozwolonej strefy/celu, efekt natychmiastowy, odrzucenie. Jeśli legalny cel zniknie przed rozpatrzeniem, wydarzenie szuka wskazanego w opisie celu rezerwowego; jeśli go nie ma, zachowuje koszt i nie daje efektu. Interfejs musi wyświetlić takie ryzyko.
- W trakcie planowania widzimy „przewidywany wynik po własnych ruchach”, ale nie wynik przyszłego zagrania AI. Wszystkie ikony efektów i zasad pola są jawne.

## 2.3. Właściwości kart i słownik

- **Koszt (K):** wymagana energia. **Moc (M):** drukowany wynik przed modyfikacjami. Nie ma punktów życia.
- **Wejście:** jednorazowe po położeniu i ujawnieniu. **Aura:** trwały bonus/ograniczenie dopóki jednostka znajduje się na planszy i nie została wyciszona. **Finał:** jednorazowe po 6. turze, o ile karta nadal jest na planszy i jest aktywna.
- **Wzmocnij X:** dodaj X do Mocy wskazanej jednostki do końca meczu; **Osłab X:** odejmij X do końca meczu; Moc jednostki nigdy nie spada poniżej 0. Łączne znaczniki zmian na pojedynczej jednostce z kart i bossowych efektów mają zakres od −4 do +4; przekroczenie jest ignorowane. Aury liczone są niezależnie, ale suma bonusu z Aur na jednej karcie jest ograniczona do +4.
- **Wycisz:** wyłącza Aurę i Finał wskazanej jednostki do końca meczu, ale nie cofa już wykonanych Wejść. Nie odbiera podstawowej Mocy. Jednostka wyciszona może dostać wzmocnienie, lecz nie aktywuje Aury.
- **Usuń:** przenieś jednostkę i jej wzmocnienia na stos odrzuconych właściciela. Nie uruchamiaj ponownie Wejścia. Można usunąć własny żeton.
- **Przesuń:** karta zachowuje zmiany Mocy, traci bonusy zależne od starej strefy i od razu przelicza nowe Aury. Strefa docelowa musi mieć wolny slot.
- **Ochrona:** raz ignoruje pierwsze wrogie „Usuń”, „Osłab”, „Wycisz” lub „Przesuń”, po czym znika; nie blokuje bonusów strefy ani wydarzeń symetrycznych.
- **Sąsiad:** STREAM ↔ CZAT ↔ ZAPLECZE; STREAM nie sąsiaduje bezpośrednio z ZAPLECZEM.
- **Znacznik punktowy** (np. Hymn +3) nie jest jednostką, nie zajmuje slotu, nie można go celować standardowym Banhammerem; ma oddzielny podgląd.
- **Tagi:** Moderacja, Widz, Retro, Chaos, Hymn, Horror, Technika, Wydarzenie. W tabelach każdy typ ma jeden tag główny; synergia dotyczy wyłącznie nazwanego tagu. Unikamy ukrytych przynależności.
- **Czas działania:** wszystkie efekty nieopisane jako „w tej turze” trwają do końca meczu. Zasady przeciwnika wyświetlane w panelu wyjaśniają wyjątki.

## 2.4. Rytuał 20:30 - odblokowanie w rozdziale MaciekWolf92

Od misji **04** w 4. turze przed planowaniem obaj gracze wybierają **jedną** z trzech darmowych opcji (nie kosztuje Energii, użycie raz na mecz):

1. **HYMN** - umieść trwały znacznik **+3 punkty** w wybranej strefie.
2. **WSZYSCY DO BANA** - **wycisz** jedną wrogą jednostkę z Aurą lub Finałem, jeśli taka istnieje; w przeciwnym razie akcja jest niedostępna. Nie usuwa i nie zadaje punktów. Wybór i legalność są widoczne przed zatwierdzeniem.
3. **POKAŻ KLIPA** - dobierz **2 karty**; jeśli talia jest pusta lub ręka pełna, gra ostrzega o możliwej stracie efektu.

Opcję wybieramy jako jeden z ruchów planu i ujawniamy jako pierwszą akcję danej strony w turze 4, w kolejności pierwszeństwa. AI nie zna wyboru gracza w chwili podejmowania własnej decyzji. Przed misją 04 pole Rytuału jest oznaczone jako „odblokujesz w Rozdziale Hymnu”; nie rozpraszamy tutorialu.

## 2.5. Pozycje, statusy, rozstrzyganie konfliktów

**Deterministyczny porządek:** (1) jednoczesny wybór ruchów; (2) ujawnienie; (3) akcje Rytuału w turze 4; (4) naprzemienne wystawianie kart i natychmiastowe efekty Wejścia; (5) odświeżenie Aur; (6) naliczenie punktów; (7) po turze 6: Finały - gracz/AI według kolejności tury 6, wewnątrz od lewej strefy i kolejno od najstarszej karty - następnie ponowne naliczenie; (8) rozstrzygnięcie. Efekt Finału może przesunąć lub usunąć, ale nigdy nie wyzwala wcześniejszego Finału drugi raz.

Celowanie to dokładnie wskazana karta, nie kliknięcie „gdzieś w rzędzie”. Jeśli jednostka ma Ochronę, wyświetla się pęknięcie tarczy. Po usunięciu Aury wszystkie widoczne liczby aktualizują się płynnie. Nie wolno dopuścić do ujemnej Mocy, dzielenia przez zero ani rekurencyjnego tworzenia żetonów.

## 2.6. Zasady projektowania unikalnych modyfikatorów meczowych

Każdy przeciwnik wnosi jeden **jawny Warunek Rozprawy (WR)**. Modyfikator **z zasady działa na obie strony**; AI dobiera synergie w swojej talii, co buduje trudność i osobowość. Ekran startowy zawiera: nazwę, opis w 1 zdaniu, liczbowy przykład, ikonę i przycisk `?`. Jeśli WR ignoruje ograniczenia globalne, ma to napisane dosłownie. WR nie może uniemożliwiać zagrania karty bez wcześniejszego sygnału i ma mieć kontrę strategiczną. W trybie HARD pojawia się **Remix WR** - odmienny, jawny wariant, nie ukryty oszust AI.

---

# 3. Balans: model liczbowy i testy

## 3.1. Budżet kart

Pierwsza wersja opiera się na **celowanej wartości punktowej** \(B(K)\), w której pojedyncza karta nie może zapewniać nieograniczonej przewagi:

| Koszt K | Docelowa suma: Moc + oczekiwany ekwiwalent efektu | Typowe Moc bazowa | Typowa wartość efektu |
|---:|---:|---:|---:|
| 1 | 3 | 2–3 | 0–1 |
| 2 | 5 | 3–4 | 1–2 |
| 3 | 6 | 4–5 | 1–2 |
| 4 | 7 | 5–6 | 1–2 |
| 5 | 9 | 6–8 | 1–3 |
| 6 | 10 | 7–9 | 1–3 |

Wartość `oczekiwana` nie jest dodatkiem wyświetlanym na karcie; służy projektantowi. Bonus +2 warunkowy ≠ 2 gwarantowane: jeśli uruchamia się w 60% partii, jego ekwiwalent to około 1,2. Dobranie jednej karty traktujemy wstępnie jako **1,5 punktu użyteczności** (zależnie od pozostałych tur), a przesunięcie jako ok. 1–2, Wyciszenie ok. 2, Usunięcie słabego żetonu ok. 1–2. Nie sumujemy punktów z efektu, który może trafić 0 celów.

**Miękkie ograniczenia:** dodatki na pojedynczej karcie w przedziale [−4,+4], bonusy Aur max +4 do jednostki, efekty obszarowe max +3 łącznie bez warunku, Finał max +4 w jednej karcie, wymiana „usuń” maksymalnie jednostkę drukowanej Mocy 4 lub niższej (chyba że karta kosztuje 6 i jest zbalansowana oddzielnie). Karty muszą przechodzić testy brzegowe: puste strefy, maks. sloty, wyciszenie, zabranie celu i remis.

## 3.2. Inne źródła równowagi

- Obie strony wybierają 18 kart i maks. 2 kopie; odmienne zestawy nie zmieniają zasad kosztów.
- Rozdania nie są manipulowane pod wygraną AI. Tylko **tutorial** i wyraźnie oznaczone zagadki fabularne korzystają ze skryptowanego porządku talii.
- W NORMAL po 2 kolejnych porażkach opcjonalne podpowiedzi strategiczne („Warto rozdzielić siłę między dwie strefy”), ale **bez ukrytych dopalaczy** kart.
- Punkty zwycięstwa nie są farmione przez powtarzanie najłatwiejszego bossa. Typy odblokowują się za pierwszą wygraną, wpisy TaboLOGu za misje.
- W HARD AI ma dłuższy horyzont analizy, a nie +20% Mocy ani uprzywilejowane rozdanie.
- Wiele kopii służy spójności talii, ale nie gwarantuje dociągnięcia konkretnej karty; przy 2 kopiach w 18 i 10 obejrzanych kartach szansa zobaczenia co najmniej jednej kopii to `1 - C(16,10)/C(18,10) = 81,7%`, zakładając brak dodatkowego dociągu i mulliganu.

## 3.3. Progi do potwierdzenia playtestami

**Nie należy podpisywać obecnego projektu jako matematycznie udowodnionego balansu.** Statyczny budżet ogranicza oczywiste nadużycia, ale synergie, losowość i AI wymagają testów. Wersja beta musi spełnić: win rate 45–55% dla par gotowych talii przeciwko porównywalnemu AI; brak kart z udziałem w zwycięskich deckach ponad 75% bez uzasadnienia popularnością; różnica pierwszeństwa tury poniżej 3 p.p. w symulacjach; średni czas 6–9 min; ani jedna misja nie może wymagać jednej jedynej kombinacji kart. Dla każdej pary archetypów uruchomić min. 10 tys. meczów AI-vs-AI z różnymi seedami po zaimplementowaniu prawdziwego resolvera.

---

# 4. Katalog 52 oryginalnych kart TABOta - osobne statystyki do pojedynków

**Źródło nazw:** 52 pliki `01_...png`–`52_...png` z dostarczonego archiwum. **Źródło wizualne:** oryginalne grafiki z ZIP. **Nowe są tylko:** liczby, tagi, opis umiejętności na nakładce pojedynkowej. Kolor, postać, napis/cytat i słowa-klucze z fizycznej karty powinny pozostać niezmienione. Ponieważ w oryginalnych nazwach jest wiele zabawnych form, w tabeli zostawiam je w formie czytelnej, rozpoznawalnej względem grafik. **K/M = koszt/moc.**

Każdy typ może wystąpić w decku 0, 1 lub 2 razy. Nie ma oznaczenia „legendarny = tylko jedna kopia”, ponieważ to niepotrzebnie komplikuje rozgrywkę. Gdy karta wymaga celu, brak legalnego celu = rozpatruje się jedynie drukowaną Moc i ewentualną drugą część tekstu. Drobne bonusy są ukierunkowane na strategię, nie na niekontrolowane „combo infinity”.

| ID | Oryginalna karta | K | M | Tag | Działanie w pojedynku |
|---:|---|---:|---:|---|---|
| 01 | **Prorok Tabo** | 6 | 8 | Chaos | Finał: dodaj +1 punkt do każdej strefy, w której masz co najmniej 1 jednostkę (maks. 3). |
| 02 | **Palec Przeznaczenia** | 1 | 2 | Chaos | Wejście: przesuń inną własną jednostkę do sąsiedniej strefy z wolnym slotem; możesz zrezygnować. |
| 03 | **Tabożeństwo** | 4 | 5 | Hymn | Wejście: wzmocnij o +1 do 2 innych własnych jednostek w tej strefie. |
| 04 | **Święty Headset** | 2 | 3 | Technika | Aura: ta karta ma +2, jeżeli jest jedyną twoją jednostką w strefie. |
| 05 | **Psychosobota** | 4 | 5 | Chaos | Wejście: wybierz 1 własną jednostkę w tej strefie; ma +2, jeśli w strefie jest przynajmniej 1 wroga jednostka. |
| 06 | **Taboret Przeznaczenia** | 1 | 2 | Widz | Aura: +1 do tej karty za co najmniej 1 innego własnego Widza w strefie. |
| 07 | **LtAsiaa - Młotkowa** | 5 | 7 | Moderacja | Wejście: wycisz jedną wrogą jednostkę w tej samej strefie. |
| 08 | **ToTylkoNysmo - Moderacja** | 2 | 3 | Moderacja | Aura: +2 do tej karty, gdy jest tu inna twoja jednostka Moderacji. |
| 09 | **Jillie_Studio - Królowa Spamu** | 3 | 4 | Widz | Wejście: wzmocnij tę kartę o +1 za inną własną jednostkę w tej strefie (maks. +3). |
| 10 | **QrusKnur - KnurKnur** | 3 | 6 | Widz | Bez umiejętności. Solidna jednostka punktowa. |
| 11 | **GreedN3 - Dawca Wspomnień** | 3 | 4 | Retro | Wejście: dobierz 1 kartę, jeśli w tej strefie leży inna twoja karta Retro. |
| 12 | **InfinityPotato0 - Toksyk Premium** | 4 | 6 | Chaos | Wejście: osłab wybraną wrogą jednostkę w tej strefie o −1. |
| 13 | **MaciekWolf92 - Strażnik Hymnu** | 3 | 4 | Hymn | Aura: ta karta ma +2, jeżeli w tej strefie leży Hymn lub jest znacznik Rytuału HYMN. |
| 14 | **Tabarzak - Brat Krwi** | 3 | 4 | Widz | Wejście: wzmocnij inną własną jednostkę w tej strefie o +2. |
| 15 | **KokoszTsunami - Potężny Strimer** | 5 | 8 | Widz | Wejście: +1 do tej karty, jeżeli aktualnie przegrywasz tę strefę. |
| 16 | **KroolRemizy - Ekspert Sztućców** | 2 | 4 | Retro | Finał: +1 do tej karty, jeśli grasz na ZAPLECZU. |
| 17 | **Krisuroku - Okrzyk Zagłady** | 3 | 4 | Chaos | Wejście: nadaj +2 Mocy następnej własnej jednostce zagranej w tej samej strefie (jednorazowy znacznik strefy; wygasa po 6. turze). |
| 18 | **MackoTheHollow - Cozy Głos** | 2 | 3 | Widz | Wejście: wybrana własna jednostka w tej strefie otrzymuje Ochronę. |
| 19 | **Meeefjuuu - Przebojowość** | 3 | 4 | Hymn | Wejście: +1 do maks. 2 własnych jednostek z tagiem Hymn we wszystkich strefach. |
| 20 | **Nyravespera - Gocka Moc** | 4 | 6 | Horror | Aura: +1 do tej karty za inną własną jednostkę Horror tutaj (maks. +2). |
| 21 | **Pestarz - Kierownica o 3 w Nocy** | 2 | 3 | Chaos | Wejście: wzmocnij tę kartę o +2, jeśli jest twoją pierwszą jednostką w danej strefie. |
| 22 | **Pierd0la - Wieczny Finał** | 4 | 5 | Widz | Finał: wzmocnij tę kartę o +2, jeżeli zagrano ją w turze 5 lub 6. |
| 23 | **AL_PSX - Bez Piwnic** | 2 | 4 | Retro | Wejście: jeśli ZAPLECZE jest puste po twojej stronie, dobierz 1 kartę zamiast dodawać Moc. |
| 24 | **Magiccorn - Magiczna Kukurydza** | 2 | 3 | Chaos | Wejście: wzmocnij inną własną jednostkę w tej strefie o +2. |
| 25 | **Andziaalek - Tirowiec** | 3 | 4 | Technika | Wejście: przesuń tę kartę do sąsiedniej strefy; jeśli to zrobisz, zyskaj na niej +2. |
| 26 | **Drakson - Darmowe Woskowanie** | 2 | 3 | Widz | Wejście: usuń do 1 znacznika Osłabienia z własnej jednostki w tej strefie; za każdy usunięty −1, wzmocnij ją o +1 (maks. +2). |
| 27 | **Larond - Acziwkowy Spoceniec** | 4 | 5 | Retro | Finał: +2 do tej karty, jeśli wygrywasz co najmniej 2 strefy przed rozpatrzeniem Finałów. |
| 28 | **Orzechowy Rozpruwacz - Taboretograf** | 3 | 4 | Technika | Wejście: stwórz żeton STOŁEK (Moc 2, tag Technika) w tej strefie, jeśli jest miejsce. |
| 29 | **B4Nork - Wariacik** | 3 | 5 | Chaos | Wejście: przesuń wybraną inną własną jednostkę do sąsiedniej strefy; możesz zrezygnować. |
| 30 | **Gumbox - Gamboksik** | 2 | 3 | Chaos | Aura: +2 do tej karty, jeżeli w tej strefie nie ma żadnej innej własnej jednostki z literą „A” w nazwie (sprawdzamy nazwę bez polskich znaków, wielkość bez znaczenia). |
| 31 | **Obwarzanek** | 1 | 2 | Retro | Aura: ta karta ma +1, gdy leży na ZAPLECZU. |
| 32 | **Ptak z Dark Souls** | 5 | 7 | Horror | Wejście: jeżeli w tej strefie jest wroga jednostka o Mocy 2 lub niższej, usuń jedną taką jednostkę. |
| 33 | **Męczony Kapucynek** | 2 | 3 | Horror | Wejście: gdy zagrywasz tę kartę w turze 4–6, dodaj jej +2. |
| 34 | **TRUP-POL S.A.** | 4 | 5 | Horror | Wejście: stwórz żeton TRUPEK (Moc 2, tag Horror) w tej strefie, jeśli jest miejsce. |
| 35 | **Wampir z Podlasia** | 5 | 7 | Horror | Wejście: wzmocnij tę kartę o +2, jeśli w chwili zagrania przegrywasz tę strefę. |
| 36 | **Kierowca Śmigłowca** | 3 | 4 | Technika | Wejście: przesuń inną własną jednostkę do dowolnej strefy z wolnym slotem; możesz zrezygnować. |
| 37 | **Wiertarka do Kawy** | 2 | 3 | Technika | Wejście: wzmocnij inną własną jednostkę w tej strefie o +2. |
| 38 | **Zombie z Rekinem** | 4 | 6 | Horror | Wejście: osłab o −1 maksymalnie 2 wrogie jednostki w tej strefie (każdą najwyżej raz). |
| 39 | **Hymn** | 4 | 5 | Hymn | Wejście: +1 do maks. 2 innych własnych jednostek w tej strefie. |
| 40 | **Banhammer** | 4 | 5 | Moderacja | Wejście: osłab wybraną wrogą jednostkę w tej strefie o −2. |
| 41 | **Clip Moment** | 2 | 3 | Retro | Wejście: dobierz 1 kartę; jeżeli talia jest pusta, +1 do tej karty. |
| 42 | **Top Chatter** | 3 | 4 | Widz | Wejście: +1 do tej karty za każdego innego własnego Widza w tej strefie (maks. +2). |
| 43 | **TaboRanek** | 2 | 3 | Hymn | Wejście: +2 do tej karty, jeśli zagrana w turze 1 lub 2. |
| 44 | **Wodny Wąż** | 5 | 7 | Horror | Wejście: osłab wybraną wrogą jednostkę w tej strefie o −2. |
| 45 | **Cozy ASMR** | 2 | 4 | Hymn | Finał: ta karta otrzymuje +1, jeśli w tej strefie nie było w turze 6 wrogiego wydarzenia. |
| 46 | **500 Follow Special** | 5 | 7 | Hymn | Wejście: +1 do maks. 2 innych własnych jednostek Hymn (w dowolnych strefach). |
| 47 | **ELTaboBot** | 5 | 7 | Technika | Finał: +1 do tej karty za każdą wrogą jednostkę na CZACIE (maks. +3). |
| 48 | **Wapniak - Hejt Prastary** | 3 | 4 | Chaos | Wejście: osłab wybraną wrogą jednostkę w tej strefie o −2. |
| 49 | **KubaFanBZP - BaniCzny Błazen** | 2 | 3 | Chaos | Wejście: gdy jest tu wroga Moderacja, osłab jedną z nich o −2; inaczej +1 do siebie. |
| 50 | **Cydyn - Ojciec Bliźniaków** | 5 | 6 | Widz | Wejście: stwórz w tej strefie 2 żetony BLIŹNIAK (Moc 1, tag Widz), jeśli są 2 wolne miejsca; jeśli jedno - stwórz 1. |
| 51 | **KruparGames - Ojciec Admin** | 3 | 4 | Technika | Wejście: dobierz 1 kartę, jeśli masz w tej strefie inną własną Technika. |
| 52 | **Madbbranko - Komórka Wątroby** | 3 | 5 | Widz | Finał: ta karta otrzymuje +1, jeżeli jest na stole inna twoja jednostka z tagiem Widz. |

**Uzasadnienie tematyczne:** Gumbox bawi się motywem litery A z lore; Cydyn tworzy bliźniaki; Pestarz premiuje wczesne, ryzykowne wystawienie, a nie „bieganie z ink ribbonem”; Maciek pilnuje Hymnu; LtAsiaa i Nysmo kontrolują czat. Zamierzona prostota kart bez umiejętności (QrusKnur) jest potrzebna do budowy pierwszych talii i tutoriala.

## 4.1. Szczególne wyjątki i czytelność kart

- **Gumbox i litera A:** dla uniknięcia problemów z językami implementacja ma sprawdzać `nameKey` z wersji polskiej, nie aktualną wersję przetłumaczonej nazwy; dotyczy innych *własnych* jednostek w tej strefie.
- **LtAsiaa / Rytuał BAN:** wyciszenie wyłącza tylko Aury i Finały, nie natychmiastowe efekty ani bazową Moc. Nie można wyciszać „znaczników punktowych”.
- **Cydyn:** wymaga wolnych slotów; w pełnej strefie tworzy 0 żetonów i gra ostrzega przed zagraniem.
- **Clip Moment / KruparGames:** dociąg nie gwarantuje dobrego zagrania, szczególnie późno; nie zwiększaj automatycznie ich bazowej Mocy w testach tylko dlatego, że „efekt nie zapunktował”.
- **Krisuroku:** znacznik następnej własnej jednostki w strefie pokazuje pulsującą ramkę; sam Krisuroku nie aktywuje własnego bonusu.
- **Drakson:** zdejmuje maksymalnie 2 jednostkowe punkty Osłabienia z **jednej** wskazanej własnej karty. Jeśli brak minusów, nie daje bonusu.
- **Palec Przeznaczenia i B4Nork:** jeśli sąsiednia strefa jest pełna, przeniesienie nie następuje; brak automatycznej zamiany pozycji.
- **Moc i buffy:** w tooltipie pokazuj np. `Moc 7 = bazowa 5 + wejście 2`, nie tylko końcową liczbę.

## 4.2. Karty żetonów (generowane na planszy, nie do talii)

| Żeton | Moc | Tag | Jak powstaje | Czy zajmuje slot? |
|---|---:|---|---|---|
| STOŁEK | 2 | Technika | Orzechowy Rozpruwacz | Tak |
| TRUPEK | 2 | Horror | TRUP-POL S.A. | Tak |
| BLIŹNIAK | 1 | Widz | Cydyn | Tak, każdy osobno |
| GŁOS Z CZATU | 1 | Widz | modyfikatory wybranych bossów | Tak |
| ECHO | 1 | Chaos | wybrane wydarzenia | Tak |

Żetony nie trafiają do decku, nie mogą wrócić do ręki, nie są kartami wróżebnymi, a ich znikanie ma dyskretną animację (bez epatowania przemocą).

---

# 5. Rozszerzenie gry: 24 nowe karty WYDARZEŃ („Wydarzenia z Czatu”)

**Łączna liczba grywalnych typów = 52 oryginalne karty + 24 wydarzenia = 76.** Nie udajemy, że te 24 były w fizycznym zestawie. Mają **osobny prosty szablon z ikoną, tytułem i krótkim tekstem** - można wykorzystać 2D ikonografię z istniejących ilustracji i gradienty, bez 24 nowych malowideł. Wróżby LOSUJĄ WYŁĄCZNIE oryginalne 52 karty. Karty wydarzeń **nie mają Mocy i po użyciu znikają do odrzuconych**. Karty można posiadać 2 razy w pojedynkowym decku; maks. 6 wydarzeń w 18 kartach.

| ID | Wydarzenie | K | Dokładny efekt | Inspiracja |
|---|---|---:|---|---|
| E01 | **Ostatni Ogórek** | 1 | Wzmocnij własną jednostkę o +1. Jeśli jest na ZAPLECZU, dodatkowe +1. | Ogórek przetrwa, choć Tabo na Caution nadal się nie leczy. |
| E02 | **Ink Ribbon** | 1 | Dobierz 1 kartę. Nie możesz zagrać więcej wydarzeń w tej turze. | Z Ink Ribbonem nie biegamy. |
| E03 | **Przestaw Kreskę Zasięgu** | 1 | Przesuń własną jednostkę do sąsiedniej strefy z miejscem. | Zasięg znika w połowie zdania. |
| E04 | **Nie Ma Litery A** | 1 | Wzmocnij własną jednostkę o +1; jeśli to Gumbox, +2 zamiast +1. | Gamboksik protestuje. |
| E05 | **Proszek z RE** | 1 | Nadaj Ochronę wybranej własnej jednostce. | Wszystkie proszki obowiązkowo. |
| E06 | **Spokojny RSKS** | 1 | Wzmocnij własną jednostkę Hymn o +2. | Rodzinny, spokojny, kameralny; pozornie. |
| E07 | **Pora Zrobić Porządek** | 2 | Osłab wrogą jednostkę w wybranej strefie o −2. | Sprzątanie taboretowej rzeczywistości. |
| E08 | **Nic Tu Nie Działa** | 2 | Wycisz wrogą jednostkę z Aurą lub Finałem. | Krótka awaria, długa historia. |
| E09 | **Do Pieca!** | 2 | Wzmocnij 2 własne jednostki na ZAPLECZU po +1. | Bez LtAsii nawet ogień ma regulamin. |
| E10 | **Podaj Pilota** | 2 | Przesuń własną jednostkę do dowolnej strefy z wolnym slotem. | Nowa meta: plecy do ekranu. |
| E11 | **Dwie Minuty Do Hymnu** | 2 | Umieść znacznik +2 w strefie, gdzie masz jednostkę Hymn. | Próba mikrofonu przed 20:30. |
| E12 | **Mały Ban** | 2 | Usuń wrogi żeton o Mocy 2 lub niższej; jeśli nie ma żetonu, osłab jednostkę o −1. | To tylko timeout. |
| E13 | **Proplayer Gloves** | 3 | Wzmocnij własną jednostkę o +3. | Rękawiczki uruchamiają tryb pro. |
| E14 | **Sprawdź Płyty** | 3 | Dobierz 2 karty; odrzuć 1 wybraną kartę z ręki. | Bez książeczki do PSX nie wpuszczamy. |
| E15 | **Finał Finałów** | 3 | Umieść znacznik +3 w wybranej strefie, jeśli to twoja tura 5 lub 6; inaczej +1. | Finał, który może mieć pre-finał. |
| E16 | **Dziękuję, Czat** | 3 | Wzmocnij 2 różne własne jednostki Widz po +1. | Wszyscy chwaleni, na chwilę. |
| E17 | **Zerwany Internet** | 3 | Przesuń jedną wrogą jednostkę o drukowanej Mocy maks. 4 do sąsiedniej strefy z miejscem. | Łączność nie była tego warta. |
| E18 | **Mikami Patrzy** | 3 | Wzmocnij swoją jednostkę Horror o +3. | Niech patrzy jak gramy na HARD. |
| E19 | **Kto Zjadł Obwarzanek?** | 2 | Wzmocnij własną jednostkę Retro o +2 i dobierz 1 kartę, jeśli kontrolujesz Obwarzanek. | Tajemnica piekarni. |
| E20 | **Beczka ASMR** | 3 | Osłab do 2 wrogich jednostek w jednej strefie po −1. | Ściszacz emocji. |
| E21 | **Wysoki Sądzie, Protest** | 4 | Usuń wrogą jednostkę o drukowanej Mocy 3 lub niższej. | Rozprawa i protest w jednym. |
| E22 | **Wiadomość 10k** | 3 | Umieść znacznik +2 na CZACIE i dobierz 1 kartę. | Dycha komentarzy potrafi ważyć. |
| E23 | **Kawa z Wiertarki** | 2 | Wzmocnij własną Technika o +2; jeśli brak Technika, daj +1 dowolnej swojej jednostce. | Improwizacja i kofeina. |
| E24 | **Archiwizuj TaboLOG** | 4 | Umieść znacznik +2 w dwóch **różnych** strefach, w których masz co najmniej 1 jednostkę (jeśli tylko jedna, +2 tam). | Kronika Turnieju odnotowuje kolejną karcianą aferę. |


**Ważna reguła kosztów wydarzeń:** Wydarzenie kosztuje Energii tyle, ile karta jednostki, ale zamiast stałej Mocy dostarcza precyzyjnie ukierunkowany efekt. Wstępne ograniczenie „maks. 6 wydarzeń w 18” chroni przed talią pozbawioną sposobu wygrania stref. Wydarzenia E07, E08, E17, E21 powinny dostać priorytetowe testy, gdyż kontrola przeciwnika jest zwykle mocniejsza niż czysta Moc.

## 5.1. Przykładowe talie gotowe (18 kart każda)

**Startowa talia tutorialu / pierwszego rewanżu (wszystkie typy dostępne od początku):** 2× Palec Przeznaczenia; 2× Taboret Przeznaczenia; 2× Obwarzanek; 2× QrusKnur; 2× Święty Headset; 2× Clip Moment; 2× TaboRanek; 1× Prorok Tabo; 1× E01 Ostatni Ogórek; 1× E07 Pora Zrobić Porządek; 1× E03 Przestaw Kreskę Zasięgu. **18 kart = 15 jednostek + 3 wydarzenia; maks. 2 kopie.** Skryptowana kolejność w tutorialu różni się od normalnego tasowania tej talii.

**„ModeRACJA”:** 2× LtAsiaa; 2× Nysmo; 2× Banhammer; 2× Jillie; 2× Taboret Przeznaczenia; 2× Top Chatter; 1× KruparGames; 1× Palec Przeznaczenia; 1× QrusKnur; 1× Mały Ban; 1× Nic Tu Nie Działa; 1× Dziękuję, Czat. Suma 18.

**„Hymniarze”:** 2× MaciekWolf92; 2× Hymn; 2× Meeefjuuu; 2× TaboRanek; 2× Cozy ASMR; 2× Święty Headset; 2× Taboret Przeznaczenia; 1× Prorok Tabo; 1× Dwie Minuty Do Hymnu; 1× Spokojny RSKS; 1× GreedN3. Suma 18.

**„Horror na HARD”:** 2× Wampir z Podlasia; 2× Męczony Kapucynek; 2× TRUP-POL S.A.; 2× Zombie z Rekinem; 2× Nyravespera; 2× Obwarzanek; 1× Ptak z Dark Souls; 1× Wodny Wąż; 1× Palec Przeznaczenia; 1× Mikami Patrzy; 1× Ostatni Ogórek; 1× Pora Zrobić Porządek. Suma 18.

Pierwsza z nich to wzorzec projektowy, nie narzucony zestaw od pierwszej sekundy; automatycznie zastępuj niedostępne typy kartami o tym samym koszcie z posiadanej puli, zachowując strukturę energii.

---

# 6. Scenariusz główny - kampania „Puchar PROPLAYERA”

## 6.1. Wstęp fabularny i struktura

**Prolog (krótka animacja lub napisy, można pominąć):** Tabo pokazuje widzom fizyczne Karty TABOta. Ktoś z Czatu rzuca wyzwanie, a Tabo odpowiada: „Przecież to są MOJE karty. Jak ja mam przegrać we własną grę?”. ELTaboBot traktuje tę wypowiedź jako oficjalne zgłoszenie do turnieju. Na ekranie pojawia się „PUCHAR PROPLAYERA - ZGŁOSZENIE PRZYJĘTE” i licznik **20 wyzwań**. Bot odczytuje punkt 20:30 regulaminu, którego Tabo oczywiście nie czytał.

> **TABO:** „Jakiego regulaminu?!”  
> **ELTABOBOT:** „Tego, którego nie przeczytałeś.”  
> **TABO:** „Nic tu kurła nie działa!”  
> **ELTABOBOT:** „Turniej uruchomiono pomyślnie.”

**Stawka:** główna nagroda to **Złoty Taboret** i przyznany przez społeczność tytuł **PROPLAYERA**. Porażka oznacza wyłącznie sportową kompromitację i możliwość rewanżu. ELTaboBot nie usuwa widzów ani nie niszczy rzeczywistości: jest sumiennym, przesadnie literalnym organizatorem, który sam stanie się finałowym przeciwnikiem.

**Struktura:** 4 akty × 5 wyzwań. Wszystkich 20 oryginalnych przeciwników, ich unikalne zasady, talie, nagrody i kolejność pozostają niezmienione. Każdy uczestnik prezentuje własny styl. TaboLOG jest **Kroniką Turnieju**: zapisuje historię stolików i zdobyte pieczątki zamiast odzyskiwanych wspomnień.

- **Akt I - Ty w ogóle umiesz w to grać? (01–05):** szkolenie, retro, regulamin litery A, Hymn i spam Jillie. Po 05 bot ogłasza, że zakończył się dopiero etap podstawowy.
- **Akt II - Każdy ma własną metę (06–10):** zagadki, nocna kierownica, SIEMA, bliźniaki i noc horroru. Po 10 Tabo dostaje jedynie certyfikat „BRĄZOWY TABORET”.
- **Akt III - To nie jest koncert życzeń (11–15):** wertykalność, śmigłowiec, muzyka, retro i komentarze. Po 15 pojawia się fałszywy napis „FINAŁ TURNIEJU!”.
- **Akt IV - Ostateczny finał. Naprawdę. Chyba. (16–20):** siódma tura Pierd0li, kontrola ModeRACJI, audyt, stara szkoła i jawne techniczne zakłócenia ELTaboBota.

**Mapa:** 20 turniejowych stolików i aren, ułożonych w cztery akty. Nie są to punkty geograficzne ani miejsca z innej gry. Kolejne zwycięstwa dostarczają pieczątek, nowych kart, wpisów do Kroniki i kolejnych rywali. Dialogi są nowymi autorskimi kwestiami postaci, a nie cytatami z rzeczywistych osób.

**Schemat wyzwania:** prezentacja przeciwnika → humorystyczny kontekst → jawny warunek wyzwania → pojedynek → pieczątka, karty i wpis do Kroniki → kolejny stolik. Rewanże i tryb wróżb pozostają niezależne od fabularnego wyniku.

## 6.2. Głosy i status kwestii

Wszystkie kwestie w dalszych rozdziałach to **oryginalnie napisane dialogi dla fikcyjnych awatarów**. Jeśli realni członkowie społeczności nie chcą nagrywać tekstów, głosówki można zastąpić napisem + charakterystycznym, licencjonowanym krótkim dżinglem. **Nie klonować głosów realnych osób bez ich świadomej zgody.** Każdy dialog ma wyzwalacz `START`, `WR`, `LEAD` (wygrywa 2 strefy na koniec tury 3–5), `TRAIL` (przegrywa 2 strefy na koniec tury 3–5), `LOSE` (porażka AI), `WIN` (zwycięstwo AI); odtwarza się maksymalnie raz na stan/partię, nie przerywa wejścia na kartę, daje się pominąć. Priorytet komunikatów: rozstrzygnięcie > WR > strefa > zwykły komentarz.

**Zasada fairness:** „prowadzenie” w turach 1–5 to informacyjna przewaga, nie prognoza pewnego zwycięstwa. W grze pojawia się etykieta `AKTUALNIE WYGRYWA`, nie `JUŻ WYGRAŁEŚ`.

---

## 6.3. Dwadzieścia wyzwań Pucharu - przeciwnicy, mechaniki, scenariusz, dialogi

Poniższe WR-y **są nakładkami na te same zasady rdzeniowe**. Opisy efektów, w szczególności powtarzalność, turę wystąpienia, stronę działania i sposób rozstrzygania remisu, są obowiązujące. Sceny dialogowe służą jako gotowy scenariusz do napisów lub nagrania (kwestie są autorskie, nie archiwalne). Przy każdej misji w NORMAL system podaje startową talię z dostępnych kart; tabela odblokowań nie oznacza, że gracz musi ją zbudować ręcznie.

### Rozprawa 01/20 - ToTylkoNysmo - Kontrola Wejścia

**Akt:** I · **Sceneria:** Poczekalnia Pucharu PROPLAYERA · **Mechanika na planszy:** `PRÓBA SEZONOWCA`

**Sytuacja fabularna.** ToTylkoNysmo pełni dyżur w poczekalni turniejowej. Uparł się, że Tabo jest największym sezonowcem we własnej grze, więc zanim dopuści go do Pucharu, pokaże mu zasady.

**Unikalny Warunek Rozprawy:** PRÓBA SEZONOWCA: w turach 1–3 Nysmo odkrywa swój zaplanowany ruch PRZED zatwierdzeniem ruchu Tabo (wyjątek informacyjny tylko tutorialu). Ekran wskazuje legalne pola i koszt kart; po turze 3 obie strony wracają do zwykłego ukrytego planowania.

**Co robi gracz:** Rozegraj 6 skryptowanych tur i wygraj 2 strefy. Po samouczku można od razu powtórzyć mecz w pełni losowym rozdaniu.

**Taktyka AI i lekcja:** Tutor blokuje błędne ruchy wyłącznie w pierwszych trzech turach i uczy kolejno kosztów, stref, dodatkowej punktacji. Nie wprowadza efektów usuwania ani dociągu.

**Remix PROPLAYER:** W HARD (rewanż): pierwsza Moderacja zagrana na CZAT w każdej turze otrzymuje +1 Mocy (symetrycznie).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **08 ToTylkoNysmo - Moderacja, 11 GreedN3 - Dawca Wspomnień, 14 Tabarzak - Brat Krwi**, wydarzenie **E02**; wpis TaboLOG nr 01. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Zanim dostaniesz bana, pokażę ci, jak się kładzie karty.”
- **WR** - „Pierwsze trzy tury przeprowadzę cię za rękę. Potem spróbujesz sam.”
- **LEAD** - „O, sezonowiec się uczy! Zobaczymy po zakończeniu tury.”
- **TRAIL** - „Nie szkodzi. Wygrać trzeba dwie strefy, nie wszystkie trzy.”
- **LOSE** - „Szkolenie zaliczone. Możesz wejść do turnieju, PROPLAYERZE.”
- **WIN** - „Na razie zostajesz w poczekalni. Zaczniemy jeszcze raz.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 02/20 - GreedN3 - Retro Sprawdzian

**Akt:** I · **Sceneria:** Retro-stolik i kasety VHS · **Mechanika na planszy:** `PIERWSZE WSPOMNIENIE`

**Sytuacja fabularna.** GreedN3 zaprasza Tabo na retro-pojedynek przy półce z kasetami VHS. Sprawdza, czy doświadczenie ze starych gier pomaga także w planowaniu tur i rozsądnym używaniu kart Retro.

**Unikalny Warunek Rozprawy:** PIERWSZE WSPOMNIENIE: pierwsza twoja karta Retro zagrana w meczu otrzymuje +2 Mocy (każda strona osobno).

**Co robi gracz:** Wygraj pojedynek; pobocznie zagraj kartę Retro i obserwuj zielony znacznik +2.

**Taktyka AI i lekcja:** Uczy rozpoznawania tagów i pojedynczych efektów WR. Greed ma więcej kart Retro, ale Tabo może wykorzystać tę samą regułę.

**Remix PROPLAYER:** W HARD bonus +2 otrzymuje tylko pierwszy Retro położony na ZAPLECZU (i tu obowiązuje symetrycznie).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **03 Tabożeństwo, 23 AL_PSX - Bez Piwnic**, wydarzenie **E04**; wpis TaboLOG nr 02. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Stare gry nauczyły mnie jednego: nie marnuj najlepszej karty na pierwszą lepszą głupotę.”
- **WR** - „Karta Retro na początku potrafi zbudować świetną przewagę.”
- **LEAD** - „Dobrze liczysz. Na starych grach też nie dało się klikać bezmyślnie.”
- **TRAIL** - „Nie marnuj ruchów. Retro premiuje cierpliwość.”
- **LOSE** - „No proszę. Retro w dobrych rękach.”
- **WIN** - „Rewanż? Te stare karty mają jeszcze kilka sztuczek.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 03/20 - Gumbox - Inspekcja Litery A

**Akt:** I · **Sceneria:** Gabinet Gamboksika · **Mechanika na planszy:** `NIE WIDZĘ A`

**Sytuacja fabularna.** Gumbox przynosi własny regulamin stolika: ważniejsza od Mocy bywa litera A. Tabo odkrywa, że turniej oficjalnie dopuszcza najbardziej absurdalne zasady, byle ogłoszono je przed grą.

**Unikalny Warunek Rozprawy:** NIE WIDZĘ A: pierwsza własna jednostka bez litery „A” w nazwie (polskie znaki liczą się jak zwykłe litery), zagrana na CZACIE w każdej turze, dostaje +1 (symetrycznie).

**Co robi gracz:** Wygraj mecz, wykorzystując co najmniej raz bonus bez „A”.

**Taktyka AI i lekcja:** Nauka warunków opartych o nazwę; interfejs automatycznie podświetla karty kwalifikujące się do bonusu.

**Remix PROPLAYER:** W HARD również ostatnia jednostka z literą A zagrywana na CZACIE w danej turze traci −1 (symetryczny jawny efekt; minimalnie 0).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **30 Gumbox - Gamboksik, 24 Magiccorn - Magiczna Kukurydza**, wydarzenie **E06**; wpis TaboLOG nr 03. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Nie widzę tutaj żadnego A. Pan Gamboksik zatwierdza rozgrywkę.”
- **WR** - „Sprawdzaj, czy nazwa twojej karty ma literę A. To naprawdę cały mój regulamin.”
- **LEAD** - „Wygląda, że nawet alfabet dziś sprzyja twojej talii.”
- **TRAIL** - „Zajrzyj do nazw, zanim położysz kolejną kartę.”
- **LOSE** - „Regulamin zatwierdzony. Litera A nie protestuje.”
- **WIN** - „Zapraszam po ponowne zaliczenie alfabetu.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 04/20 - MaciekWolf92 - Strażnik Hymnu

**Akt:** I · **Sceneria:** Katedra Godziny 20:30 · **Mechanika na planszy:** `BACZNOŚĆ 20`

**Sytuacja fabularna.** MaciekWolf92 przerywa przejście Tabo do kolejnej rundy, bo ceremonia 20:30 odbyła się bez Hymnu. To pierwsza lekcja Rytuału, który odtąd staje się częścią turniejowej strategii.

**Unikalny Warunek Rozprawy:** BACZNOŚĆ 20:30: od tej misji w 4. turze obie strony wybierają Rytuał. Dodatkowo pierwszy Hymn zagrany na STREAM w całym meczu ma +1 (na stronę).

**Co robi gracz:** Rozegraj pojedynek i wybierz jedną z trzech akcji Rytuału; pokaż graczowi przewidywany efekt przed kliknięciem.

**Taktyka AI i lekcja:** Tutorial rozdziałowy: na początku 4. tury ekran zwalnia, otwiera 3 karty Rytuału, narracja objaśnia koszty 0 i konsekwencje.

**Remix PROPLAYER:** W HARD wybór Rytuału zostaje ujawniony dopiero po zatwierdzeniu planów obu stron; w NORMAL widać wybrany typ AI przed potwierdzeniem jako szkoleniową podpowiedź.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **13 MaciekWolf92 - Strażnik Hymnu, 39 Hymn**, wydarzenie **E08**; wpis TaboLOG nr 04. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Wszystko pięknie, ale HYMNU NIE BYŁO!”
- **WR** - „Rytuał 20:30 jest darmowy, ale tylko raz. Wybieraj uważnie.”
- **LEAD** - „Jeśli utrzymasz tę przewagę, Hymn będzie o tobie.”
- **TRAIL** - „Odpowiedni Rytuał może jeszcze odmienić wynik.”
- **LOSE** - „Hymn był. Wygrałeś. W porządku, zaliczam.”
- **WIN** - „Hymn musi zabrzmieć jeszcze raz. Poprawka!”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 05/20 - Jillie_Studio - Królowa Spamu

**Akt:** I · **Sceneria:** Arena Czatowej Lawiny · **Mechanika na planszy:** `LAWINA EMOTEK`

**Sytuacja fabularna.** Jillie_Studio ogłasza się królową pierwszej rundy i zasypuje Czat emotkami. Wygrana wymaga równowagi między strefami, a nie tylko najgłośniejszego spamu.

**Unikalny Warunek Rozprawy:** LAWINA EMOTEK: pierwsza jednostka Widz zagrana przez każdą stronę na CZAT w każdej turze ma +1; kolejne w tej samej turze bez bonusu.

**Co robi gracz:** Wygraj mimo bardzo dużej punktacji Jillie na Czacie.

**Taktyka AI i lekcja:** AI buduje Czata, ale świadomie zostawia słabiej bronione Zaplecze. Uczy, że nie każdą strefę trzeba wygrywać.

**Remix PROPLAYER:** W HARD CZAT ma 5 slotów na stronę zamiast 4 - tylko w tym pojedynku (oba limity jawne).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **09 Jillie_Studio - Królowa Spamu, 42 Top Chatter, 45 Cozy ASMR**, wydarzenie **E09**; wpis TaboLOG nr 05. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „TY MYŚLISZ, ŻE MOŻESZ ZE MNĄ WYGRAĆ NA CZACIE?!”
- **WR** - „Przygotuj się na spam! Jeden Czat to nie cały pojedynek.”
- **LEAD** - „CO?! MOJE EMOTKI NIE POMAGAJĄ?!”
- **TRAIL** - „CZAT, JESZCZE WIĘCEJ EMOTEK!”
- **LOSE** - „CO?! KTO WYŁĄCZYŁ MOJE EMOTKI?!”
- **WIN** - „TAK TO SIĘ WYGRYWA NA CZACIE!”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 06/20 - QrusKnur - Zagadka KnurKnura

**Akt:** II · **Sceneria:** Tajemniczy Stolik Zagadek · **Mechanika na planszy:** `POSTAĆ ENIGMATYCZNA`

**Sytuacja fabularna.** QrusKnur rozstawia stolik zagadek. Twierdzi, że najważniejsza jest ta strefa, którą inni ignorują. Nie wyjaśnia swojej strategii, bo sam nie jest pewien, czy ją rozumie.

**Unikalny Warunek Rozprawy:** POSTAĆ ENIGMATYCZNA: po turach 3 i 5 każda strona dostaje znacznik +2 w swojej strefie z najmniejszą liczbą WŁASNYCH jednostek, o ile jest tam co najmniej 1 jednostka; remis rozstrzyga kolejność STREAM→CZAT→ZAPLECZE.

**Co robi gracz:** Przetrwaj obie falę bonusów; podświetlane strzałki pokazują przyszłą strefę zysku.

**Taktyka AI i lekcja:** Nauka przewidywania efektów końca tury, które są symetryczne. Unikamy elementu losowego.

**Remix PROPLAYER:** W HARD znaczniki pojawiają się także po turze 2, ale tylko +1 każdy.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **12 InfinityPotato0 - Toksyk Premium, 48 Wapniak - Hejt Prastary**, wydarzenie **E10**; wpis TaboLOG nr 06. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Myślisz, że znasz moją strategię? Ja też nie.”
- **WR** - „Spójrz na najmniej punktowaną strefę, zanim ją odpuścisz.”
- **LEAD** - „Najciekawsze rozwiązanie jest zazwyczaj najmniej oczywiste.”
- **TRAIL** - „Nie ignoruj strefy, która wydaje się przegrana.”
- **LOSE** - „Odnalazłeś odpowiedź. Ja wciąż szukam pytania.”
- **WIN** - „Zagadka rozwiązana. Przeze mnie.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 07/20 - Pestarz - Nocna Kierownica

**Akt:** II · **Sceneria:** Garaż o 03:00 · **Mechanika na planszy:** `NOCNA META`

**Sytuacja fabularna.** Pestarz urządza nocny mecz przy kierownicy. Kawa z wiertarki i stos dziwacznych kart sprawiają, że do wygranej przyda się zimna głowa, nawet o trzeciej nad ranem.

**Unikalny Warunek Rozprawy:** NOCNA META: pierwsza jednostka zagrana przez każdą stronę na ZAPLECZE w turze 1–3 otrzymuje +1. Jednorazowo na stronę w całym meczu.

**Co robi gracz:** Wygraj bez konieczności zagarnięcia całego CZATU; karta Pestarza premiuje zajmowanie pola jako pierwszy.

**Taktyka AI i lekcja:** Nauka inwestowania niskokosztowej karty wcześnie, kontra to późniejsze duże karty przeciwnika.

**Remix PROPLAYER:** W HARD karta na ZAPLECZU zagrana w turze 1 otrzymuje +2, w 2–3 już tylko +1; nadal tylko pierwsza na stronę.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **21 Pestarz - Kierownica o 3 w Nocy, 37 Wiertarka do Kawy**, wydarzenie **E11**; wpis TaboLOG nr 07. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Jedną ręką gram, drugą wiercę kawę. Co może pójść nie tak?”
- **WR** - „W nocy reguły nie śpią. Za to ty możesz przegapić bonus.”
- **LEAD** - „Dobra, może jednak trzeba było najpierw zrobić kawę.”
- **TRAIL** - „Przestaw kierownicę, nim ugrzęźniesz w tej strefie.”
- **LOSE** - „Wiercenie kawy przełożę na rewanż.”
- **WIN** - „Kawa jest mocniejsza od twojej talii.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 08/20 - Krisuroku - Okrzyk Zagłady

**Akt:** II · **Sceneria:** Amfiteatr SIEMA · **Mechanika na planszy:** `SIEMA KRISUROKU`

**Sytuacja fabularna.** Krisuroku wita Tabo na turniejowym amfiteatrze głośnym „SIEMA!”. Na jego arenie liczy się tempo, odważne ruchy i dobre wyczucie chwili.

**Unikalny Warunek Rozprawy:** SIEMA KRISUROKU: pierwszy koszt-3 zagrany przez każdą stronę na STREAM w każdej turze daje +1 Mocy swojej jednostce.

**Co robi gracz:** Wygraj, wykorzystując co najmniej jedną kartę kosztu 3 na Streamie.

**Taktyka AI i lekcja:** Uczy planowania krzywej Energii i efektu „następna karta” Krisuroku.

**Remix PROPLAYER:** W HARD zamiast warunku kosztu 3 liczy się karta Chaos (pierwsza zagrana na STREAM co turę).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **17 Krisuroku - Okrzyk Zagłady, 29 B4Nork - Wariacik**, wydarzenie **E12**; wpis TaboLOG nr 08. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „SIEEEEMA! DOBRA, TERAZ GRAMY!”
- **WR** - „Najgłośniejsze wejście nie zawsze jest najlepszym zagraniem.”
- **LEAD** - „Ładne zagranie. SIEMA dla takiej taktyki!”
- **TRAIL** - „SIEMA! TRZEBA SZYBCIEJ PODEJMOWAĆ DECYZJE!”
- **LOSE** - „SIEMA! DOBRY MECZ, TABO!”
- **WIN** - „SIEEEEMA! ZAGRAJ JESZCZE RAZ!”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 09/20 - Cydyn - Dwa Imiona

**Akt:** II · **Sceneria:** Stolik Bartka i Wojtka · **Mechanika na planszy:** `BLIŹNIACZY PRZYDZIAŁ`

**Sytuacja fabularna.** Cydyn przyprowadza symboliczne wsparcie Bartka i Wojtka. Przy tym stoliku wolne miejsca na planszy są równie ważne jak Moc, bo bliźniaki szybko zapełniają strefy.

**Unikalny Warunek Rozprawy:** BLIŹNIACZY PRZYDZIAŁ: po rozpatrzeniu tury 3, jeżeli na CZACIE są wolne sloty, każda strona otrzymuje żeton BLIŹNIAK 1 Mocy (jeżeli brak miejsca, nie otrzymuje).

**Co robi gracz:** Utrzymaj wolne miejsce na Czacie po turze 3 albo świadomie poświęć żeton dla innej strategii.

**Taktyka AI i lekcja:** Pokazuje, że miejsca w strefie są zasobem. AI specjalnie robi miejsce na własne bliźniaki.

**Remix PROPLAYER:** W HARD żeton trafia do strefy z najmniejszą sumą własnej Mocy; remis: CZAT→STREAM→ZAPLECZE.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **50 Cydyn - Ojciec Bliźniaków, 28 Orzechowy Rozpruwacz - Taboretograf**, wydarzenie **E13**; wpis TaboLOG nr 09. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „A co powiesz na dwóch dodatkowych zawodników?”
- **WR** - „Dwa żetony potrafią zająć więcej miejsca niż myślisz.”
- **LEAD** - „Bartek, Wojtek, proszę policzyć wolne pola.”
- **TRAIL** - „Zaraz zabraknie wolnych miejsc. Widzisz to?”
- **LOSE** - „Bartek i Wojtek potwierdzają wynik. Tym razem.”
- **WIN** - „W tej rodzinie nikt nie marnuje żetonów.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 10/20 - Wampir z Podlasia - Nocne Ssanie

**Akt:** II · **Sceneria:** Nocna Arena Horrorów · **Mechanika na planszy:** `NOC`

**Sytuacja fabularna.** Na specjalny wieczór horroru przybywa Wampir z Podlasia. Gra z wampirycznym awatarem, który zachowuje najgroźniejsze sztuczki na końcówkę pojedynku.

**Unikalny Warunek Rozprawy:** NOC: od początku tury 5 pierwsza własna jednostka Horror zagrana na STREAM w turze 5 lub 6 otrzymuje +2 (osobno dla każdej strony, raz na mecz).

**Co robi gracz:** Rozegraj mecz, pamiętając o tzw. późnej turze Horror; nie przeznaczaj całej Energii na wczesny Stream.

**Taktyka AI i lekcja:** Uczy planowania wysokokosztowych kart na turę 5 i rozumienia warunku przyszłej tury.

**Remix PROPLAYER:** W HARD bonus przenosi się na ZAPLECZE i jest aktywny tylko w turze 6; informacja jest jawna od wejścia.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **35 Wampir z Podlasia, 44 Wodny Wąż, 38 Zombie z Rekinem**, wydarzenie **E14**; wpis TaboLOG nr 10. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Jeszcze chwila, Taboret. Najlepsze zostawiam na noc.”
- **WR** - „Czasem warto zostawić mocniejszą kartę na później.”
- **LEAD** - „Jeszcze noc się nie skończyła. Nie ciesz się za wcześnie.”
- **TRAIL** - „Noc należy do cierpliwych. Jeszcze mamy czas.”
- **LOSE** - „Noc się kończy. Czas oddać zwycięstwo.”
- **WIN** - „Noc wzięła tę rundę. Możemy spróbować znowu.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 11/20 - B4Nork - Ludologiczny Wariacik

**Akt:** III · **Sceneria:** Wieża Wertykalnego Taboreta · **Mechanika na planszy:** `WERTYKALNOŚĆ`

**Sytuacja fabularna.** B4Nork otwiera wolną strefę turnieju. Jego wertykalne wyzwanie uczy, że przesunięcie jednej karty może przesądzić o wyniku lepiej niż największe wzmocnienie.

**Unikalny Warunek Rozprawy:** WERTYKALNOŚĆ: pierwsza własna jednostka PRZESUNIĘTA w meczu otrzymuje +2 Mocy (każda strona osobno).

**Co robi gracz:** Wygraj po przynajmniej jednym przesunięciu (Palec, Śmigłowiec, B4Nork lub wydarzenie).

**Taktyka AI i lekcja:** Uczy przemieszczania między strefami i rozróżniania bonusów bazowych od Aur.

**Remix PROPLAYER:** W HARD bonus +1 można otrzymać za pierwsze DWIE różne przesunięte jednostki (maks. +2 na stronę).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **27 Larond - Acziwkowy Spoceniec, 33 Męczony Kapucynek**, wydarzenie **E15**; wpis TaboLOG nr 11. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Wertykalność jest najważniejsza! Nawet w karciance!”
- **WR** - „Możesz przesuwać jednostki. Patrz, gdzie po ruchu zostanie wolne pole.”
- **LEAD** - „W pionie ci idzie. W poziomie zobaczymy.”
- **TRAIL** - „Wertykalność wymaga patrzenia do przodu.”
- **LOSE** - „Zwyciężyłeś w pionie i poziomie. Niebywałe.”
- **WIN** - „Pionowa przewaga zatwierdzona.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 12/20 - Kierowca Śmigłowca - Awaryjne Lądowanie

**Akt:** III · **Sceneria:** Lądowisko Nad Monitorem · **Mechanika na planszy:** `LOT OSTATNIEJ SZANSY`

**Sytuacja fabularna.** Kierowca Śmigłowca dostarcza pakiet kart specjalnych prosto nad arenę i od razu zgłasza się do gry. Zmiany pozycji stają się jego popisową taktyką.

**Unikalny Warunek Rozprawy:** LOT OSTATNIEJ SZANSY: w turze 4 każda strona dostaje jednorazowy DARMOWY przesuw jednej swojej jednostki do dowolnej strefy z miejscem; może pominąć.

**Co robi gracz:** Wygraj, ustawiając jedną jednostkę do przelotu w czwartej turze; brak jednostek nie blokuje gry.

**Taktyka AI i lekcja:** To pierwszy mecz, w którym gracz ma dodatkową akcję niezwiązaną z kartą ani Energią. Ikona LOT zawsze widoczna w HUD.

**Remix PROPLAYER:** W HARD przemieszczenie obowiązkowo wybiera się przed Rytuałem, bez znajomości wyboru przeciwnika.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **36 Kierowca Śmigłowca, 25 Andziaalek - Tirowiec**, wydarzenie **E16**; wpis TaboLOG nr 12. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Uwaga, zmiana pozycji. Proszę zabrać karty z lądowiska.”
- **WR** - „Lądowanie zmienia strefę, a z nią układ punktów.”
- **LEAD** - „Czyste lądowanie. Ale zaraz będą turbulencje.”
- **TRAIL** - „Zmiana pozycji może uratować ten mecz.”
- **LOSE** - „Lądowanie zatwierdzone. Zapisuję wynik.”
- **WIN** - „Wylądowałem pierwszy. Zapraszam do rewanżu.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 13/20 - Meeefjuuu - Koncert Życzeń

**Akt:** III · **Sceneria:** Studio Mikrofonów i Samplera · **Mechanika na planszy:** `BIS`

**Sytuacja fabularna.** Meeefjuuu zaprasza do studia muzycznego, zarzekając się, że to nie jest koncert życzeń. Minutę później przyjmuje prośbę o Hymn i zamienia pojedynek w bis.

**Unikalny Warunek Rozprawy:** BIS: jeżeli wybierzesz Rytuał HYMN w turze 4, jego znacznik daje +5 zamiast +3 (na obie strony).

**Co robi gracz:** Wygraj; docelowo zobacz co najmniej jedną interakcję Hymnu z bonusami kart.

**Taktyka AI i lekcja:** Nauka, że Rytuał może zmieniać rachunek sumy stref bardziej niż kolejny mały Widz.

**Remix PROPLAYER:** W HARD Rytuał POKAŻ KLIPA dobiera 3 zamiast 2 kart (również symetrycznie); gracze stają przed silniejszym dylematem.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **19 Meeefjuuu - Przebojowość, 46 500 Follow Special**, wydarzenie **E17**; wpis TaboLOG nr 13. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „To nie jest koncert życzeń. Chyba że masz jakieś życzenie.”
- **WR** - „Bis jest ważny, ale ostatecznie liczą się punkty i strefy.”
- **LEAD** - „Nieźle to brzmi. To może jednak będzie koncert.”
- **TRAIL** - „Nie każdy fałsz poprawisz jeszcze jednym Hymnem.”
- **LOSE** - „Dobrze zagrałeś. Przyznaję ci ten bis.”
- **WIN** - „To był mój bis. Dziękuję!”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 14/20 - AL_PSX - Kontrola Książeczek

**Akt:** III · **Sceneria:** Muzeum PSX bez Piwnic · **Mechanika na planszy:** `WERYFIKACJA PŁYT`

**Sytuacja fabularna.** AL_PSX organizuje egzamin z kultury retro. Pudełka, płyty i instrukcje leżą gotowe, a Tabo musi nauczyć się chronić kluczowe jednostki i pilnować kolejności zagrań.

**Unikalny Warunek Rozprawy:** WERYFIKACJA PŁYT: pierwsza jednostka Retro zagrana na ZAPLECZU w meczu otrzymuje Ochronę (oddzielnie dla każdej strony).

**Co robi gracz:** Wygraj. Pomocnicze zadanie: odpal Ochronę i zobacz animację zablokowanego debuffu.

**Taktyka AI i lekcja:** Uczy Ochrony i kontroli na ZAPLECZU bez dodawania nowych skomplikowanych stanów.

**Remix PROPLAYER:** W HARD Ochrona przysługuje pierwszej jednostce Retro położonej na dowolnej strefie, ale tylko gdy gracz posiada co najmniej 2 różne Retro w ręce w chwili zagrania (warunek prywatny, bonus widać po ujawnieniu).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **16 KroolRemizy - Ekspert Sztućców, 26 Drakson - Darmowe Woskowanie**, wydarzenie **E18**; wpis TaboLOG nr 14. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Gdzie książeczka? Bez książeczki nie ma pojedynku.”
- **WR** - „Pokaż wszystkie płyty i pamiętaj o Ochronie.”
- **LEAD** - „Dobrze. Teraz pokaż mi książeczkę.”
- **TRAIL** - „Gdy brak instrukcji, sprawdź Ochronę.”
- **LOSE** - „Płyty i książeczki są. Zaliczone.”
- **WIN** - „Bez książeczki nie ma zwycięstwa.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 15/20 - InfinityPotato0 - Toksyk Premium

**Akt:** III · **Sceneria:** Strefa Komentarzy · **Mechanika na planszy:** `SOLANKA KOMENTARZY`

**Sytuacja fabularna.** InfinityPotato0 czeka w strefie komentarzy pełnej prowokacji. Zbyt wiele kart w jednym miejscu może zaszkodzić, dlatego czasem najlepiej wygrać skromniejszym planem.

**Unikalny Warunek Rozprawy:** SOLANKA KOMENTARZY: po turze 4 w KAŻDEJ strefie, w której są co najmniej 2 jednostki danej strony, najsłabsza jednostka tej strony dostaje −1 (remis wybiera starszą). Każda strona jest rozliczana osobno.

**Co robi gracz:** Wygraj i wytrzymaj falę na końcu 4. tury; pokazuj na polach przewidywane ikony −1.

**Taktyka AI i lekcja:** Pierwsza lekcja przeciwko nadmiernemu spamowi małych kart. Przeciwnik może zostać ukarany przez własną regułę.

**Remix PROPLAYER:** W HARD rozliczenie następuje po turach 3 i 5 (maks. −2 na jednostkę).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **49 KubaFanBZP - BaniCzny Błazen, 40 Banhammer, 05 Psychosobota**, wydarzenie **E19**; wpis TaboLOG nr 15. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Nie wiem, jak możesz to przegrać, ale patrzę z zainteresowaniem.”
- **WR** - „Przepełniony stół może ci zaszkodzić.”
- **LEAD** - „Przyznaję, ten rozkład kart był zaskakująco nietoksyczny.”
- **TRAIL** - „Przepełnienie nie zawsze jest siłą.”
- **LOSE** - „W porządku. Przetrwałeś strefę komentarzy.”
- **WIN** - „Dziś komentarze należą do mnie.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 16/20 - Pierd0la - Finał Finałów

**Akt:** IV · **Sceneria:** Scena KONIEC? KONIEC! · **Mechanika na planszy:** `JESZCZE JEDEN FINAŁ`

**Sytuacja fabularna.** Pierd0la ogłasza wielki finał turnieju. Tabo już widzi napisy końcowe, ale okazuje się, że mecz ma jeszcze siódmą turę - a to dopiero początek fałszywych finałów.

**Unikalny Warunek Rozprawy:** JESZCZE JEDEN FINAŁ: mecz trwa **7 tur** zamiast 6. W 7. turze limit Energii wynosi 7, każdy dobiera dodatkową kartę, Finały uruchamiają się po turze 7.

**Co robi gracz:** Przetrwaj turę 7; naucz się zachowywać dużą kartę na końcówkę.

**Taktyka AI i lekcja:** Wyjątkowa zmiana długości jest znana od początku meczu i stale pokazana jako 1/7 … 7/7. Karty z opisem „tura 6” zachowują swój literalny warunek, a słowo Finał oznacza tu rozpatrzenie po 7.

**Remix PROPLAYER:** W HARD w turze 7 obowiązuje zakaz zagrywania wydarzeń, ale jednostki i Rytuał z 4. tury pozostają aktywne.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **22 Pierd0la - Wieczny Finał, 52 Madbbranko - Komórka Wątroby**, wydarzenie **E20**; wpis TaboLOG nr 16. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Już koniec? A nie, czekaj. Jeszcze jedna tura.”
- **WR** - „Na tym finale liczymy aż do siódmej tury. Naprawdę.”
- **LEAD** - „Prowadzisz? Nie przyzwyczajaj się, finałów tu dostatek.”
- **TRAIL** - „Mówiłem: do końca daleko, nawet w finale.”
- **LOSE** - „Dobrze, dobrze. To naprawdę był jeden z finałów.”
- **WIN** - „To już finał? Na pewno nie ostatni.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 17/20 - LtAsiaa - Najlepsza Młotkowa

**Akt:** IV · **Sceneria:** Trybuna ModeRACJI · **Mechanika na planszy:** `DECYZJA MODERACJI`

**Sytuacja fabularna.** LtAsiaa prowadzi kontrolę ModeRACJI przed końcowymi wyzwaniami. Zanim Tabo dostanie dostęp do Banhammera, musi dowieść, że potrafi pilnować Czatu bez paniki.

**Unikalny Warunek Rozprawy:** DECYZJA MODERACJI: pierwsza jednostka Moderacji wystawiona na CZACIE w meczu dostaje Ochronę i +1 Mocy (każda strona osobno).

**Co robi gracz:** Wygraj z umiejętną kontrowersją na Czacie. Po porażce podpowiedź: Aury można wyciszać przed rozliczeniem Finału.

**Taktyka AI i lekcja:** To test interakcji Ochrona-Wyciszenie-Osłabienie, a nie walka wyłącznie na duże cyfry.

**Remix PROPLAYER:** W HARD w 4. turze żadna ze stron nie może wybrać Rytuału BAN (pozostałe dwa działają).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **07 LtAsiaa - Młotkowa, 18 MackoTheHollow - Cozy Głos**, wydarzenie **E21**; wpis TaboLOG nr 17. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Tabo, ja cię naprawdę proszę. Nie graj tego tam.”
- **WR** - „Nie każdy Ban jest dobrym Banem. Spójrz na status celu.”
- **LEAD** - „W porządku, nie trzeba od razu używać Banhammera.”
- **TRAIL** - „Pilnuj Czatu. Banhammer nie rozwiąże wszystkiego.”
- **LOSE** - „Możesz zarządzać Czatem. Byle z umiarem.”
- **WIN** - „Kontrola ModeRACJI wykazała kilka uchybień.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 18/20 - KruparGames - Audyt Administratora

**Akt:** IV · **Sceneria:** Biuro Audytu Pucharu · **Mechanika na planszy:** `AUDYT`

**Sytuacja fabularna.** KruparGames przeprowadza oficjalny audyt turnieju. Weryfikuje uczciwość zagrań i sprawdza, czy Tabo radzi sobie także wtedy, gdy regulamin jest nieznośnie dokładny.

**Unikalny Warunek Rozprawy:** AUDYT: po turach 2 i 4 strona z wyższym wynikiem na ZAPLECZU otrzymuje tam trwały znacznik +1. Przy remisie nikt nie dostaje bonusu.

**Co robi gracz:** Zwycięż, pamiętając o punktach kontrolnych po turach 2 i 4.

**Taktyka AI i lekcja:** Ważny aspekt tempa: liczy się przewaga na konkretny moment. Znaczniki audytu są widoczne na osi tur.

**Remix PROPLAYER:** W HARD audyt następuje również po turze 6, ale Finały w normalnym 6-turowym meczu rozpatrują się PO audycie.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **51 KruparGames - Ojciec Admin, 34 TRUP-POL S.A.**, wydarzenie **E22**; wpis TaboLOG nr 18. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Po przeanalizowaniu logów stwierdzam, że problem jest między krzesłem a monitorem.”
- **WR** - „W audycie wygrywa ten, kto nie zgubił się w liczbach.”
- **LEAD** - „Kontrola wykazała przewagę. Proszę jej nie zmarnować.”
- **TRAIL** - „W logach widać błąd decyzyjny. Można go jeszcze naprawić.”
- **LOSE** - „Audyt zamknięty: Tabo gra zgodnie z zasadami.”
- **WIN** - „Audyt: zwycięstwo administratora. Zgodne z regulaminem.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 19/20 - Wapniak - Hejt Prastary

**Akt:** IV · **Sceneria:** Retro-Arena Woodstock ’76 · **Mechanika na planszy:** `STARY HEJT`

**Sytuacja fabularna.** Wapniak, ostatni rywal przed finałem, stawia na doświadczenie i klasyczne zagrania. Przekonuje, że więcej kart nie zawsze znaczy lepiej i że starych strategii nie należy lekceważyć.

**Unikalny Warunek Rozprawy:** STARY HEJT: gdy na koniec meczu strona ma 3 lub 4 własne jednostki w jednej strefie, otrzymuje tam **−2 punkty strefy** (nie osłabia kart; dotyczy obu stron).

**Co robi gracz:** Wygraj, rozkładając karty z głową: 2 duże jednostki mogą przewyższyć 4 malutkie.

**Taktyka AI i lekcja:** Mechanika anty-spamu jest symetryczna i jawna; nad punktacją każdej strefy wyświetla się potencjalna kara „−2 w finale”.

**Remix PROPLAYER:** W HARD kara zaczyna się już przy 2 jednostkach i wynosi −1; przy 3–4 jednostkach wynosi −3 (na stronę i strefę).

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **20 Nyravespera - Gocka Moc, 32 Ptak z Dark Souls**, wydarzenie **E23**; wpis TaboLOG nr 19. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „Za moich czasów to wystarczała jedna dobra karta.”
- **WR** - „Za dużo kart w jednej strefie bywa kiepskim planem.”
- **LEAD** - „Młodzi też czasem zagrają klasycznie.”
- **TRAIL** - „Jedno dobre zagranie może wygrać dwie strefy.”
- **LOSE** - „Stara szkoła uznaje to zwycięstwo.”
- **WIN** - „Klasyczna strategia nadal działa.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

### Rozprawa 20/20 - ELTaboBot - Test PROPLAYERA

**Akt:** IV · **Sceneria:** Studio Finałowe ELTaboBota · **Mechanika na planszy:** `NIC TU KURŁA NIE DZIAŁA!`

**Sytuacja fabularna.** Na wielkiej arenie finałowej pozostaje tylko jeden ukryty przeciwnik. ELTaboBot ujawnia, że to on - organizator turnieju. Symuluje typowe awarie transmisji, ale zapowiada zakłócenia z góry i poddaje obu graczy identycznym zasadom.

**Unikalny Warunek Rozprawy:** NIC TU KURŁA NIE DZIAŁA!: w turach 2, 4 i 6 po jednej wskazanej strefie wyłączane jest PIERWSZE zagrywane Wejście każdej strony (t2 STREAM, t4 CZAT, t6 ZAPLECZE). Dotyczy tylko Wejść z jednostek/wydarzeń, nie bazowej Mocy, Aur ani Rytuału. Efekt znika na końcu bieżącej tury, wskazana strefa jest zapowiedziana od początku meczu.

**Co robi gracz:** Wygraj finał, wykorzystując dwa z trzech pól i omijając aktywne zakłócenie albo zagrywając tam karty bez Wejścia.

**Taktyka AI i lekcja:** Remiks lekcji z kampanii: przenoszenie, Aury, Finały, Rytuał, Ochrona. Brak losowania pola „glitch”, wszystko jest oznaczone od początku.

**Remix PROPLAYER:** W HARD kolejność zakłóceń to t2 ZAPLECZE, t4 STREAM, t6 CZAT; AI ma lepiej zaplanowaną talię, ale obowiązują identyczne zasady.

**Nagroda za pierwsze zwycięstwo:** nowe karty oryginalne **47 ELTaboBot, 15 KokoszTsunami - Potężny Strimer**, wydarzenie **E24**; wpis TaboLOG nr 20. W fabule ukończenie automatycznie dodaje je do kolekcji; w HARD nagrodą są alternatywne ramki i jedna notatka fabularna, NIE nowe statystyki.

**Kwestie do nagrania lub wyświetlenia:**

- **START** - „OSTATNI UCZESTNIK: ELTABOBOT. Test PROPLAYERA rozpoczyna się teraz.”
- **WR** - „W turach 2, 4 i 6 wyłączamy pierwsze Wejście w oznaczonej strefie. Oboje znamy harmonogram.”
- **LEAD** - „ANALIZA: WYBRANO ZASKAKUJĄCO ROZSĄDNY PLAN.”
- **TRAIL** - „ANALIZA: PRZYDAŁOBY SIĘ MNIEJ IMPROWIZACJI.”
- **LOSE** - „WERYFIKACJA ZAKOŃCZONA. POZIOM UMIEJĘTNOŚCI: PROPLAYER.”
- **WIN** - „WYNIK: ELTABOBOT. REGULAMIN PRZEWIDUJE REWANŻ.”

**Reżyseria (niski koszt):** jedna statyczna plansza postaci z subtelną animacją 2D (oddech/poświata/tilt), jedno dźwiękowe potwierdzenie WR, osobny krótki sting zwycięstwa. Kwestie `LEAD/TRAIL` wymagają przynajmniej 3. tury i wyświetlają się maks. raz w każdej partii.

## 6.4. Finał i dwa zakończenia

**Przed wyzwaniem 20:** po pokonaniu Wapniaka Tabo widzi pusty stolik i napis „OSTATNI UCZESTNIK - TOŻSAMOŚĆ UKRYTA”. ELTaboBot ujawnia, że ostatni przeciwnik został dobrany po analizie wszystkich wcześniejszych meczów. Gdy Tabo pyta, kto nim jest, słyszy: „JESTEM NIM JA”. Bot ma wirtualną myszkę i katalog złych decyzji zawodnika.

**NIC TU KURŁA NIE DZIAŁA!:** dawne zakłócenia nie są próbą zniszczenia archiwum. To przygotowana przez organizatora, jednakowa dla obu stron symulacja technicznych problemów znanych ze streamów. W NORMAL tury 2/4/6 blokują pierwsze Wejście odpowiednio na STREAMIE/CZACIE/ZAPLECZU; w PROPLAYER kolejność jest inna, ale jawna. **Mechaniki bez zmian.**

**Zakończenie FABUŁA (NORMAL):** Tabo wygrywa finał; wszystkie 20 portretów rozbłyskuje, Złoty Taboret pojawia się na arenie. Napis: **TABORETRO - MISTRZ KART TABOta**. ELTaboBot ogłasza „Weryfikacja zakończona. Poziom umiejętności: PROPLAYER”. LtAsiaa prosi, by Tabo nie spadł z taboretu, Nysmo przypomina, że były to tylko 20 meczów, a Jillie żąda rewanżu. Tabo odmawia i ogłasza, że idzie zagrać w coś normalnego. Bot natychmiast wyświetla: „Odblokowano tryb PROPLAYER. Czy rozpocząć ponownie?”. Krótkie instrumentalne outro.

**Zakończenie PROPLAYER (HARD):** alternatywny żart, niewymazujący pierwszego zwycięstwa: „CERTYFIKAT PROPLAYERA - POZIOM HARD ZALICZONY”. Bot chce wydrukować dyplom, drukarka odpowiada „NIC TU KURŁA NIE DZIAŁA!”. Istniejący silnik nadal kończy ten wariant takim samym triumfem; rozbudowany pojedynek lustrzany **TABO kontra TABO** i rewers „PRAWDZIWY PROPLAYER” pozostają opcjonalnym backlogiem, a nie obietnicą już wdrożonego systemu.

**Po zakończeniu:** kampania NORMAL zamyka się samodzielnie (bez konieczności HARD), pozostawia pełną kolekcję i rewanże. TaboLOG działa jako Kronika Turnieju i przechowuje pieczątki zwycięstw oraz charakterystyczne anegdoty ze stolików.

## 6.5. Krzywa nauki / przepustowość nowości

| Misje | Mechaniki, które gracz musi znać po przejściu | Czego jeszcze NIE trzeba uczyć |
|---|---|---|
| 01 | Tury, Energia, ręka, trzy strefy, liczenie punktów, koniec meczu | Rytuał, wydarzenia z usuwaniem, duble talii |
| 02–03 | Tagi, pasywne WR, budżet kart | Wieloetapowe combo i pełny deckbuilder |
| 04–05 | Rytuał 20:30, spam/kontra w dwóch strefach | Draft |
| 06–08 | Koniec tury, atrybuty przeciwnika, krzywa Energii | Złożone tury dodatkowe |
| 09–10 | Żetony, wolne sloty, planowanie Horror na późno | Ochrona przed finałowym audytem |
| 11–14 | Przesuwanie, darmowe akcje, synergia Rytuału, Ochrona | Kara anty-spam |
| 15–18 | Negatywne statusy, 7. tura, kontrola, punkty kontrolne | Glitch bota |
| 19–20 | Anty-spam, reset Wejścia, pełny miks systemów | - |

---

# 7. Kompletny poziom TUTORIALOWY - scenopis interakcji krok po kroku

**Cel:** w jednym bezpiecznym meczu gracz ma poznać cel, kartę i jej parametry, koszt Energii, przeciąganie/kliknięcie, trzy strefy, Aury, dociąg, cofanie planu, rozstrzygnięcie, punktowanie i możliwość przegrania jednej strefy. **Nie wprowadzamy w tutorialu Rytuału ani konstrukcji talii**, bo są osobnymi lekcjami fabularnymi. Przejście całego tutoriala ok. 8–12 minut przy czytaniu wszystkich opisów, szybki gracz 5–6 minut.

**Ustalony porządek losowania w tutorialu:** ręka startowa = Taboret Przeznaczenia, Święty Headset, QrusKnur, Clip Moment, Prorok Tabo; dociąg początku tury 2 = Ostatni Ogórek, tury 3 = Obwarzanek, tury 4 = drugi QrusKnur, dociąg z Clipa w turze 4 = drugi Święty Headset, tury 5 i 6 = pozostałe legalne karty. Skrypt respektuje liczby typów z powyższej talii i wprowadza niezbędne karty w odpowiednim momencie. W trybie zwykłym nie ma takiego ustawiania talii.

**Stan:** po „Nowa gra” ekran pyta „Pierwszy raz grasz w Karty TABOta?” z przyciskami `ZACZNIJ NAUKĘ` (domyślny) i `ZNAM JUŻ ZASADY` (przeskakuje do nieskryptowanego pojedynku z Nysmo, ale odblokowania za 01 nadal trzeba zdobyć). Progres tutoriala zapisuje `tutorialStep`. Każde okienko ma przycisk `POKAŻ JESZCZE RAZ`, a wszystkie objaśnienia dostępne są w późniejszym „Pomoc - zasady”.

### Scena T-00 - wejście

**Kadr:** stół w fioletowo-złotych kolorach, z prawej portret Nysmo, sędziego poczekalni turniejowej, z lewej mały portret Tabo. Pojawia się karta z wielkim napisem „GRASZ JAKO TABO”. 

- **NYSMO:** „Spokojnie, pokażę ci zasady. Nawet PROPLAYER musi wiedzieć, gdzie kliknąć.”
- **TABO:** „Przecież to moje karty. Co tu można zepsuć?”
- Pokaż trzy puste strefy, trzy wskaźniki 0:0, etykietę `WYGRYWAJ DOWOLNE 2 Z 3`.
- **Interakcja:** gracz musi najechać na każdą strefę lub kliknąć ją raz (na dotyku tylko kliknięcia), żeby wyskoczył krótki opis: STREAM = rozgrywka, CZAT = publiczność, ZAPLECZE = sprzęt/sekrety. Po trzech pokazach przycisk DALEJ.

### Scena T-01 - poznaj kartę

- Karta **Taboret Przeznaczenia (koszt 1, Moc 2)** wynurza się nad rękę z animacją 280 ms. Hover podnosi ją o 18 px, skala 1,12, pojawia się panel: `KOSZT 1 - ile Energii wydajesz; MOC 2 - ile punktów dokłada; AURA - bonus, jeśli obok jest inny Widz`.
- **NYSMO:** „Lewa cyfra kosztuje, prawa daje punkty. Nie zamieniaj ich.”
- **Akcja:** przeciągnij na STREAM lub kliknij kartę, potem slot STREAM. Inne strefy na 3 sekundy są przygaszone jako sugestia, ale po wyjaśnieniu możliwy jest reset tutoriala, nie trwała blokada.
- Bot zagrywa Obwarzanek na STREAM (2). Wynik 2:2; `REMIS STREFY NIE DAJE PUNKTU`.

### Scena T-02 - Energia i wybór celu

- Tura 2: licznik `2 / 2`; dobierz **Święty Headset (2/3)**; „Dobierasz 1 kartę na początku kolejnych tur”.
- Wybór headsetu i wystawienie na **CZAT**. Ponieważ jest jedyną własną jednostką na Czacie, aura +2: karta pokazuje `3 + 2 = 5`.
- Bot kładzie Palec Przeznaczenia na CZAT (2) bez przesunięcia. Wynik: STREAM 2:2, CZAT 5:2, ZAPLECZE 0:0.
- **TABO:** „O! Jedna karta i jest piątka. Czyli słuchawki naprawdę są święte.”
- Pop-up: `PUNKTY LICZĄ SIĘ W KAŻDEJ STREFIE ODDZIELNIE.`

### Scena T-03 - mocna jednostka i planowanie tur

- Tura 3: 3 Energia, dobierz QrusKnur (3/6). Zaznacz go i przeciągnij na **ZAPLECZE**.
- Bot zagra GreedN3 (3/4) na ZAPLECZE. Tabo ma przewagę w Czacie (5:2) i na Zapleczu (6:4).
- **NYSMO:** „Widzisz? Dwie strefy, a nie największy numerek gdziekolwiek.”
- Gracz wciska `PODGLĄD`, pojawia się log zagranych kart, liczby i niewykorzystanej Energii. Kliknięcie `?` na Qrus pokazuje brak umiejętności - pozytywna lekcja o prostych kartach.

### Scena T-04 - kilka kart w jednej turze i cofanie

- Tura 4: 4 Energia; gracz widzi przygotowane karty **Clip Moment (2/3)**, **Ostatni Ogórek (wydarzenie K1)** i **Obwarzanek (1/2)**.
- Podpowiedź „Karty możesz zagrywać **w dowolnej kolejności**, aż skończy się Energia”. Zalecane zagrania: Clip Moment na STREAM, Ostatni Ogórek jako +1 do Taboretu na STREAM, Obwarzanek na ZAPLECZE (tam ma Aurę +1).
- Po postawieniu Clipa wyświetl `Dobierz 1 kartę`; los w tutorialu jest ustalony, a gracz może obejrzeć nową kartę, nie musi jej zagrać.
- Po zagraniu Ogórka pulsuje przycisk `COFNIJ PLAN`, który **cofa ostatnią akcję** razem z efektem w podglądzie, ale nie przelicza przeszłych tur. Gracz cofa i ponownie wykonuje akcję, aby nauczyć się mechaniki.
- Bot dokłada Headset na STREAM i Headset na CZAT (każdy ma drukowaną Moc 3, bez samotnej Aury, bo są tam inne jednostki).
- **NYSMO:** „Ogórek leczy honor, nie HP. Tu masz punkty.”
- Koniec tury: Tabo STREAM 6, CZAT 5, ZAPLECZE 9; bot STREAM 5, CZAT 5, ZAPLECZE 4.

### Scena T-05 - Aura może zniknąć

- Tura 5: 5 Energia, gracz zagrywa drugiego QrusKnura (3/6) na CZAT i drugiego Świętego Headseta (2/3) na ZAPLECZE.
- Na Czacie wcześniejszy Headset przestaje być samotny, traci własne `+2`. UI pokazuje `AURA NIEAKTYWNA - obok inna twoja jednostka`, a punktacja Czatu zmienia się z podglądem `5 + 6 − 2 = 9`.
- Bot kładzie QrusKnura na STREAM i Obwarzanek na CZAT. Wyniki po turze (Tabo : bot): STREAM 6:11, CZAT 9:7, ZAPLECZE 12:4.
- **TABO:** „Czyli nie wystarczy dokładać wszystkiego wszędzie. Dobra, już rozumiem.”
- Komunikat: `PROWADZISZ W 2 STREFACH. STREAM MOŻESZ PRZEGRAĆ.`

### Scena T-06 - Finał i rozstrzygnięcie

- Tura 6: 6 Energia. Gracz otrzymuje **Proroka Tabo (6/8)**; wystawia go na STREAM. Podgląd karty pokazuje efekt Finału `+1 do każdej kontrolowanej przez ciebie strefy z jednostką, maks. 3`. Bot wystawia własnego Proroka na STREAM; nikt nie zna przyszłego wyniku do momentu ujawnienia, lecz tutorial podaje przykład w podpowiedzi.
- Przed zatwierdzeniem `KONIEC TURY` gracz widzi nad stołem informację `PO TEJ TURZE: FINAŁ` oraz rekapitulację planu.
- Ujawnienie, jeden po drugim `8`, `8`, błysk Finałów w trzech strefach (po +1 dla każdej strony mającej tam jednostkę). **Wynik końcowy TABO : BOT:** STREAM **15:20**, CZAT **10:8**, ZAPLECZE **13:5**. Wygrana TABO 2:1 na strefy.
- **NYSMO:** „Zauważ: przegrywasz Stream, ale wygrałeś cały mecz. Jest różnica!”
- **TABO:** „Pierwsza ważna rzecz, którą dziś powiedziałeś.”
- Na ekranie końcowym `ZALICZONO SZKOŁĘ PRZETRWANIA` i jawne odblokowania po misji 01.

**Ważna implementacja:** wszystkie wskazane karty mogą być „pożyczonymi egzemplarzami tutorialowymi”, bez przedwczesnego trwałego odblokowania. W normalnej partii od początku do końca używa się tej samej talii, a w tutorialu szczególne rozdanie ma być oznaczone `TRYB NAUKI - KOLEJNOŚĆ KART DEMONSTRACYJNA`. Aby uzyskać opisane liczby, pierwszy własny Obwarzanek stoi na ZAPLECZU i ma +1 z Aury; przeciwnik ma Obwarzanek na STREAM, więc nie otrzymuje tego bonusu. AI wystawia swoje karty dokładnie w kolejności T-01…T-06.

### Scena T-07 - trzyminutowa lekcja swobodna (opcjonalna)

Po zaliczeniu tutoriala gracz może wybrać `ZAGRAJ PRAWDZIWY REWANŻ`, z losowo tasowanymi rękami i prostym AI Nysmo. Nagroda za pierwszy tutorial już jest przyznana, więc nikt nie musi wygrać rewanżu, żeby kontynuować fabułę. Ten ekran daje szansę sprawdzić, czy gracz rozumie reguły poza skryptem.

## 7.1. Osobne szkolenie Rytuału i deckbuildera

**Przed rozprawą 04:** specjalna plansza: Maciek pokazuje `Rytuał HYMN (+3)`, `BAN (Wyciszenie)` i `POKAŻ KLIPA (dociąg 2)`, ilustrując przykładową sytuację: Tabo prowadzi 9:8 na Streamie, przegrywa 6:10 na Czacie i wygrywa 5:4 na Zapleczu. Gracz może podejrzeć wynik po Hymnie w wybranej strefie. Dopiero po zatwierdzeniu lekcji zaczyna się właściwy mecz.

**Przed HARD:** animowany deckbuilder ma siedem kroków: (1) porównaj 2 kopie, (2) zobacz kosztową krzywą talii, (3) wybierz 12 jednostek, (4) uzupełnij do 18 kart, (5) sprawdź limity, (6) zapisz preset, (7) zatwierdź; możliwość `AUTOUŁÓŻ` na każdym etapie. Wybór wstępnej gotowej talii pozostaje dostępny w HARD.

---

# 8. Kompletna mapa ekranów i nawigacja

## 8.1. Architektura przejść

```text
START / SPLASH
  └─ MENU GŁÓWNE
       ├─ NOWA GRA → wybór slotu / potwierdzenie nadpisania → Fabularna / Tutorial → mapa
       ├─ KONTYNUUJ [gdy istnieje zapis] → ostatni punkt, ekran walki lub mapa
       ├─ WRÓŻBY → NOWA WRÓŻBA → pytanie → tasowanie i cięcie → 1/3/5 → odsłanianie → zapis wyniku
       │           └─ HISTORIA → lista → szczegóły → podejrzyj każdą kartę → eksport/usuń
       ├─ KOLEKCJA / TALIE [po tutorialu] → katalog → deckbuilder → zapis presetu
       ├─ POJEDYNKI [po tutorialu] → wybór bossa / talii / AI → plansza
       ├─ OPCJE → grafika, audio, język, dostępność, dane lokalne
       ├─ ZASADY / TABOLOG → instrukcje + odblokowane wpisy
       └─ WYJŚCIE Z GRY (desktop) / ZAMKNIJ MENU (web)
```

**Wymagane przyciski główne z prośby:** NOWA GRA, KONTYNUUJ (tylko gdy zapis), WRÓŻBY, WYJŚCIE. Dodatkowe funkcje można schować w dolnym pasku `KOLEKCJA`, `OPCJE`, `ZASADY`, zamiast rozpychać pionową listę. Web nie ma kontroli nad zamknięciem karty przeglądarki; przycisk `Wyjście` w web wraca do ekranu tytułowego i wyświetla informację `Możesz zamknąć kartę przeglądarki`.

## 8.2. Specyfikacje każdego ekranu

| # | Ekran / stan | Co widać | Interakcje / przejścia / stany puste |
|---:|---|---|---|
| 01 | Splash / ładowanie | Logo Kart TABOta, krótka poświata pikselowej gwiazdy, postęp preloadu | Klik „pomiń”; jeśli asset brakuje - bezpieczny placeholder, nie wieczne kręcenie |
| 02 | Menu główne | Animowana talia, Tabo, neon, przyciski NOWA/KONTYNUUJ/WRÓŻBY/WYJŚCIE, dolny pasek | Hover: blask i lekki tilt, dźwięk; kontynuuj disabled z tooltipem „Nie znaleziono zapisu” |
| 03 | Nowa gra | Wybór spośród 3 lokalnych slotów, nazwa rozgrywki, FABUŁA/HARD (HARD początkowo zablokowany) | Potwierdzenie nadpisania i możliwość anulowania; żadnych domyślnie destrukcyjnych kliknięć |
| 04 | Wczytywanie / wybór slotu | Czas zapisu, ukończone rozprawy, aktualny rozdział, miniatura portretu | Kontynuuj / eksportuj / usuń za potwierdzeniem; odzysk z kopii awaryjnej |
| 05 | Mapa kampanii | 4 akty, 20 punktów, postacie, strzałki, stan ukończenia, wpisy w TaboLOGu | Hover po punkcie: postać, WR, zdobyte karty, poziom HARD; klik → briefing; zablokowany → warunek |
| 06 | Dialog fabularny | Portret z efektem 2D, nazwa, tekst w 2–3 liniach, opcjonalne audio/napisy | Klik i spacja = następny dialog; Escape = pomiń całość; log rozmowy; głośność postaci |
| 07 | Briefing przeciwnika | Nazwa WR, krótki przykład liczbowy, specjalne ikony, prognoza tur, nagrody, podgląd dostępnej talii | „ROZPOCZNIJ”, „CO ZNACZY?”, „ZMIEŃ TALIĘ” w HARD, powrót do mapy |
| 08 | Plansza meczu | 3 pasy, 2 × 12 slotów, dwa portrety, Energia, tury, talia/ręka/stos, log, Rytuał | Hover i drag/drop; legalne miejsca świecą, błędne pulsują; myszka nad liczbą pokazuje rozkład punktów; potwierdź plan |
| 09 | Zoom / tooltip karty | Oryginalna duża ilustracja, nazwa, K/M, tag, dokładny opis, historia efektów | Prawy przycisk/long press = przypnij; rolka przewija; porównaj dwie; ESC zamknij |
| 10 | Pauza | Wznowienie, zasady tej bitwy, opcje, zapisz i wyjdź do mapy, poddaj mecz | Zapisywany dokładny stan; poddanie wymaga potwierdzenia; HUD pod spodem zamrożony |
| 11 | Wynik - wygrana | Punktacja 3 pasów, Mecz 2:1, EXP brak (nie ma farmy), odblokowania, wpis TaboLOGu, dżingiel | Przyciski dalej/rewanż/podsumowanie ruchów/obejrzyj nową kartę |
| 12 | Wynik - porażka/remis | Ta sama rzetelna punktacja, krótkie wskazówki o dwóch decydujących turach | Rewanż z nowym seedem, obejrzyj log, zmień talię (HARD); brak utraty kolekcji |
| 13 | Katalog kart | Wszystkie 76 typów z filtrami i licznik odblokowane/całość | Hover rozkłada historię i wariant bojowy; nieodblokowane zasłonięte, źródło odblokowania widoczne |
| 14 | Deckbuilder | 18-slotowa lista talii, biblioteka, kosztowa krzywa, filtr tagów, limit kopii 2 | `+`, `−`, dwuklik, drag do listy, autoułóż, sortuj, zapisz/wczytaj do 8 presetów, waliduj |
| 15 | Karta - detale | Pełna oryginalna ilustracja i przełącznik WRÓŻBA/POJEDYNEK; plik źródłowy pochodzenia | Czytaj cytat, słowa-klucze i efekt bojowy osobno; powrót zachowuje filtr katalogu |
| 16 | Swobodny pojedynek | Lista ukończonych bossów, AI Easy/Normal/Hard, deck preset, przełącznik WR | Start / losowy przeciwnik / instrukcja; brak niezdobytych kart w katalogu gracza |
| 17 | Wybór HARD / draft | 24 oferowane karty, 18 docelowych, wskaźnik 12 jednostek / max 6 wydarzeń, plan przeciwnika | Klik `dodaj`, `usuń`, sortowanie, losuj ofertę raz na pojedynek, autoułóż, anuluj bez kary |
| 18 | Wróżby - start | Duża talia, przyciski NOWA WRÓŻBA / HISTORIA / INSTRUKCJA | Subtelne unoszenie kart po hover, brak zależności od kampanii |
| 19 | Wróżby - pytanie i rozkład | Pole wpisania pytania (opcjonalne), wybór 1/3/5, krótkie opisy układów | Walidacja 0–500 znaków, licznik, dalej/wstecz, lokalne prywatne dane |
| 20 | Tasowanie | 52 rewersy, animowane przesuwanie talii, tryb „tasuj” przyciskiem lub gestem | Tasuj ponownie, przyspiesz, pomiń animację; RNG nie zależy od animacji |
| 21 | Odcięcie lewą ręką | Talia w dwóch stosach i instrukcja symbolicznego odcięcia | Przeciągnij górną część na lewo lub klik `OTNIJ LEWĄ RĘKĄ`; bez obowiązkowego gestu ręką |
| 22 | Rozkład 1/3/5 | Zakryte karty na podpisanych polach; symboliczny blask i licznik odsłoniętych | Klik każdą kartę, flip 3D CSS/2D tween, powiększ, podgląd słów-kluczy |
| 23 | Wynik wróżby | Wszystkie karty na właściwych pozycjach, cytaty, hasła, interpretacja pozycji, pytanie | Zapis do historii, dodaj własną notatkę, eksport obrazka/JSON, ponowna wróżba |
| 24 | Historia wróżb | Lokalne wpisy od najnowszych, data, skrót pytania, tryb 1/3/5, liczba kart | Szukaj, filtruj po dacie/rozkładzie, eksportuj wszystko, usuń pojedynczy wpis po potwierdzeniu |
| 25 | Wróżba - szczegóły | Zapisane pytanie, dokładny układ, kolejność 1:1, każda grafika, własna notatka | Klik „PODEJRZYJ KARTĘ”, edytuj notatkę, kopiuj interpretację, usuń, wróć do tej samej pozycji na liście |
| 26 | Opcje | Audio głos/muzyka/SFX, jakość, pełny ekran, FPS, dostępność, zapis/eksport | Suwaki reagują natychmiast; `Przywróć domyślne` po potwierdzeniu; ustawienia niezależne od kampanii |
| 27 | Pomoc / TaboLOG | Zasady, tagi, słownik, samouczek do ponownego uruchomienia, odblokowane wpisy | Wyszukiwarka, filtry, przewijanie z utrzymanym stanem; skróty klawiaturowe |
| 28 | Autorzy i źródła | Podziękowania, źródła streamów, kredyty kart i audio, licencje bibliotek | Linki do źródeł; odtwarzanie klipów tylko gdy asset z prawem użycia |
| 29 | Wyjście / potwierdzenie | Informacja o zapisanym stanie i platformie, możliwość powrotu | Desktop: systemowe zamknięcie; Web: powrót do tytułu, bez obietnicy zamknięcia okna |

**Wszystkie ekrany działają myszką, klawiaturą i dotykiem, tam gdzie to możliwe.** Nie zakładaj, że hover jest konieczny do używania aplikacji. Dodatkowe informacje muszą być dostępne również po kliknięciu/long pressie oraz przez nawigację klawiaturą.

## 8.3. Plansza - układ rekomendowany (16:9)

```text
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ [≡]   TURA 04/06      ENERGIA TABO 4/4    RYTUAŁ: [HYMN] [BAN] [KLIP]     [?]        │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ OPONENT: JILLIE     ZASADA MECZU: LAWINA EMOTEK [i]       Talia: 8   Stos: 2         │
│                                                                                      │
│        STREAM                      CZAT                       ZAPLECZE               │
│    ┌───┬───┬───┬───┐        ┌───┬───┬───┬───┐         ┌───┬───┬───┬───┐              │
│ AI │ C │ C │   │   │     AI │ C │ C │ C │   │      AI │ C │   │   │   │              │
│    └───┴───┴───┴───┘        └───┴───┴───┴───┘         └───┴───┴───┴───┘              │
│          12 : 10                  08 : 17                    10 : 08               │
│    ┌───┬───┬───┬───┐        ┌───┬───┬───┬───┐         ┌───┬───┬───┬───┐              │
│ T  │ C │ C │ C │   │      T │ C │ C │   │   │       T │ C │ C │   │   │              │
│    └───┴───┴───┴───┘        └───┴───┴───┴───┘         └───┴───┴───┴───┘              │
│        [PUNKTY + ]               [PUNKTY − ]                [PUNKTY + ]              │
│──────────────────────────────────── TWOJA RĘKA ─────────────────────────────────────│
│ [karta] [karta] [karta] [karta] [karta] [karta]  [COFNIJ] [ZAKOŃCZ TURĘ]            │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

Kolor nie jest jedynym nośnikiem informacji: obok wyników są ikony `↑`, `↓`, `=` oraz etykiety „Prowadzisz / Przegrywasz / Remis”. Na monitorze o mniejszej rozdzielczości grę skalować proporcjonalnie; rękę przewijać poziomo i pozwolić przypiąć powiększenie. Nie ściskać oryginalnych pionowych ilustracji do nieczytelnej wysokości.

## 8.4. Stany UI - nie tylko ekrany

- `disabled` - półprzezroczyste, z tooltipem wyjaśniającym przyczynę („Za mało Energii”, „Brak wolnego slotu”, „Zablokowane do misji 04”).
- `hover` - skala / obrys / tilt, dźwięk maks. raz na wejście kursora; brak niekontrolowanego pulsowania.
- `selected` - karta 1.10–1.15×, strzałki do legalnych stref; prawy panel pokazuje dokładny efekt.
- `dragging` - przyczepiona do kursora duża karta, docelowe pola magnetyczne, ghost slot. Upuszczenie poza planszą powraca do ręki animacją.
- `pending` - plan jeszcze niezatwierdzony; wyraźne oznaczenie i przycisk „cofnij”.
- `committed` - brak możliwości edycji, przyjemna animacja sekwencji efektów; opcja `POMIŃ ANIMACJĘ` nie może zmienić rachunku.
- `resolve` - każda zmiana punktów ma kierunek, źródło i czytelny zapis w logu.
- `network-offline` - nie ma blokady gry ani wróżb; brak sieci to normalny, wspierany stan.
- `save-error` - wyraźna informacja, przycisk ponownego zapisu/eksportu, bez utraty aktualnego stanu.

---

# 9. Tryb WRÓŻBY - wierność oryginalnej instrukcji

## 9.1. Dwa zestawy danych - nigdy ich nie mieszać

- **Oryginalny TABOt:** zawsze dokładnie 52 unikatowe karty od 01 Prorok Tabo do 52 Madbbranko; bez statystyk pojedynkowych, bez kopii, bez kart wydarzeń E01–E24, bez warunków odblokowania.
- **Katalog bitewny:** odblokowywane 52 typy bazowe i 24 wydarzenia, możliwość dwóch kopii każdego typu w 18-kartowej talii.
- Ta separacja jest absolutna. Jeśli osoba odblokowała w kampanii zaledwie 15 kart, **we wróżeniu nadal ma 52**.

## 9.2. Rytuał zgodny z załączoną instrukcją

Instrukcja fizycznych Kart TABOta wskazuje: (1) potasowanie i skupienie na pytaniu, (2) odcięcie lewą ręką, (3) rozkład 1, 3 albo 5 kart, (4) interpretowanie tytułu, cytatu, słów-kluczy i ilustracji oraz odniesienie do streamowego kontekstu, (5) potraktowanie absurdalnej odpowiedzi z humorem. W grze ma to postać **uczciwego losowania bez powtórek w obrębie jednej wróżby**.

**Rozkłady:**

| Liczba | Dokładne pozycje | Co czyta gracz |
|---:|---|---|
| **1** | 1. Odpowiedź | Jeden symbol, jego cytat/hasła, krótka interpretacja do pytania. Przykładowe pytania: tak/nie/co dalej, bez udawania obiektywnego prorokowania |
| **3** | 1. **Przeszłość** · 2. **Teraz** · 3. **Przyszłość** | Każda karta mówi o swojej pozycji, następnie jedno zbiorcze podsumowanie łączące trzy obrazy |
| **5** | 1. **Sytuacja** · 2. **Problem** · 3. **Rada** · 4. **Chaos** · 5. **Finał** | Pięć podpisanych pól z sugestiami, na końcu jedna humorystyczna „wróżba streamerowa” |

**Odpowiedź w stylu fizycznej talii:** Tytuł = postać lub okoliczność; cytat = klimat, nie twarda przepowiednia; hasła z dołu karty = energia; obraz = dodatkowy żart i emocja. Jeśli karta jest zabawna, sugeruj lekkość; jeśli mroczna, ostrożność/pecha; jeśli przedstawia widza, rolę społeczności. Jeśli nic nie pasuje, wynik nadal jest symboliczną zabawą.

**Bez AI koniecznego do działania:** interpretator łączy napisane przez autorów 52 krótkie opisy z krótkim szablonem pozycji (9 szablonów = 1 + 3 + 5) oraz jedną z kilku puent. Pytanie użytkownika jest jedynie pokazywane w nagłówku i archiwum - generator nie musi go analizować ani nigdzie wysyłać. Dopuszczalny dodatkowy lokalny moduł wyboru kategorii pytania (praca/relacje/retro) wyłącznie po świadomym wyborze, ale nie jest potrzebny do v1.

## 9.3. Losowanie, odcięcie, powtórki

1. UI tworzy kopię listy 52 ID i tasuje Fisher–Yates przy użyciu lokalnego źródła losowości (`crypto.getRandomValues` w web, odpowiednik bezpiecznego generatora systemowego w desktop). Samo kręcenie kart jest animacją, **nie mechanizmem wynikowym**.
2. Gracz symbolicznie „odcina lewą ręką”: wybiera punkt podziału wizualnym gestem albo kliknięciem. Rotuj kolejność talii (cut), ale nie dodawaj ponownego losowania dającego powtarzające się ID.
3. Weź pierwsze 1/3/5 ID z potasowanej, uciętej listy. Każde ID może wystąpić **najwyżej raz w danej wróżbie**. Przy nowej wróżbie ta sama karta może oczywiście wrócić.
4. Zapisz kolejność ID bez zmian do historii, wraz z seedem tylko do debugowania (seed nie jest wymagany do ponownego otwarcia - wystarczą ID i ich pozycje).
5. Przy odsłanianiu nie losuj ponownie: wynik ustalony w momencie ułożenia zakrytych kart. Zamknięcie widoku w połowie: zapisz `revealedCount` i wróć do tego samego układu.

## 9.4. Jak opisać 52 karty w wróżbach - propozycje dopowiedzeń

**Uwaga:** poniższa kolumna to **nowe, humorystyczne dopowiedzenia autorów gry**, a nie cytaty z fizycznych kart. Oryginalne cytaty i słowa-klucze wyświetlaj bezpośrednio z grafiki; nie przepisuj na ślepo OCR-em, bo gra może pokazać niezgodny tekst. Numery dokładnie odpowiadają plikom w ZIP.

| # | Karta | Krótki motyw wróżebny (autorski) |
|---:|---|---|
| 01 | Prorok Tabo | Pytanie jest wielkie, ale odpowiedź może być mniejsza niż twój czat. |
| 02 | Palec Przeznaczenia | Czas wskazać kierunek, a potem przez moment tego nie żałować. |
| 03 | Tabożeństwo | Najpierw przyznaj się do własnego chaosu, potem porządkuj cudzy. |
| 04 | Święty Headset | Wycisz hałas i sprawdź, co naprawdę słyszysz. |
| 05 | Psychosobota | Świętuj sukces, ale trzymaj guzik do awaryjnego restartu. |
| 06 | Taboret Przeznaczenia | Usiądź i pomyśl: może nie trzeba biec za wszystkim naraz. |
| 07 | LtAsiaa - Młotkowa | Porządek nadejdzie, gdy ktoś wreszcie rozda właściwe bany. |
| 08 | ToTylkoNysmo - Moderacja | Pilnuj granic; nie każdy zombie to wróg. |
| 09 | Jillie_Studio - Królowa Spamu | Emocji jest dużo, lecz jedna ważna wiadomość może zniknąć w spamie. |
| 10 | QrusKnur - KnurKnur | Tajemnica czeka na człowieka, który nie musi wyjaśniać wszystkiego. |
| 11 | GreedN3 - Dawca Wspomnień | Wspomnienia są cenniejsze od kolejnego punktu w rankingu. |
| 12 | InfinityPotato0 - Toksyk Premium | Nie każda ostra krytyka zasługuje na odpowiedź. |
| 13 | MaciekWolf92 - Strażnik Hymnu | Tradycja pomoże, o ile nie zagłuszy zdrowego rozsądku. |
| 14 | Tabarzak - Brat Krwi | Sojusze pozwalają przetrwać więcej niż samotne bohaterstwo. |
| 15 | KokoszTsunami - Potężny Strimer | Twoja aura robi wrażenie - upewnij się, że to nie tylko reflektor. |
| 16 | KroolRemizy - Ekspert Sztućców | Daj sobie chwilę na kulturę, kawę i ułożenie sztućców. |
| 17 | Krisuroku - Okrzyk Zagłady | Odważnie przywitaj nową szansę, nawet jeśli reszta sali się zdziwi. |
| 18 | MackoTheHollow - Cozy Głos | Odpoczynek nie jest porażką i może dać najlepszą strategię. |
| 19 | Meeefjuuu - Przebojowość | Powiedz, o co ci chodzi, zanim świat wymyśli refren za ciebie. |
| 20 | Nyravespera - Gocka Moc | Mrok dodaje stylu, ale nie musi decydować o wyborze. |
| 21 | Pestarz - Kierownica o 3 w Nocy | Nocne pomysły czasem są genialne, lecz rano przeczytaj notatki. |
| 22 | Pierd0la - Wieczny Finał | Wielkie zakończenie może okazać się początkiem kolejnego finału. |
| 23 | AL_PSX - Bez Piwnic | Nie każda piwnica istnieje. Poszukaj dowodu, zamiast zgadywać. |
| 24 | Magiccorn - Magiczna Kukurydza | Mały absurd może stać się najważniejszą wskazówką. |
| 25 | Andziaalek - Tirowiec | Droga będzie długa; pilnuj kierunku i kolan. |
| 26 | Drakson - Darmowe Woskowanie | Nie wszystko wymaga dodatkowego woskowania, zwłaszcza plan awaryjny. |
| 27 | Larond - Acziwkowy Spoceniec | Ambicja jest piękna, ale nie musi być sportem ekstremalnym. |
| 28 | Orzechowy Rozpruwacz - Taboretograf | Kiedy trudno znaleźć miejsce, zbuduj własny taboret. |
| 29 | B4Nork - Wariacik | Skok daje perspektywę, lecz najpierw sprawdź, gdzie jest podłoga. |
| 30 | Gumbox - Gamboksik | Jeśli nie widzisz litery, może patrzysz na złą stronę problemu. |
| 31 | Obwarzanek | Proste przyjemności bywają skuteczniejsze niż dramatyczne przepowiednie. |
| 32 | Ptak z Dark Souls | Nie licz śmierci, policz wyciągnięte z nich lekcje. |
| 33 | Męczony Kapucynek | Upór jest siłą, ale gra nie zawsze musi trwać do świtu. |
| 34 | TRUP-POL S.A. | Papierologia potrafi przeżyć koniec świata; zachowaj kopię. |
| 35 | Wampir z Podlasia | Nie wysysaj z siebie resztek energii, żeby udowodnić cudzy punkt. |
| 36 | Kierowca Śmigłowca | Zmiana perspektywy przyjdzie szybciej niż wyjaśnienie lotu. |
| 37 | Wiertarka do Kawy | Jeśli narzędzie jest nie takie, ważne, by kawa ostatecznie powstała. |
| 38 | Zombie z Rekinem | Absurd może wpływać na wynik, nawet jeśli krąży obok rekin. |
| 39 | Hymn | Ważny rytuał przypomni, że nie jesteś tu sam. |
| 40 | Banhammer | Nie każdy konflikt wymaga bana; czasem wystarczy ostrzeżenie. |
| 41 | Clip Moment | Najcenniejszy moment często trwa krócej niż jego wspomnienie. |
| 42 | Top Chatter | Społeczność potrafi pomóc, ale nie warto mierzyć wszystkiego licznikiem. |
| 43 | TaboRanek | Poranek daje drugą szansę sprawom, które nocą były beznadziejne. |
| 44 | Wodny Wąż | Uważaj, czy nie szukasz odpowiedzi w niewłaściwym akwenie. |
| 45 | Cozy ASMR | Czasem cisza powie więcej niż najdłuższy klip. |
| 46 | 500 Follow Special | Małe jubileusze zasługują na radość, nie na presję kolejnych celów. |
| 47 | ELTaboBot | Automat wszystko policzy, ale może przegapić sedno. |
| 48 | Wapniak - Hejt Prastary | Prastara uraza nie musi trwać od Woodstocku po dziś. |
| 49 | KubaFanBZP - BaniCzny Błazen | Śmiech jest potężny; bana używaj tylko zgodnie z regulaminem. |
| 50 | Cydyn - Ojciec Bliźniaków | Dwa spojrzenia na ten sam problem dadzą pełniejszą odpowiedź. |
| 51 | KruparGames - Ojciec Admin | Dobry administrator przypomni o kopii zapasowej twojego planu. |
| 52 | Madbbranko - Komórka Wątroby | Serce ma miejsce na więcej niż jedną historię. |

## 9.5. Przykładowa pełna interpretacja - trzy karty

**Pytanie użytkownika:** „Czy zrobić kolejnego nocnego streama?”  
**Układ:** Przeszłość = Pestarz - Kierownica o 3 w Nocy; Teraz = Cozy ASMR; Przyszłość = Hymn.

> **Przeszłość / Pestarz:** Nie każda późna noc kończy się rozsądną decyzją; masz już doświadczenie z absurdalnymi godzinami.  
> **Teraz / Cozy ASMR:** Zanim wystartujesz, sprawdź, czy szukasz spokoju, czy kolejnego chaosu.  
> **Przyszłość / Hymn:** Gdy się pojawisz, społeczność może nadać całemu wieczorowi własny rytm.  
> **Podsumowanie:** „Możesz streamować, ale nie dziw się, gdy dwie minuty później wszyscy każą ci wstać do Hymnu.”

To **przykład testowy**, nie wynik prawdziwego losowania. Oprogramowanie pokazuje interpretacje pozycji i finalną autorską puentę; nigdy nie twierdzi, że zna przyszłość.

## 9.6. Historia wróżb - funkcjonalnie kompletna

Każda zakończona wróżba domyślnie zapisuje się automatycznie po pokazaniu ostatniej karty (gracz może to wyłączyć w ustawieniach prywatności). Pytanie jest zapisywane **dokładnie tak, jak wpisano**, bez wysyłki na serwer. Rekord:

```json
{
  "id": "local-uuid",
  "createdAt": "2026-10-25T20:00:00+01:00",
  "question": "Czy robić nocny stream?",
  "spread": "THREE",
  "positions": ["PRZESZLOSC", "TERAZ", "PRZYSZLOSC"],
  "cardIds": [21, 45, 39],
  "revealedCount": 3,
  "interpretationVersion": "pl-v1",
  "interpretationSnapshot": ["...", "...", "..."],
  "summarySnapshot": "...",
  "userNote": "Najpierw sprawdzić słuchawki.",
  "isCompleted": true
}
```

**Po kliknięciu wpisu historii:** odtwórz dokładnie zapisany rozkład, kolejność, grafiki, datę i pytanie; pokaż każdą kartę w pełnym powiększeniu; pozwól przełączyć `Tytuł / cytat / słowa-klucze / autorski komentarz`, edytować notatkę, usunąć wpis lub wyeksportować wyłącznie ten rekord. `interpretationSnapshot` zachowuje zgodność ze starszymi wersjami tekstów; przy aktualizacji gry historia nie „zmienia wróżby”.

Historia filtruje po dacie, typie rozkładu i szukanej frazie; przy tysiącach wpisów ma paginację/wirtualizację. Użytkownik może `Eksportuj całą historię .json`, `Importuj .json` (z walidacją typu i rozmiaru), `Usuń wybrane` / `Usuń wszystko` (potwierdzenie), `Pobierz obraz układu` (PNG przez Canvas lub eksport serwerless). Przy błędzie miejsca na dysku UI proponuje natychmiast eksport, bez udawania pomyślnego zapisu.

## 9.7. Różnica wobec pojedynków - czytelny przełącznik

W trybie Wróżby **nie pokazuj K/M, znaczników, przycisków „Zagraj” ani odblokowań fabularnych**. To osobna atmosfera: delikatne flippy, fioletowo-złota iluminacja, pojedyncze dźwięki świec i kart. Pojedynki mają energiczne ruchy, pionowe słupki wyników, statusy i reakcje rywala. Użytkownik nie może przypadkowo użyć „dwa razy tej samej karty” przez posiadanie duplikatu bojowego.

---

# 10. Reżyseria wizualna i animacje 2D - wymagania obowiązkowe

## 10.1. Kierunek artystyczny

**Zasada bez wyjątku:** gra może mieć proste 2D i niewiele klatek ilustracji, **ALE musi sprawiać wrażenie żywej dzięki dopracowanej animacji i reakcji na myszkę**. Referencją są załączone ilustracje TABOta: czarne tło, elektryczny fiolet, żółto-złote kontury, akcenty różu, gwiazdy, świece, retro-elektronika. Zachowaj kontrast tekstu i nie pozwalaj efektom zasłaniać cytatów.

**Sugerowana paleta:** tło #090513; panel #171026; obrys #6f2a9b; fiolet-neon #b22cff; złoto #ffdf24; róż #ff4edb; biel #f6f3ff; ostrzeżenie #ff8666. Dobieraj kontrast tekstu co najmniej WCAG 4.5:1 dla standardowego tekstu i ≥3:1 dla elementów graficznych krytycznych. Kolory są punktem wyjścia, nie zakazem modyfikacji dla dostępności.

**Warstwy sceny:** statyczna ilustracja tła; 2–3 subtelne płaszczyzny parallax; sprite postaci/półpostać; stół; oryginalne ilustracje kart; nakładki K/M; nad kartami warstwa statusów; cząsteczki tylko w momencie akcji; UI najwyżej. Część animacji można zrealizować shaderem/nakładką zamiast klatka-po-klatce.

## 10.2. Matryca mikroruchów i reakcji myszki

| Akcja | Reakcja | Czas/parametry startowe | Dodatkowa zasada |
|---|---|---|---|
| Najechanie na kartę w ręce | unoszenie, skala 1.10–1.14, cień, tilt do 4° zależnie od pozycji kursora | 110–180 ms easeOutCubic | Przestań obracać po odsunięciu; tooltip pełny |
| Najechanie na kartę na stole | obrys złoty, skala 1.05, panel efektów i wyniku | 100–160 ms | Nie zakrywa pozostałych wartości w strefie |
| Najechanie na przycisk menu | lekki rozbłysk, podkreślenie, dźwięk | 120 ms | Widoczny focus klawiatury wygląda podobnie |
| Przytrzymanie karty | karta przy kursorze, magnetyczne sloty, delikatna linia celu | na bieżąco, płynny lerp | Upuszczenie poza legalnym celem -> miękki powrót |
| Legalny slot | rozświetlenie + delikatny puls | 0.8 s | Nie używaj wyłącznie koloru; ikona ✓ |
| Nielegalny slot | krótki wstrząs 6–8 px, tekst przyczyny | 180 ms | Nie spalasz Energii, bo plan się nie zatwierdził |
| Wystawienie karty | krótki ślad gwiazd, sprężyste wejście, obrót do 2° | 240–350 ms | Zdarzenie i liczby oparte na logice, nie na klatce animacji |
| Wzmocnienie | złote `+2` odlatuje nad wskazaną kartę | 350–500 ms | Panel szczegółów zachowuje historię modyfikatorów |
| Osłabienie | purpurowa smuga i `−2`, 1 błysk | 300–450 ms | Nie sugeruj HP/krwi, to tylko punkty |
| Wyciszenie / ban | pieczęć `B A N`, przekreślenie ikon Aury/Finału, cichy gong | 400–650 ms | Karta zostaje na polu; nie robić animacji usunięcia |
| Usunięcie | karta kruszy się na piksele, slot staje się wolny | 420–700 ms | Rozstrzygnięcie logiczne wcześniej niż efekt wizualny |
| Żeton na polu | z karty matki wyskakuje miniaturowy portret/stołek/ikona | 300 ms | Max 4 sloty na strefę, czytelna wielkość |
| Rytuał o 20:30 | na 0.3 s przyciemnij tło, pokaz znak + hymn | 550–900 ms | Nie blokować sterowania dłużej niż konieczne |
| Rozprawa WR / awaria | neonowy pasek strefy, nazwa WR, powód zmiany | 450 ms | Ostrzeż przed nadejściem w poprzednim kroku |
| Zmiana punktacji | płynne liczenie do nowej liczby, wyróżnienie zmiany | 180–280 ms | Liczbę końcową pokazuj bez czekania na animację w logu |
| Dobranie karty | rewers leci z talii do ręki, krótki flip | 260–340 ms | Nie ujawniaj ręki AI |
| Finał meczu | zatrzymanie interakcji, 2–3 wyraźne sekwencje wyników, konfetti kart | ok. 2 s, skracalnie | Efekty można jednym kliknięciem przyspieszyć |
| Wróżenie: tasowanie | 52 rewersy przesuwają się kaskadowo i przeplatają | 1–3 s, pomijalne | Wynik losowania niezależny od renderowanych klatek |
| Wróżenie: odcięcie | wierzch talii odjeżdża w lewo, wraca na spód | 450–650 ms | Alternatywny przycisk dla osób bez możliwości przeciągania |
| Wróżenie: odsłonięcie | flip z lekką poświatą, subtelny dźwięk | 450–600 ms | Pod koniec animacji pokaż duży, czytelny obraz i tekst |

**Przystosowanie dostępności:** `Reduce Motion` skraca animacje do maks. 80 ms bez parallax/tilt, wyłącza błyski; `Disable shake` osobna opcja. Nie używać gwałtownych wielokrotnych błysków (≤3 na sekundę); napisy nie zależą od timera. Kontrast, skala interfejsu 80–150%, możliwość wyboru fontu czytelnego zamiast ozdobnego, nawigacja Tab/Shift+Tab, Enter/Spacja, Escape oraz tryb wysokiego kontrastu.

## 10.3. Grafika kart i jakość renderowania

- Wyświetlaj oryginalne PNG w proporcji bez przycinania tytułu i cytatu. Przykładowe pliki: `01_prorok_tabo.png`, `07_ltasiaa_motkowa.png`, `52_madbbranko_komorka_watroby.png`.
- Warstwa bojowa dokleja czytelne kapsuły K/M oraz tag przy karcie; nie piecz ich w ilustracji - wróżby muszą widzieć oryginalną kartę bez statystyk.
- Miniatury tworzyć w buildzie w kilku rozmiarach (np. 128/256/512 px), duże grafiki ładować dopiero przy zoomie. Wersje PNG/WebP przechowywać legalnie w pakiecie; brak żądania internetowego do każdego obracania.
- Sprite postaci może powstać z tej samej ilustracji: „idle” jako 2–3 px unoszenia, „mówi” minimalny ruch twarzy/ramki, „przegrywa” miękki rumieniec naświetlenia. Zero wymogu nowych rigów 3D.
- Animacje mają `animationId` i log. Nie powinno być możliwe kliknięcie i zagranie tej samej karty dwa razy podczas lotu sprite'a.

## 10.4. Warstwa audio i krótkie dialogi

**Cztery suwaki głośności:** muzyka, SFX, dialogi, interfejs. Napisy domyślnie włączone. Dla każdego z 20 bossów 6 triggerów (maks. 120 krótkich wypowiedzi), ale w MVP nagrać tylko START + LOSE + WIN, a WR/LEAD/TRAIL pozostawić jako napisy z dźwiękiem klawisza/dżingla. Pełne vo można dograć sukcesywnie. Ogranicz każdą kwestię do 2–8 s; przerwanie animacji nie może zatrzymywać mechaniki. Dialogi nie powtarzają się co turę. Wzmianki o prawdziwych klipach użytkownika (np. „Na Caution się nie leczymy!”, „Hymn Tabo!”, „Nic tu kurła nie działa!”, „NOWA META - granie tyłem do ekranu!”, „Nie biegasz z ink ribbonem”) mogą prowadzić do prawidłowo licencjonowanych próbek dźwiękowych po sprawdzeniu zgody i jakości; w braku praw zachować nawiązanie tekstowe/autorskie.

**Przypisanie motywów:** Nysmo - komunikaty Moderacji; Greed - szum kasety; Gumbox - kłopotliwy „A” glitch; Maciek - pojedynczy takt Hymnu; Jillie - dźwięk powiadomienia; Pestarz - start silnika; Krisuroku - przyjazny chór; Cydyn - dwa dzwonki; Wampir - nocny wiatr; śmigłowiec - łopaty; Meeefjuuu - kilka nut; LtAsiaa - stuk młotka; ELTaboBot - syntezator/głos filtra, ale bez kopiowania brzmienia realnej osoby.

---

# 11. Sztuczna inteligencja i zróżnicowanie przeciwników

## 11.1. Brak „czytania w ręce” i stały RNG

Każda strona zna: karty na stole, widoczne wydarzenia i ich historię, WR, liczbę kart w ręce rywala, stos odrzuconych, energię, kolejność punktowania. AI **nie zna** kart w aktualnej ręce Taboreta, przyszłych kart w talii gracza ani wyborów Rytuału przed ujawnieniem. W tutorialu zasady są specjalnie skryptowane i widocznie oznaczone. Dla AI można używać prostego beam search / heurystyki po legalnych zagraniach, bez potrzeby modelu ML czy usługi online.

## 11.2. Heurystyka, profile i trudność

Ocena stanu dla przeciwnika uwzględnia nie tylko globalną sumę, ale *dwa wygrywane pasy*:

```text
score(board) =
  12 * expectedLanesWon
  + 0.3 * clamp(totalPowerLead, -15, 15)
  + 1.2 * remainingEnergyEfficiency
  + 0.6 * futureSynergyPotential
  - 1.8 * exposedUnprotectedCombos
  + scriptedProfilePreference
```

Stałe są **proponowanymi parametrami do strojenia**. `expectedLanesWon` nie może oznaczać podglądania przyszłości, jest estymatą z widocznego stanu i rozkładu możliwych kart oponenta. AI generuje legalne plany ze swojej ręki do aktualnego limitu Energii, oblicza dokładne skutki własnych efektów, a następnie ocenia kilka wiarygodnych odpowiedzi przeciwnika opartych na znanych/nieznanych kartach. Trzymamy budżet obliczeniowy 10–30 ms w web na średnim sprzęcie, z fallbackiem do krótszego beam search. Długi czas `myślenia` jest wyłącznie efektem animacji, nie długim blokowaniem JS.

**Easy:** poprawne zasady, losowy wybór z trzech najlepszych planów, mniejsze planowanie przyszłych tur. **Normal:** wybiera najlepszy plan z top-k, uwzględnia 1 turę przyszłych zagrożeń. **Hard:** porównuje scenariusze do Finału, optymalizuje tempo i Rytuał, ale korzysta z tych samych legalnych informacji. Wszystkie AI muszą kończyć swą turę nawet przy zerowych legalnych ruchach.

## 11.3. Charakter zamiast cheatów

| Archetyp AI | Postacie | Na co poświęca dodatkową wagę | Jak go kontrować |
|---|---|---|---|
| Archiwista | Greed, AL, Krupar | ZAPLECZE i Retro; punkty audytu | Wyrównuj Zaplecze w odpowiedniej turze, graj większe jednostki późno |
| Spamer | Jillie, Cydyn | Liczebność CZATU i generowanie żetonów | Pozostałe strefy, kara za tłok, usuwanie żetonów |
| Kontroler | Nysmo (po tutorialu), LtAsiaa, InfinityPotato | Wyciszanie i wybór kluczowych celów | Ochrona, rozproszenie synergii, duża bazowa Moc |
| Kombinator | Qrus, Gumbox, B4Nork, Śmigłowiec | Zadania specjalne stref | Planuj sloty i miej karty przesuwające |
| Koncert | Maciek, Krisuroku, Meeefjuuu | HYMN i STREAM | WYcisz Aura, wygraj dwie pozostałe strefy |
| Horror | Wampir, Wapniak, Pestarz | Wysokokosztowe zagrania i zaskoczenie | Krzywa kosztów, przejmowanie wczesnej przewagi |
| Finał | Pierd0la, ELTaboBot | Zachowanie zasobów pod dodatkową turę/glitch | Kontroluj momenty WR, nie ustawiaj całej strategii na Wejścia |

**Niezmiennik:** AI nigdy nie oszukuje w kolejności doboru (poza jawnie skryptowanym tutorialem), nie zagrywa karty większym kosztem niż Energia i nie ma tajnej 13. jednostki. Trudność bierze się ze sposobu wykorzystania WR i lepszej oceny dwóch stref.

## 11.4. Dialogi sytuacyjne a tempo rozgrywki

Gdy przeciwnik prowadzi w 2 strefach na koniec tur 3–5, losuj z jego nieodtworzonych kwestii LEAD tylko raz. Gdy przegrywa 2, analogicznie TRAIL. Jeśli w tej samej turze WR wyświetla wielką animację i cue LEAD, WR ma pierwszeństwo, LEAD pojawia się jako dyskretny napis pod portretem. W ustawieniach `Dialogi przeciwników: wszystkie / tylko początek i koniec / wyłączone`. **Nie ustawiaj animacji tak, by czekała na zakończenie audio lub połączenie sieciowe.**

---

# 12. Postęp, nagrody, ekonomia i system talii

## 12.1. Odblokowania bez RNG i bez grindu

**Na samym początku** odblokowane typy 52-kartowej puli: `01, 02, 04, 06, 10, 31, 41, 43`; z wydarzeń: `E01, E03, E05, E07`. Pozwala to złożyć legalną 18-kartową talię nawet przy limicie 2 kopie i min. 12 jednostek. Resztę przyznają kolejno rozprawy 01–20, jak rozpisano w każdym rozdziale. **Inwariant kompletności:** osiem oryginalnych startowych + 44 oryginalne zdobywane = **52/52**. Cztery startowe wydarzenia + 20 wydarzeń z rozpraw = **24/24**. Ponowne ukończenie starcia nie daje nowych kopii; zamiast tego można zdobyć portretową ramkę/oznaczenie „perfekcyjna wygrana” (czysto kosmetyczne).

**Gdy FABUŁA jest ukończona:** gracz ma pełną kolekcję 76 typów, może projektować nieograniczenie wiele decków w eksporcie JSON i do 8 szybkich presetów na profilu. W HARD każda misja ma ofertę 24 kart **wśród już odblokowanych**, lecz po NORMAL wszystkie są już dostępne. Opcja „Użyj gotowej talii” pozostaje pełnoprawnym wyborem, nigdy karanym niższą punktacją.

## 12.2. Algorytm tworzenia gotowej talii NORMAL

Przed każdym meczem `getStoryDeck(opponentId, unlockedIds)` zwraca listę dokładnie 18 typów z kopią maks. 2. Udział docelowy: 4–5 kart za 1–2 Energii, 7–9 kart za 3–4, 3–5 kart za 5–6 oraz 0–3 wydarzenia. To zalecana **krzywa kosztów**, nie sztywny zakaz. Zawsze co najmniej 12 jednostek. Na końcu wykonywana walidacja; jeśli misja jest szkoleniowa i brakuje jeszcze określonego typu, system oferuje egzemplarz `loaner` bez trwałego odblokowania. Normalna talia jest taka sama między próbami danego bossa (czytelność), a losowa ręka zmienia przebieg meczów.

**Opcjonalne wyzwania:** zwycięstwo bez korzystania z Rytuału BAN, zwycięstwo z jedną zapełnioną strefą, odblokowanie easter egga w TaboLOGu. Nie dają silniejszych wersji kart, tylko wpisy w kronice, motywy rewersów i odznaki „SEZONOWIEC”, „TWARDY TABORET”, „WETERAN”, „HEJTER” (żartobliwa klasyfikacja TaboLore).

## 12.3. HARD: draft z prawdziwymi decyzjami

**Krok 1:** na początku każdego pojedynku gra pokazuje 24 losowo wybrane **instancje** kart ze zdobytej kolekcji; minimum 16 z nich musi być jednostkami, maks. 8 wydarzeniami, a do oferty nie można wstawić 3 kopii typu. Gwarantuj co najmniej 5 tanich (K1–2) i co najmniej 3 typy o K5–6. Jeżeli generator nie spełnia ograniczeń, przelosuj przed pokazaniem (ograniczone próby + deterministyczny plan rezerwowy).

**Krok 2:** gracz wybiera 18 z 24. Interfejs odlicza kopie, kosztową krzywą, liczbę jednostek i wydarzeń. Automatyczne podpowiedzi: „masz tylko 1 kartę za K1 - rozważ dołożenie taniej”, „za mało jednostek: 10/12”.

**Krok 3:** do wyboru `WYBIERZ AUTOMATYCZNIE`, `WŁASNY PRESET (JEŚLI PASUJE DO OFERTY)` i `ZAPISZ WYNIK`. Nie można pominąć braku legalnych opcji; generator zawsze daje wykonalny draft. Własny preset spoza oferty można zapisać do trybu Swobodnego, ale w HARD misja wymaga zasad draftu.

**Krok 4:** rozpoczęcie meczu. Jeśli gracz przegra, może wybrać `REWANŻ TĄ SAMĄ OFERTĄ` (zmienia się tylko seed rozdań) lub `NOWY DRAFT` (nowa oferta). To ważne: losowość nie może blokować przez 20 min w próbie zdobycia jednej karty. Oferta i wybór zapisywane są przed walką.

**Krok 5:** po każdym pięciu meczach HARD pojawia się obowiązkowa jednoekranowa notatka TaboLOGu, ale nie przerywa podstawowego loopu na dłużej niż 20 s.

## 12.4. Swobodna gra i powtarzalność

Po tutorialu odblokuj panel `POJEDYNKI` - rewanże z poznanymi postaciami, własne talie lub gotowe, rozmaite poziomy AI i wybór WR. Rozróżnij liczniki `wygrane na NORMAL` i `wygrane na HARD`; nie porównuj ich jako jednego rankingu. Przeciwnik, który był już pokonany, nigdy nie zamyka pozostałych aktywności.

---

# 12A. Konkretne talie przeciwników i talie FABUŁA (gotowe do zapisania w danych)

Tabela poniżej nadaje się do eksportu do `storyDeck` oraz `enemyDeck` dla 20 poziomów. Pokazuje **18 kart na stronę**. Skróty `01–52` to oryginalne karty z rozdziału 4, `E01–E24` to wydarzenia z rozdziału 5; `×2` oznacza dwie kopie, brak `×2` jedną. Każda talia została programowo zwalidowana co do długości, limitu kopii i liczby jednostek. Talia TABO zawiera **wyłącznie typy odblokowane przed danym pojedynkiem**; talia przeciwnika może zawierać jeszcze niezdobyte karty, dzięki czemu pokazuje nagrody i uczy z nich korzystać. **Wyjątek:** tutorial stosuje ustawioną w rozdz. 7 kolejność, a nie losowe rozdanie.

**Balans:** to propozycja contentowa v1, wymagająca późniejszej symulacji i testowania przeciw ludzkiemu graczowi. Poniższe rozpiski nie są „deckami idealnie zbalansowanymi”; ich celem jest pełna implementowalność i spójne z archetypami zachowanie przeciwnika.

| Rozprawa | Talia TABO (Normal, 18) | Talia przeciwnika (18) |
|---:|---|---|
| 01 | 01, 10×2, 02×2, 31×2, 04×2, 41×2, 43×2, 06×2, E01, E03, E07 | 10×2, 11, 21, 04×2, 40×2, 06×2, 07, 08×2, 09×2, E01, E02, E18 |
| 02 | 10×2, 11×2, 14×2, 02×2, 31, 04×2, 43×2, 06, 08×2, E01, E02 | 11×2, 13, 16×2, 23, 27×2, 31×2, 41×2, 07, 09×2, E04, E10, E17 |
| 03 | 10×2, 11, 14×2, 23×2, 03×2, 31, 04, 41×2, 43, 06, 08, E02, E04 | 17, 02×2, 21, 24, 29×2, 30×2, 32, 48×2, 49, 05×2, E06, E08, E18 |
| 04 | 10×2, 11, 14×2, 02, 23, 24×2, 03×2, 30×2, 31, 04, 06, E03, E06 | 13×2, 19×2, 03, 39, 43×2, 45×2, 46, 06×2, 08, 09, E04, E11, E19 |
| 05 | 10×2, 11×2, 13×2, 24, 30, 31, 39×2, 04, 41, 43, 06, 08, E07, E08 | 10×2, 18×2, 22×2, 26×2, 50, 52, 06×2, 08, 09×2, E16, E19, E20 |
| 06 | 11, 02, 03, 30, 39, 04, 41, 42×2, 43, 45×2, 06, 08, 09×2, E01, E09 | 10×2, 12×2, 17, 02×2, 21, 29, 30×2, 48, 49×2, 07, E10, E11, E15 |
| 07 | 10, 11, 12×2, 02×2, 30×2, 41×2, 42, 43, 48×2, 06, 08, E06, E10 | 12×2, 17×2, 02×2, 21×2, 24×2, 29, 30, 35, 48×2, E13, E17, E23 |
| 08 | 10, 11, 14×2, 21×2, 23, 03, 31, 37×2, 39, 41, 42, 48, 06, E10, E11 | 12, 15, 17×2, 02×2, 21×2, 29, 30×2, 48×2, 49, 05, E05, E10, E13 |
| 09 | 11, 12, 13, 17×2, 24, 29×2, 03, 31, 37, 04, 41, 43, 45, 06, E06, E12 | 10, 18×2, 22×2, 42, 26, 50×2, 52×2, 06×2, 09×2, E03, E17, E22 |
| 10 | 11, 12, 17, 02, 21, 28×2, 43, 39, 04×2, 41, 43, 50, 06, 10, 24, E13 | 13, 18, 31×2, 33×2, 34, 35×2, 36×2, 37×2, 38, 48, E08, E11, E18 |
| 11 | 11×2, 14, 02, 28, 35, 37×2, 38×2, 41, 43×2, 44, 08, 09, E11, E14 | 12×2, 17, 02×2, 21×2, 24, 29×2, 30×2, 46, 48×2, E03, E11, E13 |
| 12 | 10, 17×2, 02, 21, 24, 27×2, 28, 29, 31, 33×2, 04, 43, 50, E08, E15 | 25, 28×2, 31×2, 36×2, 37×2, 38, 39, 04×2, 47, 08, E06, E17, E23 |
| 13 | 11, 12, 02, 24, 25×2, 33, 35, 36×2, 37×2, 39, 41, 43, 06, E05, E16 | 13×2, 18, 19×2, 02, 03, 39, 43×2, 45×2, 46, 52, 06, E03, E06, E08 |
| 14 | 10, 12, 13, 19×2, 02, 21, 24, 25, 27, 30, 31, 04, 46, 08×2, E16, E17 | 11×2, 16×2, 17, 23×2, 25×2, 27×2, 31×2, 41, 50, E07, 21, E15 |
| 15 | 11, 16×2, 19, 02×2, 25, 26×2, 27, 28, 37, 38, 42, 43, 44, E13, E18 | 12×2, 15, 17×2, 02×2, 21, 29, 30×2, 48×2, 49×2, E04, E07, E23 |
| 16 | 14, 02, 21×2, 25, 29, 30, 40, 45, 46, 48, 49×2, 05, 06, 09, E07, E19 | 10, 14, 15, 18×2, 22×2, 23, 26×2, 52, 06×2, 09×2, E11, E15, E16 |
| 17 | 11, 13, 02, 22×2, 23, 24, 25, 31, 33, 35, 41, 49×2, 52×2, E18, E20 | 10×2, 11, 04×2, 40×2, 06×2, 07×2, 08×2, 09×2, E08, E09, E18 |
| 18 | 11, 12, 16, 18×2, 19, 02, 23, 24, 28, 29, 45, 48, 05, 06, 07, E16, E21 | 28, 03, 31, 34, 36×2, 37×2, 04×2, 47, 49, 51×2, 06, 10, 21, E24 |
| 19 | 10, 11, 02, 24, 26, 29, 30, 31, 34×2, 37, 43, 45, 46, 51×2, E10, E22 | 12, 17×2, 02×2, 24, 29, 30×2, 44, 48×2, 49×2, 05, E10, E13, E20 |
| 20 | 10, 11, 18×2, 20×2, 21, 23, 28, 29, 31, 32, 33, 04, 42, 06, E21, E23 | 12, 02, 25×2, 28, 37×2, 04×2, 45, 47×2, 05, 51×2, E10, E12, E21 |

**Uwaga o utrzymaniu:** po strojeniach liczb w katalogu kart talie powinny być ponownie testowane; nie dobieraj AI w ukryciu „kontry” do ręki gracza. Można zmienić skład stałej talii danej misji w aktualizacji, ale zapis wyzwań i wersji zasad należy utrzymać kompatybilny z istniejącym slotem.

---

# 13. Technologia i architektura - konkretny plan implementacji

## 13.1. Preferowany stos

**TypeScript + React (ekrany/menu, komponenty modalne) + Phaser 3 (stół, animacje kart i VFX) + Zustand lub Redux Toolkit (stan UI) + czysty moduł `@tabota/game-core` (silnik zasad, zero importów graficznych).** Web jako wersja referencyjna. Później **Tauri 2** opakowuje ten sam frontend w aplikacje na Windows, macOS i Linux; Electron jest alternatywą, jeśli prostsza obsługa audio/pluginów przeważy nad większą wagą paczki. Phaser dokumentuje `pointerover`, `pointerout`, `pointermove` i tweening; Tauri dokumentuje desktopowy cross-platform. Linki do aktualnej dokumentacji w źródłach.

**Czego nie robić:** łączenia obliczania punktów z klatkami animacji, łączenia logiki bossa z `if` w UI, zapisywania tylko obrazu planszy bez seedów, używania wyłącznie `Math.random()` w testach reproducible, wrzucania nazw kart jako hardcodowanych selectorów CSS, wiązania wyników wróżb z kartami bojowymi.

## 13.2. Repozytorium (proponowana struktura)

```text
tabota/
├─ apps/web/                  # React/Vite + Phaser
├─ apps/desktop/              # Tauri shell, ikony, instalatory
├─ packages/game-core/       # zasady, legalność, resolver, RNG, stany, testy
├─ packages/cards/           # card-definitions.pl.json; tarot-text.pl.json
├─ packages/story/           # 20 misji, 20 WR i dialogi z tego GDD
├─ packages/ai/              # algorytm ruchów i profile przeciwników
├─ packages/persistence/     # schema danych, IndexedDB, migracje, eksport
├─ assets/cards/original/    # 52 dostarczone grafiki (bez zmian)
├─ assets/cards/events/      # 24 nowe proste karty specjalne
├─ assets/audio/             # własne lub licencjonowane sample / vo / napisy
└─ docs/                     # niniejszy GDD, QA i mockupy
```

## 13.3. Przykładowe formaty danych (nie implementacja)

```ts
type Lane = 'STREAM' | 'CHAT' | 'BACKSTAGE';
type CardType = 'UNIT' | 'EVENT';
type AbilityTrigger = 'ON_PLAY' | 'AURA' | 'FINAL';

type CardDefinition = {
  id: string;             // 'TABO_08', 'E_03'
  originalTarotId?: number; // tylko dla kart 1–52
  nameKey: string;
  visualAsset: string;
  cost: 1|2|3|4|5|6;
  power: number;          // 0 dla EVENT
  kind: CardType;
  tags: string[];
  abilities: Array<{ trigger: AbilityTrigger; effect: string; args: Record<string, unknown> }>;
};

type Instance = {
  instanceId: string; cardId: string; ownerId: 'PLAYER'|'AI';
  lane?: Lane; createdTurn?: number; buff: number; debuff: number;
  protected: boolean; silenced: boolean; token: boolean;
};

type EncounterDefinition = {
  id: number; opponentKey: string;
  ruleId: string; ruleParams: Record<string, unknown>;
  hardRuleParams: Record<string, unknown>;
  enemyDeck: string[]; storyDeck: string[];
  dialogue: Record<string, string>; unlocks: string[];
};
```

W faktycznym kodzie `power` i `buff/debuff` powinny mieć jedną walidowaną metodę obliczenia Mocy (bez ręcznego dopisywania w UI), a log zdarzeń musi utrwalać kolejność efektów. W przyszłości można łatwo dodać lokalizacje, bez zmieniania logicznych `card_id`.

## 13.4. Przykład resolvera i mechanik jako danych

```text
validateDeck(cards):
    assert length == 18
    assert count(unit) >= 12 and count(event) <= 6
    assert for_each(cardId) count <= 2
    assert all IDs unlocked or explicitly loaned for this tutorial

startMatch(seed, deckPlayer, deckAI, encounter):
    shuffle independently with seededRNG
    draw(5), mulligan(0..2), put matchRound=1
    apply visible Warunek Rozprawy

submitTurn(planPlayer, planAI):
    reject illegal plays (energy, slots, targets, copy, stage action)
    commit both plans (plans must be immutable from now on)
    if round == 4: resolve Ritual selection (if unlocked)
    while any plan has moves:
        resolve one action from current initiative holder; alternate
        place units and resolve ON_PLAY
        recalculate auras, protection, changed lane totals
        append deterministic log event
    apply end-of-round boss rule, if any
    if final round:
        resolve FINAL in canonical order
        apply end-of-match boss penalty/bonus
        compare lanes, compare sum on ties
        persist result
    else:
        round += 1
        refresh energy = round (cap 6, stage16 hard exception 7)
        draw(1), run next-round stage triggers
```

**Uwaga implementacyjna:** karty w planie, które miały legalną strefę w momencie układania, muszą sprawdzać docelowe wolne miejsca po wcześniejszych naprzemiennych akcjach. UI z wyprzedzeniem ostrzega o ryzyku, a gdy slot zostanie zajęty, karta pozostaje w ręce, a jej Energia zostaje zwrócona - nie może znikać po cichu. Wówczas dalsze ruchy planu tej strony pozostają w ustalonej kolejności, ale nie muszą mieć już pierwotnie wystarczającej Energii; silnik próbuje je rozegrać, jeśli legalne. Unika to softlocków i fałszywej „kradzieży” karty.

**WYDARZENIA:** zagrane i odrzucone wywołują `ON_PLAY`; jeśli WR finałowego bota wyłącza pierwsze Wejście w strefie w danej turze, wydarzenie liczy się do wykorzystania blokady, nawet gdy nic nie zdziała - ekran musi to sygnalizować przed zatwierdzeniem. **Efekt Proroka Tabo:** Finał liczy liczbę stref z co najmniej jedną własną jednostką, nie liczbę kart; max 3.

## 13.5. Lokalny zapis - dwa niezależne magazyny

**Kampania (per slot):** wersja schematu, currentMode, chapter, completedMissionIds, hardCompletedMissionIds, unlockedOriginalIds, unlockedEventIds, kosmetyki, zapisane presety talii, ustawienia, ukończony tutorial, historia wyniku/replay seed, ewentualny mid-match snapshot (stół, dociągi, oba decki, wszystkie statusy, stany WR, energia, plany niezatwierdzone, kolejność inicjatywy, RNG state i log). Autozapis po każdym `submitTurn` i po przejściu na mapę; nigdy w połowie rozstrzygania animacji.

**Wróżby (globalnie na urządzeniu):** rekordy z punktu 9.6, osobna baza/tabela, oddzielone od kasowania kampanii. Usunięcie slotu kampanii nie usuwa prywatnych pytań. Domyślnie lokalnie IndexedDB (przeglądarka), na desktopie ten sam mechanizm + natywny import/eksport. JSON z `schemaVersion`, walidacja Zod/JSON Schema, migracje między wersjami, jednorazowy automatyczny backup przy aktualizacji schematu. `Kontynuuj` w razie braku slotu disabled z czytelną informacją. Żadna chmura ani analytics bez osobnej zgody.

**Ochrona danych:** wróżby mogą zawierać osobiste pytania; NIE dołączać treści pytań do crash logów, narzędzi analitycznych, reklam ani zewnętrznych URL. Użytkownik może je wyeksportować/usunąć, a instrukcja w menu jasno mówi, na którym urządzeniu są przechowywane. Tryb incognito i blokada zapisu przeglądarki mogą powodować utratę historii; sygnalizuj to przed pierwszym wróżeniem.

---

# 14. Warunki odbioru (Definition of Done)

## 14.1. Mecze, balans i AI - testy automatyczne

- [ ] Walidacja decku: 18 kart, 12–18 jednostek, 0–6 wydarzeń, maks. 2 kopie.
- [ ] Dokładnie 52 oryginalnych ID i 24 nowych ID, bez duplikatów; nazwy assetów odpowiadają ZIP.
- [ ] Tura 1–6 ma dokładnie 1–6 Energii; w rozprawie Pierd0li 1–7 ma 1–7.
- [ ] Limit 4 slotów na strefę (wyjątek Jillie HARD = 5 na CZACIE, wyświetlany jawnie).
- [ ] Po wyciszeniu giną tylko AURA/FINAŁ; Wejścia się nie cofają.
- [ ] Buff [−4,+4], Aura +4, Moc nieujemna; wielokrotne wejścia nie tworzą nieskończonej pętli.
- [ ] Żetony Cydyna tworzą 0/1/2 instancje zgodnie z wolnymi slotami.
- [ ] Przesuwanie przy pełnym slocie nigdy nie usuwa karty bez podpowiedzi.
- [ ] Rytuał nie kosztuje Energii i odblokowuje się dokładnie po misji 03/przed 04.
- [ ] AI zna tylko legalne informacje; przy pustej ręce nadal kończy turę.
- [ ] Finalny bot wyłącza wyłącznie pierwsze Wejście w jawnej strefie, a nie koszty czy bazową Moc.
- [ ] Porównanie stref rozstrzyga zwycięstwo prawidłowo także przy ogromnej przewadze przeciwnika w jednej przegranej strefie.
- [ ] Log meczu jest deterministyczny przy tym samym seed, taliach, decyzjach i wersji reguł.
- [ ] Każdy z 20 bossów ma unikalny WR i poprawnie zdefiniowany remix HARD.
- [ ] Dla każdej pary z 5 archetypów po 10 tys. seedów mierzymy win rate, przewagę inicjatywy i średnie tempo, a parametry stroimy z danych.
- [ ] Random-vs-random, normal-vs-normal, hard-vs-hard, mirror deck; wykrywamy żaden ruch bez kosztu, żaden niezakończony match, brak softlocków.
- [ ] W tutorialu dokładna sekwencja prowadzi do końcowego wyniku `15:20 / 10:8 / 13:5`, niezależnie od FPS i przerwania animacji.

## 14.2. UI / animacje / dostępność - testy ręczne

- [ ] Każda karta reaguje na hover/klik/focus; po odsunięciu kursora wraca płynnie, nie pozostaje zawieszona.
- [ ] Każdy przycisk menu ma hover/focus/disabled i czytelną podpowiedź, nie istnieją martwe elementy.
- [ ] Wszystkie modyfikacje Mocy mają źródło w tooltipie i animację zmiany stanu, a nie sam nagły przeskok liczby.
- [ ] WR dostępne z planszy **w każdej chwili**, nawet podczas ruchu AI i po pauzie.
- [ ] Wybór celu ma wizualne oznaczenie legalności, a anulowanie ruchu jest możliwe przed zatwierdzeniem.
- [ ] Nie są wymagane gesty myszy do przejścia gry; klik i klawiatura dają równoważny efekt.
- [ ] Ustawienie „zmniejsz animacje” wyłącza tilt, parallax, shake i częste błyski.
- [ ] 60 FPS jako cel na zwykłym sprzęcie desktopowym, degradacja do 30 FPS bez zmiany reguł; brak długich freeze przy dociągu.
- [ ] Audio i napisy działają niezależnie; brak głosówki nie powoduje milczącego pominięcia ważnej wskazówki.
- [ ] 1280×720, 1600×900, 1920×1080, 2560×1440, mniejszy web viewport, dotyk - UI nie obcina nazw i slotów.
- [ ] Gra działa offline po pobraniu assetów; brak backendu nie psuje przycisków.

## 14.3. Wróżby i dane - testy automatyczne

- [ ] Losowanie rozkładu 1/3/5 z listy dokładnie 52 ID; **brak powtórki ID w jednej wróżbie**.
- [ ] Wróżby nie zawierają E01–E24 ani statystyk pojedynkowych.
- [ ] Tasowanie Fisher–Yates nie wykorzystuje animacji do wyniku.
- [ ] Wpisane pytanie 0–500 znaków nie opuszcza urządzenia.
- [ ] Historia ma datę, pytanie, spread, kolejność kart, interpretację, notatkę i numer wersji.
- [ ] Po powrocie z historii te same grafiki i pozycje, bez ponownego losowania.
- [ ] Import, eksport, pojedyncze i zbiorcze usuwanie wymagają walidacji/odpowiedniego potwierdzenia.
- [ ] Brak uprawnień do storage jest wykrywany, a gra oferuje bezpieczny eksport.
- [ ] Skasowanie kampanii nie usuwa historii wróżb.

---

# 15. Etapy realizacji - plan produkcyjny bez ryzyka nadmiaru prac

| Faza | Dostarczane rzeczy | Warunek wejścia w następną fazę |
|---|---|---|
| **P0: Papier + test balansu** | 18-kartowy deck, trzy strefy, 12 wybranych jednostek, dwa wydarzenia, prosty AI w konsoli | 30 partii ręcznych, jasne reguły, brak oczywistej „jednej najlepszej karty” |
| **P1: Vertical Slice** | Menu, tutorial Nysmo z 6 turami, mapa z 01–03, działający log punktów, hover, animacje, lokalny zapis | Nowy gracz kończy tutorial bez objaśnień twórcy |
| **P2: Rdzeń kart** | Wszystkie 52 jednostki, 24 wydarzenia, wszystkie zdolności, statusy, testy silnika, katalog i deckbuilder | Automatyczne testy efektów bez regresji |
| **P3: Kampania** | 20 unikalnych WR, 20 przeciwników, FABUŁA, dialogi napisowe, proste ilustracje lokacji | Ukończenie całej kampanii od początku do końca bez debugowania ręcznego |
| **P4: Wróżby** | Rozkłady 1/3/5, pełne oryginalne PNG, lokalna historia, export/import, interpretacje | Każdy test z 9. i 14.3 przechodzi |
| **P5: HARD i polishing** | Draft 24→18, AI Hard, remixy, animacje statusów, muzyka, dźwięk, dostępność | Wyniki playtestów z definicji ukończenia akceptowalne |
| **P6: Wydania** | Build web/PWA, Tauri Windows/Linux/macOS, podpisane assety, credits, instrukcja użytkownika | Test uruchomienia, zapis/odczyt i dźwięk na każdej platformie |

**Priorytet przy cięciach budżetu:** nigdy nie usuwaj czytelności, poprawnego resolvera, animowanego feedbacku na ruch myszy, zapisów ani historii wróżb. Lepiej skrócić liczbę voice lines nagranych dźwiękowo (zachowując napisy), niż usuwać unikalne WR-y bossów. Dialogi fabularne nie wymagają dużych scen 3D, a 24 wydarzenia mogą mieć ilustracje skomponowane z istniejących motywów.

---

# 16. Konkretny backlog dla programisty / grafika / scenarzysty

## Programista gry

1. Resolver zdarzeń bez komponentów renderujących; funkcje `validatePlan()`, `commitPlans()`, `resolveAction()`, `recalculatePower()`, `resolveFinal()`, `resolveEncounterRule()` i testy jednostkowe dla 52 + 24.
2. Mapowanie `card_id` ↔ oryginalne PNG, ładowanie miniatur i pełnych ilustracji.
3. Trzy strefy, sloty, talia, ręka, Energia, naprzemienna inicjatywa, mulligan, przejścia stanów.
4. Mechanika wyciszenia, ochrony, osłabienia, usuwania, przesuwania i żetonów, zawsze na logice a nie tweenach.
5. Data-driven 20 WR i warianty HARD z poziomów 01–20.
6. AI bez cheatów z presetami osobowości i wariantami trudności.
7. Dwa przepływy kolekcji/decków oraz osobny flow wróżebny i jego storage.
8. Export/import JSON, walidacja schematów, testy migracji, zapis w trakcie meczu.

## Grafik/animator UI

1. System tła neon 2D, przycisków, slotów, kapsuł Moc/Koszt/tag i tooltipów.
2. Karta w 6 stanach (spoczynek/hover/selected/drag/disabled/resolve), plus 3D flip na wróżbach.
3. Dla 20 postaci wycięte portrety z kart + efekty idle/wygrana/przegrana.
4. 20 ikon WR (mogą dzielić bazowy szablon: śmigło, młotek, VHS, emotka, kac, wampir, glitche).
5. Efekty `+M`, `−M`, Wycisz, Usuń, Ochrona, Przesuń, dociąg, 20:30, żetony, koniec meczu.
6. Rewersy, talia, cięcie, odwrócenie i układy 1/3/5, animacje zapisania do historii.

## Scenarzysta i audio

1. Weryfikacja pisowni i zgód na wizerunki / podpisy / oryginalne głosówki w zakresie 52 grafik.
2. 20 × 6 kwestii z rozdz. 6.3 - w wersji napisowej gotowe do implementacji, z wyraźną etykietą „tekst autorski”.
3. Jedna krótka scena otwarcia, 4 przerywniki aktów i dwa zakończenia.
4. 52 humoryzowane dopowiedzenia wróżb z rozdz. 9.4 + 9 szablonów pozycji i kilka bezpiecznych puent.
5. Lista legalnych sampli Twitch, przyporządkowanie do wydarzeń, wybór alternatywnych dżingli w razie braku licencji.

---

# 17. Miejsca na konkretne starsze i nowsze lore

Poniżej gotowe „kotwice” do umieszczenia w rozdziałach (nie wszystkie muszą być nagraniami; część lepiej działa jako nazwa osiągnięcia, naklejka na ekran lub tekst WR):

| Nawiązanie ze źródeł / listy użytkownika | Proponowane umiejscowienie |
|---|---|
| Nysmo jako sędzia poczekalni | Samouczek Pucharu i kontrola pierwszego stolika; bez bezpośrednich powiązań z wcześniejszą grą |
| „Widzowie nie istnieją” | Okazjonalny żart Czatu, nie cel kampanii; stawką jest Złoty Taboret |
| „Na Caution się nie leczymy!” | Wydarzenie Ostatni Ogórek, tooltip, osiągnięcie, linia Tabo w tutorialu; w karciance nie tworzymy HP |
| „Punkt 20:30 - baczność do Hymnu” | Rytuał w turze 4, misja MaciekWolf92, karta Hymn |
| „WSZYSCY DO BANA” i najlepsza Młotkowa | Karty LtAsiaa/Nysmo/Banhammer i misja 17 |
| „Nie biegasz z Ink Ribbonem” | E02, garaż Pestarza, tutorial karta wydarzenia |
| „Pokaż płyty!” / do weryfikacji książeczki | Misja 14 AL_PSX; WR Ochrona |
| „NOWA META - granie tyłem do ekranu” | E10 Podaj Pilota, scena końcowa PROPLAYER |
| „PORA zrobić porządek!”, „Nic tu kurła nie działa!” | E07, E08, osobne VFX porządkowania/glitchu |
| „To nie jest koncert życzeń... a jednak jest!” | Misja Meeefjuuu, koncert życzeń |
| „Tylko LtAsiaa może rozpalić piec” | E09 Do Pieca!, wpis archiwum|
| „Tabo robi zombiaczki na mięciutko” | Animacja stref Horror / TRUP-POL i rekin |
| „Hymn Tabo”, „Hymn LtAsii” | MaciekWolf92, finał, galeria z opcjonalnymi licencjonowanymi dżinglami |
| „Schowaj platyny!”, „Shinji Mikami”, „Cosplay Homukiego” | Sekretne odznaki, podpisy odkrywanych kart, żarty w dialogach między aktami |
| Obwarzanek jako ukryte słowo w tytule streamu | Karta #31, nagroda easter egg za rozegranie jej na Zapleczu 3 razy |
| 500 Follow / Psychosobota / Tabożeństwo | Karty 05/03/46 i dekoracje kaplicy Macieja |
| Ptak z Dark Souls przy 50 śmierciach; męczony kapucynek | Karty 32/33, scena z WR Wapniaka i wieży B4Norka |
| Wampir z Podlasia / The Blood of Dawnwalker | Karta #35, boss 10, tło nocy |
| Kierowca Śmigłowca i PRAGMATA | Karta #36, boss 12, lot nad monitorem |
| Poród Cydyna i bliźniaki Bartek/Wojtek | Karta #50, boss 09, żetony BLIŹNIAK |
| Jillie i capslock / lawina spamu | Karta #09, boss 05, animowane dymki |
| Qrus i 10k, LtAsiaa i 20k, Nysmo i 10k komentarzy | E22 Wiadomość 10k, galerie wpisów / osiągnięcia |
| Kocha retro/PSX, święte słuchawki, proplayer | Karty 04, 23, 41, tło menu i kosmetyki |
| Piec, zasięg, wieś / nieistniejące streamy | E03, E09, mapa Rozdziału III, loader gry |

**Klipy i opisy streamów:** część źródeł z października 2026 jest tylko tytułem lub automatycznym streszczeniem; nie przypisuj realnym ludziom nowych dosłownych cytatów, jeśli ich nie odsłuchano. W rozdziale 6 wszystkie kwestie zostały celowo oznaczone jako autorskie, aby można je było legalnie i łatwo dopracować z zainteresowanymi.

---

# 17A. Statyczny audyt kosztów i matematyczne ograniczenia (wykonany przy przygotowaniu dokumentu)

Z tabeli w rozdziale 4 policzono dla każdej oryginalnej karty **Moc drukowana + oszacowany ekwiwalent punktowy umiejętności**. To nie jest symulacja rzeczywistych meczów i nie uwzględnia kolejności dociągu. Jej cel to sprawdzenie, czy kosztowne karty nie dostają nieproporcjonalnego, gwarantowanego wyniku już na papierze.

| Koszt | Liczba kart | Średnia wstępna wartość [Moc + efekt] | Budżet z rozdz. 3 | Odchylenie średniej |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2,77 | 3 | −0,23 |
| 2 | 15 | 4,29 | 5 | −0,71 |
| 3 | 15 | 5,39 | 6 | −0,61 |
| 4 | 10 | 6,57 | 7 | −0,43 |
| 5 | 8 | 8,40 | 9 | −0,60 |
| 6 | 1 | 10,00 | 10 | 0,00 |

**Wniosek:** wszystkie sześć grup kosztowych znajduje się średnio w przedziale najwyżej 0,71 punktu poniżej przyjętego budżetu. Jest to celowa, konserwatywna przestrzeń na synergie, przewagę kolejności i dobieranie kart. Nie stanowi dowodu równowagi między pojedynczymi kartami, ponieważ np. Ochrona bywa niewykorzystana, a Wyciszenie i dobór celu mogą być znacznie cenniejsze niż szacunkowe 1–2 punkty.

**Sprawdzenie rozdań:** w talii 18 kart, gdy są 2 kopie danego typu, przy obejrzeniu 10 kart bez dodatkowego doboru szansa trafienia co najmniej jednej wynosi dokładnie **81,699%** z rozkładu hipergeometrycznego. Przy jednej kopii jest to **55,556%**. To uzasadnia dwie kopie do budowania synergii, ale nie zamienia talii w deterministyczną kombinację.

**Pierwsza lista kart do szczególnego testowania:** `07 LtAsiaa` i `E08 Nic Tu Nie Działa` (wyciszenie Aur), `32 Ptak z Dark Souls` i `E21 Wysoki Sądzę` (usuwanie), `28 Orzechowy Rozpruwacz`, `34 TRUP-POL`, `50 Cydyn` (tworzenie punktów i zapełnianie slotów), `47 ELTaboBot` (Finał), `E24 Archiwizuj TaboLOG` (punktowanie w dwóch strefach). Te karty mają największe ryzyko wartości zależnej od kontekstu.

**Zasada uczciwej implementacji:** najpierw zaprogramować logikę, potem wykonać tysiące partii testowych i regularnie stroić liczby - nie rozwiązywać problemów balansu tajnym wzmacnianiem AI. **Nie ma podstaw, by obiecać idealną równowagę bez tych testów.**

---

# 18. Źródła i załączniki wykorzystane przy tworzeniu dokumentu

**Dostarczone przez autora projektu:**

- `Karty_TABOta_52_Pojedyncze_PNG_FINAL(4).zip` - **dokładnie 52 oryginalne pliki kart**, kolejność i tytuły 01–52.
- `Instrukcja wróżenia KARTY TABOta (1)(2).png` - sposób przygotowania, odcięcie, znaczenia symboli i rozkłady 1/3/5.
- `Wklejony tekst(20261025-175724).txt` - zrzut podsumowań streamów, w tym motyw Wampira z Podlasia, kapucynka, obwarzanka, R.E.P.O., 500 Follow i aktualna aktywność widzów.
- `Wklejony tekst (2)(9).txt` - zrzut cytatów z serwisu ELTabo (część wpisów ma ostre słownictwo i humor 18+).
- `Wklejony tekst (3)(6).txt` - lista honorowców i charakterystyki widzów, Moderacji, Pestarza, Cydyna, Gumboxa itp.
- `TABORETRO_Protokol_Zero_Widzow_Scenariusz_GGMAX.md` - wcześniejszy duży scenariusz gry na silniku GameGuru MAX, do którego ten projekt nawiązuje fabularnie; obecna karcianka działa samodzielnie.

**Publicznie dostępne lore (stan sprawdzany 25.10.2026):**

- TaboLore: <https://ltasiaa.github.io/LtAsiaa/TaboLore.html> - w tym zasady „strimy i widzowie nie istnieją”, 20:30 Hymn, Moderacja, Hard, Caution, Ink Ribbon.
- Surowy zapis lore: <https://raw.githubusercontent.com/LtAsiaa/LtAsiaa/refs/heads/Master---Asia/TaboLore.html>.
- TaboLOG: <https://raw.githubusercontent.com/LtAsiaa/LtAsiaa/refs/heads/Master---Asia/TaboLog.html>.
- ELTabo - Podsumowanie streamów: <https://eltabo.pl/podsumowanie-strimow/>; Cytaty: <https://eltabo.pl/cytaty/>; Honorowcy: <https://eltabo.pl/honorowcy/> (pokrewne treści przekazane w plikach).

**Technologia i standardy:**

- Phaser - zdarzenia myszy / pointer oraz animacje: <https://docs.phaser.io/phaser/concepts/input> i <https://docs.phaser.io/phaser/concepts/tweens>.
- Tauri - wieloplatformowy desktop: <https://tauri.app/> i <https://github.com/tauri-apps/tauri>.
- TypeScript: <https://www.typescriptlang.org/>.
- WCAG - dostępność kontrastu i obsługi interfejsu: <https://www.w3.org/WAI/standards-guidelines/wcag/>.

**Podsumowanie założeń i otwartych decyzji:**

- Wersja 1.0 zakłada 20 przeciwników + opcjonalny lustrzany pojedynek, 52 oryginalne karty + 24 nowe wydarzenia, 18 kart na mecz i pełną historię wróżb.
- Statystyki są zaproponowane tak, by miały kontrolowaną wartość w funkcji kosztu; aby uczciwie stwierdzić, że „są wyrównane”, potrzebne są implementacja resolvera, symulacje i playtesty ludzi. Nie udajemy, że same szacunki zastępują te kroki.
- Trzeba potwierdzić zgody na wykorzystanie portretów, nicków i wszelkich autentycznych wycinków audio w samodzielnej grze dystrybuowanej publicznie. Teksty kwestii dialogowych z dokumentu są autorskie i może je nagrać dowolny uprawniony lektor po zatwierdzeniu przez twórców.
- Najpierw dostarcz P1 (Tutorial + 3 bossów + wróżba 1 karta jako spike UX), dopiero później rozszerz do całości. Zachowanie wysokiej jakości reakcji kursora i czytelności w każdej fazie jest obowiązkowe.

---

## Ostateczna definicja gry w jednym zdaniu

**Karty TABOta: WSZYSCY DO BANA!** to animowana, jednoosobowa gra karciana, w której Tabo wygrywa co najmniej dwie z trzech stref podczas sześciu tur, przechodzi 20 fabularnych rozpraw z własnymi regułami i odblokowuje 76 typów kart, a w osobnym niezależnym trybie wróży z 52 oryginalnych Kart TABOta i zachowuje lokalną historię pytań, układów oraz interpretacji.

