"""Atomic local persistence; campaign and private readings are independent."""
from collections import Counter
from datetime import datetime
import json
import os
from pathlib import Path
import random
import shutil
import sys
import uuid

from .content import CARDS, FORTUNES, STARTER, ENCOUNTERS, validate_deck

SCHEMA = 1
POSITIONS = {1: ["Odpowiedź"], 3: ["Przeszłość", "Teraz", "Przyszłość"],
             5: ["Sytuacja", "Problem", "Rada", "Chaos", "Finał"]}
INTRO = {"Odpowiedź": "Potraktuj ten symbol jako zaproszenie: ", "Przeszłość": "Z przeszłości zostaje wskazówka: ",
         "Teraz": "W tej chwili przyjrzyj się temu: ", "Przyszłość": "Na dalszą drogę zabierz myśl: ",
         "Sytuacja": "Tło twojej historii: ", "Problem": "Przyjrzyj się przeszkodzie: ", "Rada": "Mała rada na dziś: ",
         "Chaos": "Nieprzewidziany zwrot akcji: ", "Finał": "Na zakończenie tej historii: "}


def data_directory():
    override = os.environ.get("TABOTA_DATA_DIR")
    if override: return Path(override)
    if sys.platform == "win32":
        base, old_name = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")), "TABOta"
    elif sys.platform == "darwin":
        base, old_name = Path.home() / "Library/Application Support", "TABOta"
    else:
        base, old_name = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")), "tabota"
    destination, legacy = base / "Tabot", base / old_name
    if not destination.exists() and legacy.is_dir():
        # Copy atomically; retain the original as a recovery copy.
        temporary = base / ("Tabot-migration-" + uuid.uuid4().hex)
        try:
            shutil.copytree(legacy, temporary)
            temporary.rename(destination)
        finally:
            if temporary.exists(): shutil.rmtree(temporary)
    return destination


def stamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def new_profile(name="Taboret"):
    return dict(name=name[:60], completed=[], hardCompleted=[], unlocked=STARTER[:], presets=[],
                match=None, plan=[], updated=stamp(), tutorialDone=False, hard=False, offer=[], deck=[], mode="story")


