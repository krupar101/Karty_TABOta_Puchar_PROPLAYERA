# Przegląd gry - 26.10.2026

## Muzyka i efekty

Tło reaguje na **rzeczywisty sygnał PCM odtwarzanej muzyki**. 24 pasma
częstotliwości poruszają ciche wizualnie słupki, punkty i okręgi. Analiza obejmuje
oba odtwarzacze podczas przenikania, uwzględnia ich głośność i ściszenie pod
dżinglem. Muzyka wyłączona, głośność zero lub ograniczone animacje wygaszają
wizualizację. Brak sygnału nie zastępuje muzyki przypadkową animacją.

Analizator korzysta z [QAudioBufferOutput w Qt](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QAudioBufferOutput.html),
bez nowej zależności, dodatkowego dekodera ani mikrofonu. Limit: 1024 próbki,
24 pasma, do 20 aktualizacji na sekundę na odtwarzacz. Oddzielny sygnał Qt
aktualizuje tylko tło; nie przelicza planszy ani nie zapisuje kampanii.

Uzupełnione efekty: hover kart, przyciski (także działania wyłącznie w QML),
wybór karty i podglądu, wymiana/tasowanie, położenie karty, cofnięcie, zatwierdzenie
i początek tury, rytuał, błąd niedozwolonej akcji oraz neutralny remis.
Hover jest cichszy i ograniczony czasowo; nie przerywa ważniejszych efektów.
Ogólny klik nie zastępuje dźwięku konkretnej akcji. Próbki powstają raz podczas
uruchamiania, nie przy każdym najechaniu. Pozostają oddzielne ustawienia muzyki
i efektów.

Test na lokalnym urządzeniu audio: prawdziwy M01.mp3 dał 67 aktualizacji widma
w około 3 sekundy, wyciszenie wyzerowało pasma; pięć efektów przesłano do
QAudioSink. To weryfikuje odtwarzanie i analizę, nie zastępuje subiektywnego odsłuchu.

## Interfejs i zasady

- „Autorzy i zasady” zawiera widoczną notkę **Autor gry: KruparGames**.
- Usunięto przypisywanie `undefined` do etykiety karty, które wcześniej powodowało
  ostrzeżenia QML na wszystkich ekranach.
- Briefing ma przewijany opis oraz stałe, zawsze dostępne przyciski na dole.
  Nagłówki zawijają długie nazwy aktów. Panel planu ustawia się pod kontrolkami
  reguły i rytuału, również przy długich nazwach i przycisku darmowego lotu.
- Każdy wariant pokazuje jeden **obowiązujący opis reguły**. HARD zastępujący
  regułę NORMAL nie wyświetla już równocześnie sprzecznych warunków
  (np. STREAM w turach 5–6 i ZAPLECZE tylko w turze 6 w pojedynku 10).
- Pojedynek 01 odróżnia naukę z jawnymi ruchami od zwykłego rewanżu.
- BAN jest wyłączony w pojedynku 17 HARD i gdy nie ma legalnego celu.
- „A / BEZ A” dotyczy specjalnej reguły pojedynku 03, ale także **Aury Gumboxa
  w każdym innym pojedynku**, kiedy Gumbox jest na publicznej planszy lub w ręce
  gracza. Ukryta ręka rywala nie wpływa na oznaczenia. Uwzględnione są żetony
  oraz normalizacja liter, np. Ą = A. Wydarzenia nie dostają tej etykiety.

Sprawdzono 17 ekranów i 324 widoki pojedynków: 20 przeciwników × NORMAL/HARD ×
1280×720/960×600 × briefing/warunek/wymiana/tura 4, plus tura 7 pojedynku 16.
Test czeka również na zakończenie asynchronicznego ładowania ilustracji.
Brak ostrzeżeń QML, błędów obrazów i kolizji sprawdzanych obszarów kontrolek.
Przejrzano również zestawienia zrzutów wszystkich briefingów i plansz.

Test interakcji przechodzi myszką i klawiaturą przez pełny samouczek, jego
niezmieniony wynik 15:10:13 do 20:8:5, zapis/wznowienie, nagrody, warunek przed
wymianą, draft HARD, preset i wróżbę. Osobne próby sprawdzają hover, przeciąganie,
przejścia ekranów i zamykanie modali. Zaktualizowano stare skrypty QA do obecnych
etykiet, graficznego wyboru celu i rejestracji QQuickWindow w PySide6.

## Balans

Zmieniono tylko cztery talie przeciwników/wyzwań w źródłowej tabeli 12A GDD:

