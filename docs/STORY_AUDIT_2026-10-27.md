# Fabuła NORMAL - audyt i poprawka Ochrony (2026-10-27)

Zakończono pełną weryfikację wszystkich 20 pojedynków w czterech aktach: **10 000 gier (500 na pojedynek)**. Każdy przeciwnik został pokonany legalnie, na przypisanej talii fabularnej. Nie wykryto blokad ukończenia ani naruszeń kontrolowanych niezmienników. **Balans pozostaje bez zmian**; nie przyjmowano docelowych procentów zwycięstw.

## Zielony romb na Macko

Romb pochodził z `Card.qml` i oznaczał stan `protected`. MackoTheHollow (18) może wybrać siebie jako własną jednostkę i otrzymać Ochronę także w pojedynku 05 z Jillie_Studio. Pierwszy wrogi efekt zużywa Ochronę, a następny działa normalnie. To prawidłowa zdolność, lecz oznaczenie było niejasne.

Zastąpiono romb etykietą **OCHRONA**, umieszczoną poniżej oznaczeń kosztu/nazwy. Dodano objaśnienie „blokuje jeden wrogi efekt, po czym znika” w podglądzie bieżącej karty, dymku i nazwie dostępności. Status nie jest wyświetlany na zakrytej karcie. Zweryfikowano renderowanie prawdziwego stanu walki z Macko w 1280×720 i 960×600, bez ostrzeżeń QML.

## Metoda

- Wyłącznie FABUŁA NORMAL (`hard=False`), rzeczywiste `storyDeck` i `enemyDeck` z treści gry. Bez draftu i własnych talii.
- Rywal stosuje produkcyjne `campaign_difficulty`: beginner/casual/easy/normal w aktach I–IV. Ustawienie NORMAL w kampanii celowo tak stopniuje AI; wymuszenie normalnego AI w każdym akcie nie odpowiadałoby grze.
- Gracz wybiera heurystykę normal w 80% tur, a mniej dokładną easy w 20%. Obie korzystają tylko z informacji publicznych i własnej ręki. W tej próbie 8325 tur miało faktycznie inny plan wskutek mniej dokładnej decyzji. To przybliżenie rozsądnego, omylnego gracza, nie zmierzony model zachowania ludzi ani rozwiązanie optymalne.
- Gracz wymienia do dwóch kart o koszcie co najmniej 4; rywal zachowuje rękę, jak w aplikacji. Różne ziarna zmieniają rozdania, kolejność talii i decyzje. Ziarna: numer pojedynku × 100000 + 0…499.
- Wszystkie plany zatwierdza rzeczywiste `Match.commit` z walidacją `project`. Reguły centralne, rytuały, darmowy lot, naprzemienne rozstrzyganie, dobieranie, odrzucanie i finały wykonuje silnik produkcyjny. Nie dopisuje się do planu kart dobranych w czasie rozstrzygnięcia.
- Po każdej turze: kontrola energii, limitu ręki i stref, mocy/wzmocnień, właściciela/strefy, unikatowości identyfikatorów i zachowania wszystkich kart nietokenowych. Każda walka musi zakończyć się w 6 turach (pojedynek 16: 7); żaden wybór nie może pozostać nierozwiązany.
- Remisy liczone osobno, nie jako zwycięstwa. Wyjątki i blokady zapisują ziarno oraz błąd i powodują niepowodzenie audytu.

## Wyniki końcowe

