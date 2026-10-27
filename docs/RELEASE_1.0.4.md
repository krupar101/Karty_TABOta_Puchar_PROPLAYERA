# Karty TABOta - 1.0.4

Data wydania: 27.10.2026. Platformy: Windows x64 i Linux x86_64.

## Zmiany

- Czytelna etykieta „OCHRONA” zamiast zielonego rombu na chronionych kartach,
  w tym MackoTheHollow. Podgląd karty wyjaśnia działanie statusu.
- Pełny audyt fabuły NORMAL: 10 000 symulacji, po 500 dla każdego z 20
  pojedynków, z przypisanymi taliami, regułami walk i omylnym graczem.
- Potwierdzona legalna ścieżka przejścia wszystkich czterech aktów oraz
  zapis i odczyt postępu. Każdy przeciwnik został wielokrotnie pokonany.
- Balans bez zmian: testy nie wykazały potrzeby jego korekty.
- Powtarzalny skrypt audytu, wyniki i zwycięskie przebiegi w repozytorium.

Wersja 1.0.4 następuje bezpośrednio po 1.0.2; 1.0.3 nie była publikowana.

## Uruchomienie

Rozpakuj całe archiwum. Zachowaj katalog `_internal` obok programu.

- Windows: `TABOt/TABOt.exe`.
- Linux: `TABOt/TABOt`.

Nie potrzeba instalacji Pythona. Zapisy gry pozostają w dotychczasowym katalogu
użytkownika; archiwa nie zawierają danych gracza.

## Weryfikacja

110 testów regresji na każdym interpreterze, kontrola etykiety Ochrony w Qt
w dwóch rozdzielczościach i uruchomienie gotowych paczek z renderowaniem planszy.
Windows sprawdzono pod Wine, bez testu na natywnym Windowsie. Linux zbudowano
na Bazzite 44; zgodność ze starszymi dystrybucjami nie jest zweryfikowana.

Wyniki symulatora są przybliżeniem zachowania omylnego gracza, nie pomiarem
odsetka zwycięstw ludzi. Szczegóły: [raport audytu fabuły](https://github.com/krupar101/Karty_TABOta_Puchar_PROPLAYERA/blob/v1.0.4/docs/STORY_AUDIT_2026-10-27.md).
