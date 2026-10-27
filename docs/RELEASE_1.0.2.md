# Karty TABOta - 1.0.2

Data wydania: 27.10.2026. Platformy: Windows x64 i Linux x86_64.

## Zmiany

- Przycisk „Rytuał” w prawym panelu meczu pozwala ponownie otworzyć okno
  wyboru rytuału po jego zamknięciu bez dokonania wyboru.
- Przycisk jest aktywny tylko wtedy, gdy można zagrać rytuał. Po dodaniu
  rytuału do planu staje się nieaktywny.
- Automatyczne otwieranie okna wyboru rytuału nadal działa.

## Uruchomienie

Rozpakuj całe archiwum. Zachowaj katalog `_internal` obok programu.

- Windows: `TABOt/TABOt.exe`.
- Linux: `TABOt/TABOt`.

Nie potrzeba instalacji Pythona. Zapisy gry pozostają w dotychczasowym katalogu
użytkownika; archiwa nie zawierają danych gracza.

## Weryfikacja

105 testów na każdym interpreterze oraz uruchomienie gotowych programów
i renderowanie planszy. Windows sprawdzono pod Wine. Linux zbudowano
na Bazzite 44; zgodność ze starszymi dystrybucjami nie jest zweryfikowana.