def validate_match(s):
    if not isinstance(s, dict) or s.get("version") != 1: raise ValueError("Nieznana wersja meczu.")
    if type(s.get("mission")) is not int or not 1 <= s["mission"] <= 20: raise ValueError("Niepoprawna misja.")
    if type(s.get("turn")) is not int or not 1 <= s["turn"] <= 7: raise ValueError("Niepoprawna tura.")
    if s.get("maxTurns") != (7 if s["mission"] == 16 else 6): raise ValueError("Niepoprawny limit tur.")
    for key in ["hard", "finished", "tutorial"]:
        if type(s.get(key)) is not bool: raise ValueError("Niepoprawny stan meczu.")
    if s.get("winner") not in [None, -1, 0, 1] or type(s.get("seed")) is not int: raise ValueError("Niepoprawny wynik lub seed.")
    if not isinstance(s.get("flags"), dict) or not isinstance(s.get("log"), list) or any(not isinstance(x,str) for x in s["log"]): raise ValueError("Niepoprawny log meczu.")
    if not isinstance(s.get("actions"), list) or len(s["actions"]) > 7: raise ValueError("Niepoprawna historia ruchów.")
    if not isinstance(s.get("choices"), list) or any(not isinstance(c,dict) or c.get("owner") not in [0,1] or c.get("kind") != "discard" for c in s["choices"]): raise ValueError("Niepoprawny wybór.")
    if type(s.get("serial")) is not int or s["serial"] < 0: raise ValueError("Niepoprawny licznik instancji.")
    for k in ["deck", "hand", "discard", "board", "points", "hymn", "nextBuff", "energy", "mulligan"]:
        if not isinstance(s.get(k), list) or len(s[k]) != 2: raise ValueError(f"Niepoprawny stan: {k}.")
    if "initialDecks" in s:
        decks = s["initialDecks"]
        if not isinstance(decks, list) or len(decks) != 2 or any(not isinstance(d, list) or any(not isinstance(c, str) or c not in CARDS for c in d) or validate_deck(d) for d in decks):
            raise ValueError("Niepoprawne talie początkowe.")
    seen = set()
    for p in range(2):
        if any(not isinstance(s[k][p],list) for k in ["deck","hand","discard","board","points","hymn","nextBuff"]): raise ValueError("Niepoprawny stan gracza.")
        if len(s["hand"][p]) > 10 or len(s["deck"][p]) > 18 or len(s["discard"][p]) > 100: raise ValueError("Zbyt wiele kart.")
        if any(c not in CARDS or CARDS[c]["kind"] == "token" for c in s["deck"][p]): raise ValueError("Nieznana karta.")
        if type(s["energy"][p]) is not int or not 0 <= s["energy"][p] <= s["turn"]: raise ValueError("Niepoprawna Energia.")
        for k in ["board", "points", "hymn", "nextBuff"]:
            if len(s[k][p]) != 3: raise ValueError("Niepoprawna liczba stref.")
        for l, row in enumerate(s["board"][p]):
            limit = 5 if s["mission"] == 5 and s["hard"] and l == 1 else 4
            if not isinstance(row, list) or len(row) > limit: raise ValueError("Zbyt wiele slotów.")
            if any(not isinstance(u,dict) or u.get("lane") != l for u in row): raise ValueError("Niepoprawna strefa jednostki.")
            if not isinstance(s["points"][p][l], int) or abs(s["points"][p][l]) > 500: raise ValueError("Niepoprawne punkty.")
            if type(s["hymn"][p][l]) is not bool or type(s["nextBuff"][p][l]) is not int or not 0 <= s["nextBuff"][p][l] <= 4: raise ValueError("Niepoprawny znacznik.")
        for u in s["hand"][p] + s["discard"][p] + sum(s["board"][p], []):
            if not isinstance(u, dict) or u.get("card") not in CARDS: raise ValueError("Nieznana karta.")
            if not isinstance(u.get("uid"), str) or u["uid"] in seen: raise ValueError("Powtórzona instancja.")
            seen.add(u["uid"])
            if u.get("owner") != p or type(u.get("buff")) is not int or not -4 <= u["buff"] <= 4: raise ValueError("Niepoprawny stan karty.")
            for key in ["lane", "played", "protected", "silenced"]:
                if key not in u: raise ValueError("Niepełny stan karty.")
            if type(u["protected"]) is not bool or type(u["silenced"]) is not bool or type(u["played"]) is not int or not 1 <= u["played"] <= 7: raise ValueError("Niepoprawny status karty.")
            if u["lane"] not in [-1,0,1,2]: raise ValueError("Niepoprawna pozycja.")
            if not u["uid"].startswith("u") or not u["uid"][1:].isdigit() or int(u["uid"][1:]) > s["serial"]: raise ValueError("Niepoprawny identyfikator.")
    for key in ["flags", "log", "serial", "winner", "finished", "tutorial", "choices", "actions", "seed"]:
        if key not in s: raise ValueError("Niepełny zapis meczu.")