| Pojedynek | Zmiana | Powód |
| --- | --- | --- |
| 09 | Rywal: jeden Drakson (26) → Top Chatter (42) | Więcej synergii Widzów i mniejsza przewaga gracza przed końcem aktu. |
| 10 | Gracz: E04 → Magiccorn (24), B4Nork (29) → drugi TaboRanek (43), Nysmo (08) → QrusKnur (10) | Lepsze wczesne zagrania i samodzielna Moc; E04 nie miało Gumboxa do pełnej premii. |
| 14 | Rywal: Sprawdź Płyty (E14) → Pestarz (21) | Bardziej konkurencyjna, nadal tematyczna talia Retro. |
| 18 | Rywal: E11 → QrusKnur (10), E14 → Pestarz (21) | Mniej sytuacyjnych wydarzeń; mocniejsza walka o premiowane Zaplecze. |

Nie zmieniono statystyk kart, nagród, reguł silnika, limitów talii ani samouczka.
Talie są legalne, a gotowe talie gracza korzystają wyłącznie z kart dostępnych
na danym etapie. Bieżące zapisane mecze zachowują swoje rozdanie; korekty talii
obowiązują przy rozpoczęciu nowego pojedynku.

### Diagnostyka talii: ten sam gracz automatyczny po obu stronach

8000 partii przed i 8000 po zmianach, po 200 rozdań na każdy z 40 wariantów,
AI NORMAL po obu stronach, te same seedy `misja * 100000 + 0..199`.
Poniżej odsetek zwycięstw strony gracza w NORMAL. To **nie jest prognoza szans
człowieka**: bot nie zna ukrytych planów i ma ograniczoną ocenę przyszłych efektów.
Pojedynek 01 w tej tabeli jest rewanżem przeciw AI NORMAL; prawdziwa kampania
stosuje tam AI EASY, a nauka ma osobny, deterministyczny scenariusz.

| Pojedynek | Przed | Po |
| --- | --- | --- |
| 01 | 28.0% | 28.0% |
| 02 | 70.0% | 70.0% |
| 03 | 69.5% | 69.5% |
| 04 | 51.0% | 51.0% |
| 05 | 43.0% | 43.0% |
| 06 | 47.5% | 47.5% |
| 07 | 41.5% | 41.5% |
| 08 | 65.0% | 65.0% |
| 09 | 74.0% | 66.0% |
| 10 | 22.5% | 41.5% |
| 11 | 38.0% | 38.0% |
| 12 | 42.0% | 42.0% |
| 13 | 44.5% | 44.5% |
| 14 | 73.5% | 61.0% |
| 15 | 54.0% | 54.0% |
| 16 | 59.0% | 59.0% |
| 17 | 64.0% | 64.0% |
| 18 | 71.0% | 55.0% |
| 19 | 46.5% | 46.5% |
| 20 | 52.0% | 52.0% |

Każdy z 40 wariantów ma potwierdzone zwycięstwa gracza. Wszystkie partie
zakończyły się poprawnie; sprawdzano energię, limit ręki, pojemności stref,
zakres wzmocnień i nieujemną Moc.

### Próba w konfiguracji kampanii

Osobna próba 4000 partii na seedach z przesunięciem 10000 używała poziomów
przeciwnika zgodnych z grą: EASY w 01–02, NORMAL w dalszej fabule, HARD w
PROPLAYER. HARD korzystał z draftu pełnej kolekcji, wybieranego przez Autoułóż.
Nie modeluje to wczesnego odblokowania HARD w Opcjach ani ręcznie zoptymalizowanej
talii. Każdy etap i wariant miał zwycięskie rozdania.

Po ostatniej korekcie pojedynku 10 wykonano dodatkową, niezależną próbę 800
partii z przesunięciem 20000 (400 na wariant). Wynik: **36,5% zwycięstw w fabule,
28% w HARD** dla automatycznego gracza NORMAL. Boss pozostaje wymagający,
a zwycięstwa występują także na rozdaniach nieużywanych do strojenia talii.

Wyniki symulacji są wskaźnikiem doboru talii, a nie zastępstwem testów z ludźmi.
Wszystkie automatyczne pomiary wykonano na Linuxie; nie wykonano osobnego testu
odtwarzania na Windows/macOS.

## Odtworzenie kontroli

```bash
python -m unittest discover -s tests
python scripts/check_ui.py
python scripts/check_encounters.py
python scripts/check_interactions.py
python scripts/check_hover.py
python scripts/check_fades.py
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software python scripts/check_drag.py
python scripts/simulate.py --games 8000 --output test-artifacts/balance-after.json
python scripts/simulate.py --games 4000 --mode campaign --seed-offset 10000 --output test-artifacts/campaign-validation.json
python scripts/check_audio.py --sfx
```

Ostatnie polecenie faktycznie odtwarza muzykę i efekty; wymaga lokalnego urządzenia
audio. Zrzuty i szczegółowe raporty JSON znajdują się w ignorowanym przez Git
katalogu `test-artifacts/`; powyższe podsumowanie pozostaje w dokumentacji projektu.
