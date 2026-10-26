"""Read the author's content tables without transcribing names or changing artwork.

Game_Design.md is shipped with the game and is also its content source. Rules are
implemented separately in engine.py; prose is never executed as code.
"""
from pathlib import Path
import re
import sys
import unicodedata
from collections import Counter

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
DOCUMENT = (ROOT / "Game_Design.md").read_text(encoding="utf-8")
LANES = ["STREAM", "CZAT", "ZAPLECZE"]
ACTS = ["Ty w ogóle umiesz w to grać?", "Każdy ma własną metę", "To nie jest koncert życzeń", "Ostateczny finał. Naprawdę. Chyba."]
STARTER = ["01", "02", "04", "06", "10", "31", "41", "43", "E01", "E03", "E05", "E07"]
PORTRAITS = [8, 11, 30, 13, 9, 10, 21, 17, 50, 35, 29, 36, 19, 23, 12, 22, 7, 51, 48, 47]


def clean(s):
    return s.replace("**", "").replace("`", "").strip()


def name_key(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower().replace("ł", "l")) if not unicodedata.combining(c))


def table(section):
    for line in section.splitlines():
        if line.startswith("|"):
            parts = [clean(x) for x in line.split("|")[1:-1]]
            if re.fullmatch(r"E?\d{2}", parts[0]):
                yield parts


def expand(text):
    result = []
    for part in text.split(","):
        key, _, count = part.strip().partition("×")
        result.extend([key] * int(count or "1"))
    return result


CARDS = {}
for row in table(DOCUMENT.split("# 4. Katalog")[1].split("## 4.1.")[0]):
    cid, name, cost, power, tag, description = row
    image = next((ROOT / "karty-front").glob(cid + "_*.png"))
    CARDS[cid] = dict(id=cid, name=name, cost=int(cost), power=int(power), tag=tag,
                      description=description, kind="unit", image=str(image),
                      nameKey=name_key(name), trigger="aura" if description.startswith("Aura:") else
                      "final" if description.startswith("Finał:") else "entry" if description.startswith("Wejście:") else "none")
for row in table(DOCUMENT.split("# 5. Rozszerzenie")[1].split("## 5.1.")[0]):
    cid, name, cost, description, flavor = row
    CARDS[cid] = dict(id=cid, name=name, cost=int(cost), power=0, tag="Wydarzenie",
                      description=description, flavor=flavor, kind="event", image="", nameKey=name_key(name), trigger="entry")

# Resolve two contradictory descriptions in the GDD explicitly; see docs/DECISIONS.md.
CARDS["23"]["description"] = "Wejście: jeśli przed wystawieniem twoje ZAPLECZE było puste, dobierz 1 kartę. Zachowuje bazową Moc 4."
CARDS["26"]["description"] = "Wejście: usuń do 2 punktów Osłabienia z jednej własnej jednostki w tej strefie. Nie daje dodatniego wzmocnienia."