def validate_profile(p):
    if not isinstance(p, dict): raise ValueError("Niepoprawny profil.")
    for key in new_profile():
        if key not in p: raise ValueError("Niepełny profil.")
    if not isinstance(p["name"], str) or len(p["name"]) > 60: raise ValueError("Niepoprawna nazwa.")
    if not isinstance(p["updated"],str) or p["mode"] not in ["story","free"]: raise ValueError("Niepoprawne metadane profilu.")
    for key in ["tutorialDone","hard"]:
        if type(p[key]) is not bool: raise ValueError("Niepoprawny tryb profilu.")
    for key,limit in [("offer",24),("deck",18)]:
        if not isinstance(p[key],list) or len(p[key])>limit or any(not isinstance(c,str) or c not in CARDS or CARDS[c]["kind"]=="token" for c in p[key]) or any(n>2 for n in Counter(p[key]).values()): raise ValueError("Niepoprawna talia profilu.")
    if not isinstance(p["plan"],list) or len(p["plan"])>9 or any(not isinstance(a,dict) for a in p["plan"]): raise ValueError("Niepoprawny plan.")
    for key in ["completed", "hardCompleted"]:
        if not isinstance(p[key], list) or any(type(i) is not int or not 1 <= i <= 20 for i in p[key]): raise ValueError("Niepoprawny postęp.")
    if not isinstance(p["unlocked"], list) or any(c not in CARDS or CARDS[c]["kind"] == "token" for c in p["unlocked"]): raise ValueError("Niepoprawna kolekcja.")
    if not isinstance(p["presets"], list) or len(p["presets"]) > 8: raise ValueError("Zbyt wiele talii.")
    for preset in p["presets"]:
        if not isinstance(preset, dict) or not isinstance(preset.get("name"), str) or validate_deck(preset.get("cards"), p["unlocked"], require_opening=False): raise ValueError("Niepoprawny preset.")
    if p["match"]:
        validate_match(p["match"])
        from .engine import Match
        Match.restore(p["match"]).project(0, p["plan"])


def validate_reading(r):
    if not isinstance(r, dict) or r.get("count") not in POSITIONS: raise ValueError("Niepoprawny rozkład.")
    ids = r.get("cards", [])
    if len(ids) != r["count"] or len(set(ids)) != len(ids) or any(c not in FORTUNES for c in ids): raise ValueError("Niepoprawne karty wróżby.")
    for key, limit in [("id", 80), ("question", 500), ("note", 5000), ("summary", 5000), ("created", 80)]:
        if not isinstance(r.get(key), str) or len(r[key]) > limit: raise ValueError("Niepoprawny tekst wróżby.")
    if r.get("positions") != POSITIONS[r["count"]]: raise ValueError("Niepoprawna kolejność pozycji.")
    if not isinstance(r.get("interpretations"), list) or len(r["interpretations"]) != r["count"] or any(not isinstance(x, str) or len(x) > 5000 for x in r["interpretations"]): raise ValueError("Niepoprawna interpretacja.")
    if not isinstance(r.get("revealed"), list) or len(set(r["revealed"])) != len(r["revealed"]) or any(type(i) is not int or not 0 <= i < r["count"] for i in r["revealed"]): raise ValueError("Niepoprawny stan odsłaniania.")


def make_reading(question, count, cut=26):
    if count not in POSITIONS or not isinstance(question, str) or len(question) > 500: raise ValueError("Pytanie może mieć do 500 znaków; rozkład 1, 3 lub 5 kart.")
    deck = list(FORTUNES)
    random.SystemRandom().shuffle(deck)
    cut = max(1, min(51, cut))
    deck = deck[cut:] + deck[:cut]
    ids = deck[:count]
    return dict(id=str(uuid.uuid4()), created=stamp(), question=question, count=count, cards=ids,
                revealed=[], positions=POSITIONS[count], interpretations=[INTRO[pos]+FORTUNES[c] for pos, c in zip(POSITIONS[count], ids)],
                interpretationVersion="pl-v1", note="", summary="Karty dały wskazówki. Resztę dopiszesz samodzielnie - czat i tak będzie miał własną teorię.")