| Akt | Pojedynek | Przeciwnik | Wygrane | Przegrane | Remisy | Wygrane / 500 |
|---|---|---|---:|---:|---:|---:|
| 1 | 01 | ToTylkoNysmo | 341 | 154 | 5 | 68.2% |
| 1 | 02 | GreedN3 | 464 | 31 | 5 | 92.8% |
| 1 | 03 | Gumbox | 447 | 53 | 0 | 89.4% |
| 1 | 04 | MaciekWolf92 | 391 | 103 | 6 | 78.2% |
| 1 | 05 | Jillie_Studio | 430 | 66 | 4 | 86.0% |
| 2 | 06 | QrusKnur | 358 | 132 | 10 | 71.6% |
| 2 | 07 | Pestarz | 365 | 129 | 6 | 73.0% |
| 2 | 08 | Krisuroku | 441 | 56 | 3 | 88.2% |
| 2 | 09 | Cydyn | 428 | 66 | 6 | 85.6% |
| 2 | 10 | Wampir z Podlasia | 344 | 149 | 7 | 68.8% |
| 3 | 11 | B4Nork | 289 | 198 | 13 | 57.8% |
| 3 | 12 | Kierowca Śmigłowca | 246 | 242 | 12 | 49.2% |
| 3 | 13 | Meeefjuuu | 276 | 218 | 6 | 55.2% |
| 3 | 14 | AL_PSX | 380 | 108 | 12 | 76.0% |
| 3 | 15 | InfinityPotato0 | 311 | 179 | 10 | 62.2% |
| 4 | 16 | Pierd0la | 269 | 218 | 13 | 53.8% |
| 4 | 17 | LtAsiaa | 314 | 183 | 3 | 62.8% |
| 4 | 18 | KruparGames | 251 | 232 | 17 | 50.2% |
| 4 | 19 | Wapniak | 199 | 281 | 20 | 39.8% |
| 4 | 20 | ELTaboBot | 243 | 239 | 18 | 48.6% |

| Akt | Wygrane / wszystkie gry | Odsetek zwycięstw |
|---|---:|---:|
| 1 | 2073 / 2500 | 82.92% |
| 2 | 1936 / 2500 | 77.44% |
| 3 | 1502 / 2500 | 60.08% |
| 4 | 1276 / 2500 | 51.04% |

Trudność rośnie na poziomie średnich aktów. Poszczególne walki nie tworzą idealnie rosnącej skali: np. AL_PSX (14) jest w tym modelu łatwiejszy od sąsiadów. Najniższy wynik ma Wapniak (19): 39,8%, najwyższy GreedN3 (02): 92,8%. Każda walka ma wiele zwycięstw i porażek. Bez docelowych progów i danych od ludzi sama lokalna różnica nie uzasadnia zmiany talii ani reguł.

## Przejście kampanii i końcowa weryfikacja

Dla każdego pojedynku zapisano pierwszy zwycięski przebieg: ziarno, wymianę, plany obu stron, wybory odrzucania i końcowy wynik stref. Wszystkie 20 przebiegów odtworzono ponownie przez silnik, bez wywoływania polityki gracza. W świeżym profilu sprawdzono dostępność każdej kolejnej walki oraz legalność talii względem dotychczasowych nagród, przyznano rzeczywiste nagrody przez `Storage.reward`, zapisano profil i odczytano komplet ukończeń 1–20.

To potwierdza istnienie legalnej ścieżki przejścia kampanii z możliwością ponawiania walk, a nie gwarancję zwycięstwa przy dowolnym rozdaniu ani przejścia bez porażki. Osobno odtworzono zwycięski samouczek: obowiązkowe ruchy tur 1–3 i demonstracyjna talia rywala; nie wliczono go do 10 000 standardowych walk.

Końcowy pełny przebieg zakończony pomyślnie. Po nim nie zmieniano silnika, talii, reguł ani polityki symulacji. Nie było poprawek balansu wymagających kolejnego przebiegu.

## Artefakty i odtworzenie

- [Pełny JSON z wynikami, regułami, taliami, zwycięskimi zapisami i hashami źródeł](audits/story-normal-2026-10-27.json).
- `scripts/audit_campaign.py` - powtarzalny audyt z kodem wyjścia niezerowym przy błędzie lub braku zwycięstwa.
- `scripts/check_protection.py` - kontrola Qt oraz zrzuty `test-artifacts/protection-1280.png` i `protection-960.png`.
- Testy regresji: **110 testów, OK**, w tym legalność mniej dokładnych decyzji, brak dostępu do ukrytych informacji, odtwarzanie zwycięstwa i jednorazowe zużycie Ochrony.

```bash
.venv/bin/python scripts/audit_campaign.py --games-per-duel 500 --workers 4
QT_QPA_PLATFORM=offscreen .venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/check_protection.py
```

Symulacje sprawdzają produkcyjny silnik i wykrywają obserwowane problemy, lecz nie są formalnym dowodem poprawności wszystkich możliwych interakcji ani pomiarem odsetka zwycięstw rzeczywistych graczy. Testy istniejących reguł w `tests/test_engine.py` uzupełniają kontrolę wspólnego silnika.