FORTUNES = {r[0]: r[2] for r in table(DOCUMENT.split("## 9.4.")[1].split("## 9.5.")[0])}
ENCOUNTERS = []
deck_rows = list(table(DOCUMENT.split("# 12A.")[1].split("# 13.")[0]))
for i, block in enumerate(DOCUMENT.split("### Rozprawa ")[1:21]):
    def field(label):
        match = re.search(r"\*\*" + re.escape(label) + r":\*\* ([^\n]+)", block)
        return clean(match.group(1)) if match else ""
    headline = block.splitlines()[0].split(" - ", 1)[1]
    reward = field("Nagroda za pierwsze zwycięstwo")
    original_reward = reward.split("wydarzenie")[0]
    unlocks = re.findall(r"\b(\d{2})\s+", original_reward)
    unlocks += re.findall(r"\bE\d{2}\b", reward)
    dialogue = dict(re.findall(r"- \*\*(START|WR|LEAD|TRAIL|LOSE|WIN)\*\* - „([^”]+)”", block))
    scene = re.search(r"\*\*Sceneria:\*\* (.*?) ·", block)
    story = re.search(r"\*\*Sytuacja fabularna\.\*\* ([^\n]+)", block)
    rule = field("Unikalny Warunek Rozprawy")
    ENCOUNTERS.append(dict(id=i+1, name=headline, short=headline.split(" - ")[0], act=ACTS[i//5],
        scene=scene.group(1) if scene else "", story=story.group(1) if story else "",
        rule=rule, ruleName=rule.split(": ")[0], hardRule=field("Remix PROPLAYER"),
        dialogue=dialogue, unlocks=list(dict.fromkeys(unlocks)), portrait=f"{PORTRAITS[i]:02}",
        storyDeck=expand(deck_rows[i][1]), enemyDeck=expand(deck_rows[i][2])))

# Replace technical wording from the design source with player-facing phrasing.
if len(ENCOUNTERS) >= 3:
    ENCOUNTERS[2]["rule"] = "NIE WIDZĘ A: pierwsza własna jednostka bez litery „A” w nazwie, zagrana na CZACIE w każdej turze, dostaje +1 (symetrycznie)."
    ENCOUNTERS[2]["hardRule"] = "W HARD również ostatnia własna jednostka z literą „A” zagrana na CZACIE w tej turze traci −1 (symetrycznie; minimalnie do 0)."

for key, name, power, tag in [("T1", "STOŁEK", 2, "Technika"), ("T2", "TRUPEK", 2, "Horror"), ("T3", "BLIŹNIAK", 1, "Widz")]:
    CARDS[key] = dict(id=key, name=name, power=power, cost=0, tag=tag, description="Żeton. Zajmuje miejsce w strefie.",
                      kind="token", image="", nameKey=name_key(name), trigger="none")


def encounter_rule(mission, hard=False, tutorial=False):
    """The effective rule, without displaying replaced NORMAL conditions in HARD."""
    encounter = ENCOUNTERS[mission-1]
    if mission == 1:
        if hard:
            return "PRÓBA SEZONOWCA: pierwsza jednostka Moderacji zagrana na CZACIE w każdej turze otrzymuje +1 Mocy (dla każdej strony osobno). Plany obu stron są ukryte."
        if not tutorial:
            return "PRÓBA SEZONOWCA: pojedynek na podstawowych zasadach, bez dodatkowych premii. Plany obu stron są ukryte. Jawne ruchy w turach 1–3 są dostępne tylko podczas nauki gry."
    if not hard:
        return encounter["rule"]
    replacements = {
        2: "Pierwsza własna jednostka Retro zagrana na ZAPLECZU w meczu otrzymuje +2 Mocy.",
        6: "Po turach 2, 3 i 5 każda strona dostaje +1 punkt w swojej strefie z najmniejszą liczbą własnych jednostek, o ile nie jest pusta. Remis: STREAM → CZAT → ZAPLECZE.",
        7: "Pierwsza własna jednostka zagrana na ZAPLECZU w turach 1–3 otrzymuje +2 Mocy w turze 1 albo +1 w turze 2 lub 3. Tylko raz na stronę w meczu.",
        8: "Pierwsza własna jednostka Chaos zagrana na STREAM w każdej turze otrzymuje +1 Mocy.",
        9: "Po turze 3 każda strona otrzymuje BLIŹNIAKA o Mocy 1 w strefie z najniższym własnym wynikiem, jeżeli jest w niej miejsce. Remis: CZAT → STREAM → ZAPLECZE.",
        10: "Pierwsza własna jednostka Horror zagrana na ZAPLECZU w turze 6 otrzymuje +2 Mocy. Raz na stronę w meczu.",
        11: "Pierwsze DWIE różne własne jednostki przesunięte w meczu otrzymują po +1 Mocy. Ponowne przesunięcie tej samej karty nie daje premii.",
        14: "Pierwsza własna jednostka Retro zagrana w dowolnej strefie, gdy masz w ręce co najmniej 2 różne karty Retro (licząc zagrywaną), otrzymuje Ochronę. Raz na stronę w meczu.",
        15: "Po turach 3 i 5 w każdej strefie z co najmniej 2 własnymi jednostkami najsłabsza z nich dostaje −1 Mocy. Przy remisie wybierana jest starsza. Ochrona nie blokuje tej reguły.",
        19: "Po Finałach każda strona otrzymuje karę w każdej swojej strefie: −1 punkt przy 2 jednostkach, −3 punkty przy 3–4 jednostkach. Kara dotyczy wyniku strefy, nie Mocy kart.",
        20: "W turze 2 na ZAPLECZU, w turze 4 na STREAM, w turze 6 na CZACIE pierwsze Wejście każdej strony zostaje wyłączone. Dotyczy jednostek i wydarzeń; koszt zostaje wydany. Bazowa Moc, Aury, Finały i Rytuał działają normalnie.",
    }
    if mission in replacements:
        return encounter["ruleName"] + ": " + replacements[mission] + " Zasada działa na obie strony."
    return encounter["rule"] + "\n\n" + encounter["hardRule"]


def validate_deck(deck, unlocked=None, offer=None, require_opening=True):
    errors = []
    if not isinstance(deck, list) or any(not isinstance(c, str) or c not in CARDS or CARDS[c]["kind"] == "token" for c in deck):
        return ["Talia zawiera nieznane karty."]
    if len(deck) != 18:
        errors.append(f"Wybierz dokładnie 18 kart ({len(deck)}/18).")
    if any(n > 2 for n in Counter(deck).values()):
        errors.append("Maksymalnie 2 kopie każdego typu.")
    if sum(CARDS[c]["kind"] == "unit" for c in deck) < 12:
        errors.append("Potrzebujesz co najmniej 12 jednostek.")
    if sum(CARDS[c]["kind"] == "event" for c in deck) > 6:
        errors.append("Możesz użyć najwyżej 6 wydarzeń.")
    if require_opening and not any(CARDS[c]["kind"] == "unit" and CARDS[c]["cost"] <= 1 for c in deck):
        errors.append("Dodaj przynajmniej jedną jednostkę za ⚡ 1, aby móc zagrać w pierwszej turze.")
    if unlocked is not None and any(c not in unlocked for c in deck):
        errors.append("Talia zawiera nieodblokowane karty.")
    if offer is not None and Counter(deck) - Counter(offer):
        errors.append("Wybieraj wyłącznie karty z tej oferty draftu.")
    return errors