class Storage:
    def __init__(self, directory=None):
        self.root = Path(directory) if directory else data_directory()
        self.warnings = []
        self.data = self.read("campaign.json", dict(schema=SCHEMA, active=0, slots=[None]*3))
        self.tarot = self.read("readings.json", dict(schema=SCHEMA, readings=[]))
        self.settings = self.read("settings.json", dict(schema=SCHEMA, reduced=False, sound=True, volume=0.4, music=True, musicVolume=0.35, fullscreen=False,
                                                         veteran=False, autoReadings=True, contrast=False))
        # Existing users keep settings.json; additional music controls use defaults.
        self.settings.setdefault("music", True)
        self.settings.setdefault("musicVolume", 0.35)

    def check(self, name, value):
        if not isinstance(value, dict) or value.get("schema") != SCHEMA: raise ValueError("Nieobsługiwana wersja zapisu.")
        if name == "campaign.json":
            if type(value.get("active")) is not int or not 0 <= value["active"] < 3 or not isinstance(value.get("slots"), list) or len(value["slots"]) != 3: raise ValueError("Niepoprawne sloty.")
            for p in value["slots"]:
                if p is not None: validate_profile(p)
        if name == "readings.json":
            if not isinstance(value.get("readings"), list) or len(value["readings"]) > 10000: raise ValueError("Niepoprawna historia.")
            for r in value["readings"]: validate_reading(r)
        if name == "settings.json":
            for key in ["reduced", "sound", "fullscreen", "veteran", "autoReadings", "contrast"]:
                if type(value.get(key)) is not bool: raise ValueError("Niepoprawne ustawienia.")
            if not isinstance(value.get("volume"), (int, float)) or not 0 <= value["volume"] <= 1: raise ValueError("Niepoprawna głośność.")
            # Optional in older settings files; reject malformed new values.
            if "music" in value and type(value["music"]) is not bool: raise ValueError("Niepoprawne ustawienie muzyki.")
            if "musicVolume" in value and (type(value["musicVolume"]) not in (int, float) or not 0 <= value["musicVolume"] <= 1): raise ValueError("Niepoprawna głośność muzyki.")

    def read(self, name, fallback):
        path = self.root / name
        if not path.exists(): return fallback
        for candidate in [path, path.with_suffix(".json.bak")]:
            try:
                if candidate.stat().st_size > 20_000_000: raise ValueError("Zapis przekracza 20 MB.")
                data = json.loads(candidate.read_text(encoding="utf-8"))
                self.check(name, data)
                if candidate != path: self.warnings.append(f"Odzyskano {name} z kopii zapasowej.")
                return data
            except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
                self.warnings.append(f"Nie odczytano {candidate.name}: {exc}")
        # Preserve a corrupt original before a subsequent save.
        try: shutil.copy2(path, path.with_suffix(f".corrupt-{uuid.uuid4().hex[:8]}.json"))
        except OSError: pass
        return fallback

    def write(self, name, value):
        self.check(name, value)
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / name
        temp = self.root / (name + ".tmp")
        with temp.open("w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            try:
                previous = json.loads(path.read_text(encoding="utf-8"))
                self.check(name, previous)
            except (ValueError, KeyError, TypeError, IndexError):
                shutil.copy2(path, path.with_suffix(f".corrupt-{uuid.uuid4().hex[:8]}.json"))
            else:
                shutil.copy2(path, path.with_suffix(".json.bak"))
        os.replace(temp, path)

    def campaign(self):
        self.write("campaign.json", self.data)

    def readings(self):
        self.write("readings.json", self.tarot)

    @property
    def profile(self):
        return self.data["slots"][self.data["active"]]

    def reward(self, mission, hard=False):
        p = self.profile
        key = "hardCompleted" if hard else "completed"
        if mission not in p[key]: p[key].append(mission)
        if not hard:
            p["unlocked"] = sorted(set(p["unlocked"] + ENCOUNTERS[mission-1]["unlocks"]))
            if mission == 1: p["tutorialDone"] = True
        p["updated"] = stamp()

    def import_file(self, path, kind):
        source = Path(path)
        if source.stat().st_size > 20_000_000: raise ValueError("Plik jest większy niż 20 MB.")
        value = json.loads(source.read_text(encoding="utf-8"))
        if kind == "readings":
            self.check("readings.json", value)
            merged = {r["id"]: r for r in self.tarot["readings"]}
            for r in value["readings"]: merged.setdefault(r["id"], r)
            result = dict(schema=SCHEMA, readings=list(merged.values()))
            self.write("readings.json", result)
            self.tarot = result
        else:
            self.check("campaign.json", value)
            self.write("campaign.json", value)
            self.data = value
