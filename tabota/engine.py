"""Deterministic, renderer-independent rules. All randomness is local to a seed.

Plans are validated on a private projection. Projected draws never reveal the
deck, nor can a card drawn during resolution be inserted into an already sealed
plan. AI receives a redacted snapshot, not the player's hidden hand or draw order.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations
import math
import random

from .content import CARDS, ENCOUNTERS, LANES, validate_deck


class IllegalMove(ValueError):
    pass


def definition(unit):
    return CARDS[unit["card"]]


def campaign_difficulty(mission, hard=False, selected="normal", free=False):
    if hard: return "hard"
    if free or selected != "normal": return selected
    return ("beginner", "casual", "easy", "normal")[(mission - 1) // 5]


class Match:
    def __init__(self, mission=1, hard=False, seed=1, decks=None, tutorial=False):
        encounter = ENCOUNTERS[mission-1]
        decks = decks or [encounter["storyDeck"], encounter["enemyDeck"]]
        for deck in decks:
            if validate_deck(deck):
                raise ValueError(validate_deck(deck))
        self.s = dict(version=1, mission=mission, hard=hard, seed=seed, turn=1,
            maxTurns=7 if mission == 16 else 6, energy=[1, 1],
            initialDecks=deepcopy(decks), deck=deepcopy(decks), hand=[[], []], discard=[[], []], board=[[[], [], []], [[], [], []]],
            points=[[0, 0, 0], [0, 0, 0]], hymn=[[False]*3, [False]*3], nextBuff=[[0]*3, [0]*3],
            flags={}, log=[], serial=0, winner=None, finished=False, mulligan=[False, False],
            tutorial=tutorial, choices=[], actions=[], rulesVersion="1.0.0")
        rng = random.Random(seed)
        for d in self.s["deck"]:
            rng.shuffle(d)
            if not tutorial:
                self._ensure_opening_unit(d, rng)
        if tutorial:
            player_order = ["06", "04", "10", "41", "01", "E01", "31", "10", "04", "02", "43"]
            enemy_order = ["31", "02", "11", "04", "04", "10", "31", "01"]
            self.s["deck"][0] = self._ordered(decks[0], player_order)
            # Tutorial explicitly lends a legal demonstrator deck, two copies max.
            enemy_deck = ["31", "02", "11", "04", "04", "10", "31", "01", "06", "06", "43", "43", "10", "41", "41", "E01", "E03", "E07"]
            self.s["deck"][1] = self._ordered(enemy_deck, enemy_order)
        for p in range(2):
            self.draw(p, 5)
        self.frames = []
        self.preview = False

    @staticmethod
    def _opening_unit(cid):
        return CARDS[cid]["kind"] == "unit" and CARDS[cid]["cost"] <= 1

    @classmethod
    def _ensure_opening_unit(cls, deck, rng):
        """Swap one playable unit into a five-card opening hand, preserving counts.

        Unlike a full reshuffle/rejection loop this always terminates, and the
        chosen seed determines the repaired order for replay/save consistency.
        """
        if any(cls._opening_unit(cid) for cid in deck[:5]):
            return
        eligible = [i for i in range(5, len(deck)) if cls._opening_unit(deck[i])]
        if not eligible:
            raise ValueError("Brak jednostki za ⚡ 1 w talii startowej.")
        i = rng.choice(eligible)
        j = rng.randrange(5)
        deck[i], deck[j] = deck[j], deck[i]

    def tutorial_move(self, p=0):
        """Mandatory single-card lesson for turns 1-3; None in free play."""
        if p != 0 or not self.s["tutorial"] or self.s["turn"] > 3:
            return None
        cid, lane = [("06", 0), ("04", 1), ("10", 2)][self.s["turn"]-1]
        unit = next((u for u in self.s["hand"][0] if u["card"] == cid), None)
        # A planned lesson card was already consumed by a projection.
        return {"uid": unit["uid"] if unit else "", "card": cid, "lane": lane}

    @staticmethod
    def _ordered(deck, order):
        rest = deck[:]
        for c in order:
            rest.remove(c)
        return order + rest

    @classmethod
    def restore(cls, state):
        m = cls.__new__(cls)
        m.s = deepcopy(state)
        m.frames = []
        m.preview = False
        return m

    def clone(self, preview=True):
        m = self.restore(self.s)
        m.preview = preview
        return m

    def log(self, text):
        self.s["log"].append(f"T{self.s['turn']} · {text}")

    def once(self, key):
        if self.s["flags"].get(key):
            return False
        self.s["flags"][key] = True
        return True

    def new_unit(self, cid, player, lane=-1):
        self.s["serial"] += 1
        return dict(uid=f"u{self.s['serial']}", card=cid, owner=player, lane=lane,
                    buff=0, protected=False, silenced=False, played=self.s["turn"])

    def draw(self, p, count=1):
        if getattr(self, "preview", False):
            return
        for _ in range(count):
            if not self.s["deck"][p]:
                break
            cid = self.s["deck"][p].pop(0)
            u = self.new_unit(cid, p)
            if len(self.s["hand"][p]) < 10:
                self.s["hand"][p].append(u)
            else:
                self.s["discard"][p].append(u)
                self.log(f"RĘKA PEŁNA: {CARDS[cid]['name']} trafia na stos.")

    def mulligan(self, p, ids):
        if self.s["turn"] != 1 or self.s["mulligan"][p] or self.s["actions"]:
            raise IllegalMove("Wymiana jest dostępna tylko raz przed pierwszą turą.")
        if len(ids) > 2 or len(set(ids)) != len(ids) or any(i not in [u["uid"] for u in self.s["hand"][p]] for i in ids):
            raise IllegalMove("Wybierz od 0 do 2 kart z ręki.")
        if self.s["tutorial"] and ids:
            raise IllegalMove("Tutorial ma oznaczone, demonstracyjne rozdanie.")
        for uid in ids:
            u = next(u for u in self.s["hand"][p] if u["uid"] == uid)
            self.s["hand"][p].remove(u)
            self.s["deck"][p].append(u["card"])
        if ids:
            rng = random.Random(self.s["seed"] + 491*p + 17)
            rng.shuffle(self.s["deck"][p])
            # A mulligan must not strand anyone on turn 1 after replacing
            # their only inexpensive card. Reinsert a playable unit if needed.
            if not any(self._opening_unit(u["card"]) for u in self.s["hand"][p]):
                next_unit = next((i for i, cid in enumerate(self.s["deck"][p]) if self._opening_unit(cid)), None)
                if next_unit is not None and next_unit >= len(ids):
                    target = rng.randrange(len(ids))
                    self.s["deck"][p][target], self.s["deck"][p][next_unit] = (self.s["deck"][p][next_unit], self.s["deck"][p][target])
            self.draw(p, len(ids))
        self.s["mulligan"][p] = True

    def units(self, p, lane=None):
        return self.s["board"][p][lane] if lane is not None else [u for row in self.s["board"][p] for u in row]

    def find(self, uid):
        return next((u for p in range(2) for u in self.units(p) if u["uid"] == uid), None)

    def capacity(self, lane):
        return 5 if self.s["mission"] == 5 and self.s["hard"] and lane == 1 else 4

    def room(self, p, lane):
        return 0 <= lane < 3 and len(self.units(p, lane)) < self.capacity(lane)

    def aura(self, u):
        if u["silenced"]:
            return 0
        p, l, cid = u["owner"], u["lane"], u["card"]
        others = [v for v in self.units(p, l) if v["uid"] != u["uid"]]
        if cid == "04": return 2 if not others else 0
        if cid == "06": return int(any(definition(v)["tag"] == "Widz" for v in others))
        if cid == "08": return 2 if any(definition(v)["tag"] == "Moderacja" for v in others) else 0
        if cid == "13": return 2 if self.s["hymn"][p][l] or any(v["card"] == "39" for v in others) else 0
        if cid == "20": return min(2, sum(definition(v)["tag"] == "Horror" for v in others))
        if cid == "30": return 2 if not any("a" in definition(v)["nameKey"] for v in others) else 0
        if cid == "31": return int(l == 2)
        return 0

    def power(self, u):
        return max(0, definition(u)["power"] + u["buff"] + min(4, self.aura(u)))

    def add_points(self, p, lane, amount, source):
        self.s["points"][p][lane] += amount
        ledger = self.s["flags"].setdefault("pointSources", {})
        key = f"{p}:{lane}"
        ledger.setdefault(key, []).append(f"{source}: {amount:+d}")
        self.log(f"{'TABO' if p == 0 else 'RYWAL'} · {LANES[lane]} · {source}: {amount:+d} stałych punktów.")

    def scores(self):
        return [[self.s["points"][p][l] + sum(self.power(u) for u in self.units(p, l)) for l in range(3)] for p in range(2)]

    def wins(self, p):
        scores = self.scores()
        return sum(a > b for a, b in zip(scores[p], scores[1-p]))

    def hostile(self, u):
        if u["protected"]:
            u["protected"] = False
            self.log(f"Ochrona blokuje efekt: {definition(u)['name']}.")
            return False
        return True

    def buff(self, u, value, hostile=False):
        if u is None or (hostile and not self.hostile(u)):
            return
        before = u["buff"]
        u["buff"] = max(-4, min(4, before + value))
        if u["buff"] != before:
            self.log(f"{definition(u)['name']}: {u['buff']-before:+} Mocy.")

    def silence(self, u):
        if u and self.hostile(u):
            u["silenced"] = True
            self.log(f"WYCISZENIE · {definition(u)['name']} (bazowa Moc pozostaje).")

    def remove(self, u):
        if u and self.hostile(u):
            self.units(u["owner"], u["lane"]).remove(u)
            self.s["discard"][u["owner"]].append(u)
            self.log(f"USUNIĘCIE · {definition(u)['name']}.")

    def move(self, u, dest, hostile=False):
        if not u or dest == u["lane"] or not self.room(u["owner"], dest):
            return False
        if hostile and not self.hostile(u):
            return False
        self.units(u["owner"], u["lane"]).remove(u)
        u["lane"] = dest
        self.units(u["owner"], dest).append(u)
        self.log(f"{definition(u)['name']} → {LANES[dest]}.")
        if self.s["mission"] == 11:
            p = u["owner"]
            moved = self.s["flags"].setdefault(f"moved:{p}", [])
            if u["uid"] not in moved and len(moved) < (2 if self.s["hard"] else 1):
                moved.append(u["uid"])
                self.buff(u, 1 if self.s["hard"] else 2)
        return True

    def token(self, p, lane, cid):
        if self.room(p, lane):
            u = self.new_unit(cid, p, lane)
            self.units(p, lane).append(u)
            self.log(f"Żeton {definition(u)['name']} → {LANES[lane]}.")

    def candidates(self, p, uid, lane):
        """All explicit legal targeting choices for one placement, incl. optional skip."""
        if self.s["finished"] or lane not in range(3): return []
        hand = next((u for u in self.s["hand"][p] if u["uid"] == uid), None)
        if hand is None: return []
        cid = hand["card"]
        lesson = self.tutorial_move(p)
        if lesson and (uid != lesson["uid"] or lane != lesson["lane"]):
            return []
        d = CARDS[cid]
        event = d["kind"] == "event"
        if d["cost"] > self.s["energy"][p]: return []
        if event and (self.s["flags"].get(f"ink:{p}:{self.s['turn']}") or (self.s["mission"] == 16 and self.s["hard"] and self.s["turn"] == 7)):
            return []
        if not event and not self.room(p, lane): return []
        base = dict(uid=uid, lane=lane, targets=[], dest=-1)
        own = self.units(p)
        row = self.units(p, lane)[:]
        enemy = self.units(1-p)
        erow = self.units(1-p, lane)
        self_target = dict(hand, lane=lane)
        targets = None
        number = 1
        movement = False
        adjacent = False
        optional = False
        if cid in ["02", "29", "36"]:
            targets, movement, adjacent, optional = own, True, cid != "36", True
        elif cid == "25":
            targets, movement, adjacent, optional = [self_target], True, True, True
        elif cid in ["03", "39"]: targets, number = row, 2
        elif cid == "05": targets = row + [self_target] if erow else []
        elif cid in ["14", "24", "37"]: targets = row
        elif cid == "18": targets = row + [self_target]
        elif cid == "26": targets = [u for u in row if u["buff"] < 0]
        elif cid in ["07", "12", "40", "44", "48"]: targets = erow
        elif cid == "32": targets = [u for u in erow if self.power(u) <= 2]
        elif cid == "38": targets, number = erow, 2
        elif cid == "49": targets = [u for u in erow if definition(u)["tag"] == "Moderacja"]
        elif cid in ["19", "46"]:
            targets, number = [u for u in own if definition(u)["tag"] == "Hymn"], 2
            if cid == "19": targets = targets + [self_target]
        elif cid in ["E01", "E04", "E05", "E13"]: targets = row
        elif cid == "E06": targets = [u for u in row if definition(u)["tag"] == "Hymn"]
        elif cid in ["E03", "E10"]: targets, movement, adjacent = row, True, cid == "E03"
        elif cid == "E07": targets = erow
        elif cid == "E08": targets = [u for u in erow if definition(u)["trigger"] in ("aura", "final") and not u["silenced"]]
        elif cid == "E09":
            if lane != 2: return []
            targets, number = row, 2
        elif cid == "E11":
            if not any(definition(u)["tag"] == "Hymn" for u in row): return []
        elif cid == "E12":
            tokens = [u for u in erow if definition(u)["kind"] == "token" and self.power(u) <= 2]
            targets = tokens or erow
        elif cid == "E16": targets, number = [u for u in own if definition(u)["tag"] == "Widz"], 2
        elif cid == "E17":
            targets, movement, adjacent = [u for u in erow if definition(u)["power"] <= 4], True, True
        elif cid == "E18": targets = [u for u in row if definition(u)["tag"] == "Horror"]
        elif cid == "E19": targets = [u for u in row if definition(u)["tag"] == "Retro"]
        elif cid == "E20": targets, number = erow, 2
        elif cid == "E21": targets = [u for u in erow if definition(u)["power"] <= 3]
        elif cid == "E22" and lane != 1: return []
        elif cid == "E23":
            technicians = [u for u in own if definition(u)["tag"] == "Technika"]
            targets = [u for u in row if u in technicians] if technicians else row
        elif cid == "E24":
            lanes = [l for l in range(3) if self.units(p, l)]
            return [dict(base, zones=list(ls)) for ls in combinations(lanes, min(2, len(lanes))) if lane in ls] if lanes else []
        if targets is None:
            return [base]
        result = []
        if movement:
            for u in targets:
                for dest in range(3):
                    if dest != u["lane"] and self.room(u["owner"], dest) and (not adjacent or abs(dest-u["lane"]) == 1):
                        result.append(dict(base, targets=[u["uid"]], dest=dest))
        else:
            sizes = range(1, min(number, len(targets))+1) if number > 1 and not event else [min(number, len(targets))]
            for size in sizes:
                for group in combinations(targets, size):
                    if group:
                        result.append(dict(base, targets=[u["uid"] for u in group]))
            if number > 1 and not event:
                result.append(base)
        if optional or (not result and not event): result.append(base)
        return result

    def ritual_options(self, p):
        if self.s["turn"] != 4 or self.s["mission"] < 4 or self.s["flags"].get(f"ritual:{p}") or self.s["finished"]:
            return []
        options = [dict(special="hymn", lane=l, targets=[]) for l in range(3)]
        if not (self.s["mission"] == 17 and self.s["hard"]):
            options += [dict(special="ban", lane=u["lane"], targets=[u["uid"]]) for u in self.units(1-p)
                        if definition(u)["trigger"] in ("aura", "final") and not u["silenced"]]
        options.append(dict(special="clip", lane=0, targets=[]))
        return options

    def flight_options(self, p):
        if self.s["mission"] != 12 or self.s["turn"] != 4 or self.s["flags"].get(f"flight:{p}"): return []
        return [dict(special="flight", lane=u["lane"], dest=l, targets=[u["uid"]]) for u in self.units(p) for l in range(3) if l != u["lane"] and self.room(p, l)]

    def action_label(self, action):
        if "special" in action:
            name = {"hymn": "HYMN", "ban": "WSZYSCY DO BANA", "clip": "POKAŻ KLIPA", "flight": "DARMOWY LOT"}[action["special"]]
        else:
            u = next((u for hand in self.s["hand"] for u in hand if u["uid"] == action["uid"]), None)
            name = definition(u)["name"] if u else "Karta"
        names = []
        for uid in action.get("targets", []):
            u = self.find(uid) or next((v for h in self.s["hand"] for v in h if v["uid"] == uid), None)
            if u: names.append(definition(u)['name'])
        return name + " → " + LANES[action["lane"]] + (" · cel: " + ", ".join(names) if names else "") + (" → " + LANES[action["dest"]] if action.get("dest", -1) >= 0 else "")

    def project(self, p, plan):
        projected = self.clone()
        for a in plan:
            options = projected.ritual_options(p) + projected.flight_options(p) if "special" in a else projected.candidates(p, a["uid"], a["lane"])
            if a not in options:
                raise IllegalMove("Ruch nie jest już legalny. Cofnij plan i wybierz inny cel.")
            projected.apply(p, a)
        return projected

    def apply(self, p, a):
        """Resolve a sealed action. A lost target fizzles; blocked slots refund."""
        lane = a["lane"]
        if "special" in a:
            kind = a["special"]
            if kind == "flight":
                self.s["flags"][f"flight:{p}"] = True
                self.move(self.find(a["targets"][0]), a["dest"])
                return
            if not self.once(f"ritual:{p}"): return
            self.log(f"{'TABO' if p == 0 else 'RYWAL'} · RYTUAŁ {kind.upper()}.")
            if kind == "hymn":
                self.add_points(p, lane, 5 if self.s["mission"] == 13 else 3, "Rytuał Hymn")
                self.s["hymn"][p][lane] = True
            elif kind == "ban": self.silence(self.find(a["targets"][0]))
            elif kind == "clip": self.draw(p, 3 if self.s["mission"] == 13 and self.s["hard"] else 2)
            return
        u = next((u for u in self.s["hand"][p] if u["uid"] == a["uid"]), None)
        if not u: return
        cid = u["card"]
        d = CARDS[cid]
        event = d["kind"] == "event"
        if d["cost"] > self.s["energy"][p] or (not event and not self.room(p, lane)):
            self.log(f"{d['name']}: brak miejsca lub Energii. Karta zostaje w ręce; koszt zwrócony.")
            return
        if event and self.s["flags"].get(f"ink:{p}:{self.s['turn']}"):
            return
        before = self.scores()
        empty_back = not self.units(p, 2)
        retro_hand = len({v["card"] for v in self.s["hand"][p] if definition(v)["tag"] == "Retro"})
        self.s["energy"][p] -= d["cost"]
        self.s["hand"][p].remove(u)
        u.update(lane=lane, played=self.s["turn"])
        self.log(f"{'TABO' if p == 0 else 'RYWAL'} · {d['name']} → {LANES[lane]} (K{d['cost']}).")
        if event:
            self.s["discard"][p].append(u)
            self.s["flags"][f"event:{p}:{lane}:{self.s['turn']}"] = True
        else:
            self.units(p, lane).append(u)
            if self.s["nextBuff"][p][lane] and self.s["turn"] <= 6:
                self.buff(u, self.s["nextBuff"][p][lane])
                self.s["nextBuff"][p][lane] = 0
            self.on_rule_play(u, retro_hand)
        if self.s["mission"] == 20 and d["trigger"] == "entry" and self.s["turn"] in [2, 4, 6]:
            glitched = ([2, 0, 1] if self.s["hard"] else [0, 1, 2])[self.s["turn"]//2-1]
            if lane == glitched and self.once(f"glitch:{p}:{self.s['turn']}"):
                self.log(f"NIC TU KURŁA NIE DZIAŁA!: Wejście {d['name']} wyłączone.")
                return
        targets = [self.find(uid) for uid in a.get("targets", [])]
        # Explicit target must still satisfy its original targeting predicate.
        targets = [t for t in targets if t is not None]
        same_lane_ids = {"03", "05", "07", "12", "14", "18", "24", "26", "32", "37", "38", "39", "40", "44", "48", "49"}
        if cid in same_lane_ids or (event and cid not in ["E16", "E24"]):
            targets = [t for t in targets if t["lane"] == lane]
        t = targets[0] if targets else None
        others = [v for v in self.units(p, lane) if v is not u]
        own = self.units(p)
        erow = self.units(1-p, lane)
        if cid in ["02", "29", "36", "E03", "E10"]:
            self.move(t, a.get("dest", -1))
        elif cid == "25":
            if a.get("dest", -1) >= 0 and self.move(u, a["dest"]): self.buff(u, 2)
        elif cid in ["03", "19", "39", "46", "E09", "E16"]:
            for v in targets[:2]: self.buff(v, 1)
        elif cid == "05":
            if erow: self.buff(t, 2)
        elif cid in ["07", "E08"]: self.silence(t)
        elif cid == "09": self.buff(u, min(3, len(others)))
        elif cid in ["11", "51"]:
            if any(definition(v)["tag"] == d["tag"] for v in others): self.draw(p)
        elif cid in ["12", "40", "44", "48", "E07"]: self.buff(t, -1 if cid == "12" else -2, True)
        elif cid in ["14", "24", "37", "E06"]: self.buff(t, 2)
        elif cid in ["15", "35"]:
            if before[p][lane] < before[1-p][lane]: self.buff(u, 1 if cid == "15" else 2)
        elif cid == "17": self.s["nextBuff"][p][lane] = min(4, self.s["nextBuff"][p][lane]+2)
        elif cid in ["18", "E05"]:
            if t: t["protected"] = True
        elif cid == "21":
            if not others: self.buff(u, 2)
        elif cid == "23":
            if empty_back: self.draw(p)
        elif cid == "26":
            if t and t["buff"] < 0: self.buff(t, min(2, -t["buff"]))
        elif cid in ["28", "34", "50"]:
            for _ in range(2 if cid == "50" else 1): self.token(p, lane, {"28": "T1", "34": "T2", "50": "T3"}[cid])
        elif cid == "32":
            if t and self.power(t) <= 2: self.remove(t)
        elif cid == "33":
            if 4 <= self.s["turn"] <= 6: self.buff(u, 2)
        elif cid in ["38", "E20"]:
            for v in targets[:2]: self.buff(v, -1, True)
        elif cid == "41":
            if self.s["deck"][p]: self.draw(p)
            else: self.buff(u, 1)
        elif cid == "42": self.buff(u, min(2, sum(definition(v)["tag"] == "Widz" for v in others)))
        elif cid == "43":
            if self.s["turn"] <= 2: self.buff(u, 2)
        elif cid == "49":
            if t: self.buff(t, -2, True)
            elif not any(definition(v)["tag"] == "Moderacja" for v in erow): self.buff(u, 1)
        elif cid == "E01": self.buff(t, 2 if lane == 2 else 1)
        elif cid == "E02":
            self.draw(p)
            self.s["flags"][f"ink:{p}:{self.s['turn']}"] = True
        elif cid == "E04": self.buff(t, 2 if t and t["card"] == "30" else 1)
        elif cid == "E11":
            if any(definition(v)["tag"] == "Hymn" for v in self.units(p, lane)): self.add_points(p, lane, 2, definition(u)["name"])
        elif cid == "E12":
            if t and definition(t)["kind"] == "token" and self.power(t) <= 2: self.remove(t)
            elif t: self.buff(t, -1, True)
            elif erow: self.buff(erow[0], -1, True)  # Explicit fallback from card text.
        elif cid in ["E13", "E18"]: self.buff(t, 3)
        elif cid == "E14":
            self.draw(p, 2)
            if not self.preview and self.s["hand"][p]: self.s["choices"].append(dict(owner=p, kind="discard"))
        elif cid == "E15": self.add_points(p, lane, 3 if self.s["turn"] in [5, 6] else 1, definition(u)["name"])
        elif cid == "E17":
            if t and definition(t)["power"] <= 4: self.move(t, a.get("dest", -1), True)
        elif cid == "E19":
            self.buff(t, 2)
            if any(v["card"] == "31" for v in own): self.draw(p)
        elif cid == "E21":
            if t and definition(t)["power"] <= 3: self.remove(t)
        elif cid == "E22":
            self.add_points(p, 1, 2, definition(u)["name"])
            self.draw(p)
        elif cid == "E23": self.buff(t, 2 if t and definition(t)["tag"] == "Technika" else 1)
        elif cid == "E24":
            for l in a.get("zones", []):
                if self.units(p, l): self.add_points(p, l, 2, definition(u)["name"])

    def on_rule_play(self, u, retro_hand):
        p, l = u["owner"], u["lane"]
        d = definition(u)
        mission, hard, turn = self.s["mission"], self.s["hard"], self.s["turn"]
        matchkey, turnkey = f"rule:{p}", f"rule:{p}:{turn}"
        if mission == 1 and hard and l == 1 and d["tag"] == "Moderacja" and self.once(turnkey): self.buff(u, 1)
        if mission == 2 and d["tag"] == "Retro" and (not hard or l == 2) and self.once(matchkey): self.buff(u, 2)
        if mission == 3 and l == 1:
            if "a" not in d["nameKey"] and self.once(turnkey): self.buff(u, 1)
            if "a" in d["nameKey"]: self.s["flags"][f"lastA:{p}:{turn}"] = u["uid"]
        if mission == 4 and l == 0 and d["tag"] == "Hymn" and self.once(matchkey): self.buff(u, 1)
        if mission == 5 and l == 1 and d["tag"] == "Widz" and self.once(turnkey): self.buff(u, 1)
        if mission == 7 and l == 2 and turn <= 3 and self.once(matchkey): self.buff(u, 2 if hard and turn == 1 else 1)
        if mission == 8 and l == 0 and (d["tag"] == "Chaos" if hard else d["cost"] == 3) and self.once(turnkey): self.buff(u, 1)
        if mission == 10 and d["tag"] == "Horror" and (l == 2 and turn == 6 if hard else l == 0 and turn in [5, 6]) and self.once(matchkey): self.buff(u, 2)
        if mission == 14 and d["tag"] == "Retro" and (retro_hand >= 2 if hard else l == 2) and self.once(matchkey): u["protected"] = True
        if mission == 17 and d["tag"] == "Moderacja" and l == 1 and self.once(matchkey):
            u["protected"] = True
            self.buff(u, 1)

    def end_rule(self):
        mission, hard, turn = self.s["mission"], self.s["hard"], self.s["turn"]
        for p in range(2):
            if mission == 3 and hard:
                self.buff(self.find(self.s["flags"].get(f"lastA:{p}:{turn}")), -1)
            if mission == 6 and turn in ([2, 3, 5] if hard else [3, 5]):
                lane = min(range(3), key=lambda l: len(self.units(p, l)))
                if self.units(p, lane): self.add_points(p, lane, 1 if hard else 2, "Reguła wyzwania 06")
            if mission == 9 and turn == 3:
                lane = min([1, 0, 2], key=lambda l: self.scores()[p][l]) if hard else 1
                self.token(p, lane, "T3")
            if mission == 15 and turn in ([3, 5] if hard else [4]):
                for l in range(3):
                    if len(self.units(p, l)) >= 2:
                        u = min(self.units(p, l), key=lambda v: (self.power(v), int(v["uid"][1:])))
                        self.buff(u, -1)
        if mission == 18 and turn in ([2, 4, 6] if hard else [2, 4]):
            scores = self.scores()
            if scores[0][2] != scores[1][2]:
                p = 0 if scores[0][2] > scores[1][2] else 1
                self.add_points(p, 2, 1, "Audyt")
                self.log(f"AUDYT: +1 na Zapleczu dla {'TABO' if p == 0 else 'RYWALA'}.")

    def finals(self):
        pre_wins = [self.wins(p) for p in range(2)]
        first = 0 if self.s["turn"] % 2 else 1
        for p in [first, 1-first]:
            for l in range(3):
                for u in sorted(self.units(p, l)[:], key=lambda v: int(v["uid"][1:])):
                    if u["silenced"]: continue
                    cid = u["card"]
                    if cid == "01":
                        for lane in range(3):
                            if self.units(p, lane): self.add_points(p, lane, 1, "Prorok Tabo - Finał")
                        self.log("Prorok Tabo · FINAŁ: +1 w każdej strefie z jednostką.")
                    elif cid == "16" and l == 2: self.buff(u, 1)
                    elif cid == "22" and u["played"] in [5, 6]: self.buff(u, 2)
                    elif cid == "27" and pre_wins[p] >= 2: self.buff(u, 2)
                    elif cid == "45" and not self.s["flags"].get(f"event:{1-p}:{l}:6"): self.buff(u, 1)
                    elif cid == "47": self.buff(u, min(3, len(self.units(1-p, 1))))
                    elif cid == "52" and any(v is not u and definition(v)["tag"] == "Widz" for v in self.units(p)): self.buff(u, 1)
        if self.s["mission"] == 19:
            for p in range(2):
                for l in range(3):
                    n = len(self.units(p, l))
                    self.add_points(p, l, -((3 if n >= 3 else 1 if n == 2 else 0) if self.s["hard"] else (2 if n >= 3 else 0)), "Reguła wyzwania 19")
        scores = self.scores()
        ranking = [(self.wins(p), sum(scores[p])) for p in range(2)]
        self.s["winner"] = -1 if ranking[0] == ranking[1] else 0 if ranking[0] > ranking[1] else 1
        self.s["finished"] = True
        self.log("KONIEC · " + ("REMIS" if self.s["winner"] == -1 else "WYGRYWA " + ("TABO" if self.s["winner"] == 0 else "RYWAL")))

    def commit(self, plans):
        if self.s["finished"] or self.s["choices"]:
            raise IllegalMove("Najpierw zakończ bieżący wybór.")
        lesson = self.tutorial_move(0)
        if lesson and (len(plans[0]) != 1 or plans[0][0].get("uid") != lesson["uid"] or plans[0][0].get("lane") != lesson["lane"]):
            raise IllegalMove("W tej części nauki zagraj wskazaną kartę do wskazanej strefy.")
        for p in range(2): self.project(p, plans[p])
        self.frames = []
        self.s["actions"].append(deepcopy(plans))
        first = 0 if self.s["turn"] % 2 else 1
        for special in ["flight", "ritual"]:
            for p in [first, 1-first]:
                for a in plans[p]:
                    if "special" in a and ((a["special"] == "flight") == (special == "flight")):
                        self.apply(p, a)
                        self.frames.append(deepcopy(self.s))
        normal = [[a for a in plan if "special" not in a] for plan in plans]
        for i in range(max(map(len, normal), default=0)):
            for p in [first, 1-first]:
                if i < len(normal[p]):
                    self.apply(p, normal[p][i])
                    self.frames.append(deepcopy(self.s))
        self.end_rule()
        if self.s["choices"]:
            self.s["awaitingAdvance"] = True
        else:
            self.complete_turn()
        self.frames.append(deepcopy(self.s))
        return self.frames

    def complete_turn(self):
        self.s["awaitingAdvance"] = False
        if self.s["turn"] == self.s["maxTurns"]:
            self.finals()
        else:
            self.s["turn"] += 1
            self.s["energy"] = [self.s["turn"]]*2
            for p in range(2): self.draw(p)

    def discard_choice(self, uid):
        if not self.s["choices"]: raise IllegalMove("Nie ma karty do odrzucenia.")
        p = self.s["choices"][0]["owner"]
        u = next((u for u in self.s["hand"][p] if u["uid"] == uid), None)
        if u is None: raise IllegalMove("Wybierz kartę z ręki.")
        self.s["hand"][p].remove(u)
        self.s["discard"][p].append(u)
        self.s["choices"].pop(0)
        self.log(f"Sprawdź Płyty · odrzucono {definition(u)['name']}.")
        if not self.s["choices"] and self.s.get("awaitingAdvance"):
            self.complete_turn()

    def public_view(self, p):
        m = self.clone()
        m.s["hand"][1-p] = []
        m.s["deck"] = [["?"] * len(d) for d in self.s["deck"]]
        # Past plans are public; current plans never enter this state.
        return m


def evaluate(m, p):
    scores = m.scores()
    t = m.s["turn"]
    result = 0.0
    for l in range(3):
        diff = scores[p][l] - scores[1-p][l]
        result += 12 * math.tanh(diff / (3 if t >= 5 else 6)) + .22 * max(-15, min(15, diff))
        if m.s["mission"] == 19:
            result -= max(0, len(m.units(p, l)) - 2) * 1.2
    result += .2 * sum(scores[p])
    result += .25 * sum(u["protected"] for u in m.units(p))
    result += .2 * sum(CARDS[u["card"]]["trigger"] == "final" and not u["silenced"] for u in m.units(p))
    return result


def ai_plan(match, p=1, difficulty="normal"):
    """Beam search over public state and own hand; no access to either draw order."""
    if match.s["tutorial"] and p == 1:
        script = [[("31", 0)], [("02", 1)], [("11", 2)], [("04", 0), ("04", 1)], [("10", 0), ("31", 1)], [("01", 0)]]
        m, plan = match.clone(), []
        for cid, lane in script[match.s["turn"]-1]:
            u = next(u for u in m.s["hand"][p] if u["card"] == cid)
            options = m.candidates(p, u["uid"], lane)
            a = next((a for a in options if not a["targets"]), options[0])
            plan.append(a)
            m.apply(p, a)
        return plan
    m = match.public_view(p)
    base = []
    flight = m.flight_options(p)
    rituals = m.ritual_options(p)
    for options in [flight, rituals]:
        if options:
            scored = []
            for a in options:
                n = m.clone()
                n.apply(p, a)
                score = evaluate(n, p)
                if a.get("special") == "clip": score += 1.4 if len(m.s["hand"][p]) < 3 else 0
                scored.append((score, a))
            a = max(scored, key=lambda x: x[0])[1]
            m.apply(p, a)
            base.append(a)
    width = {"beginner": 1, "casual": 1, "easy": 1, "normal": 2, "hard": 5}.get(difficulty, 2)
    beam = [(evaluate(m, p), m, base)]
    best = beam[0]
    for _ in range(7):
        expanded = []
        for _, state, plan in beam:
            actions = [a for u in state.s["hand"][p] for lane in range(3) for a in state.candidates(p, u["uid"], lane)]
            for a in actions:
                n = state.clone()
                n.apply(p, a)
                score = evaluate(n, p) + .06 * (match.s["turn"]-n.s["energy"][p])
                expanded.append((score, n, plan + [a]))
        if not expanded: break
        expanded.sort(key=lambda x: x[0], reverse=True)
        if difficulty in ("beginner", "casual", "easy"):
            rng = random.Random(match.s["seed"] + match.s["turn"]*37+p)
            beam = [expanded[rng.randrange(min({"beginner": 12, "casual": 6, "easy": 3}[difficulty], len(expanded)))]]
        else:
            beam, seen = [], set()
            for item in expanded:
                signature = tuple(sorted((a.get("uid", a.get("special")), a["lane"], tuple(a.get("targets", [])), a.get("dest", -1)) for a in item[2]))
                if signature not in seen:
                    seen.add(signature)
                    beam.append(item)
                if len(beam) == width: break
        if difficulty in ("beginner", "casual") or beam[0][0] > best[0] or (not best[2] and beam[0][2]): best = beam[0]
    return best[2]



def prepare_turn(match, player_plan, difficulty="normal"):
    """Compute the sealed turn and its animation frames without mutating `match`.

    This function is independent of Qt so tests can prove that work moved to
    a background worker does not alter the game's deterministic rules.
    """
    simulated = match.clone(False)
    enemy = ai_plan(simulated, 1, difficulty)
    frames = simulated.commit([deepcopy(player_plan), enemy])
    while simulated.s["choices"] and simulated.s["choices"][0]["owner"] == 1:
        uid = min(simulated.s["hand"][1], key=lambda u: definition(u)["power"])["uid"]
        simulated.discard_choice(uid)
    frames[-1] = deepcopy(simulated.s)
    return simulated.s, frames


def draft_offer(unlocked, seed):
    rng = random.Random(seed)
    units = [c for c in unlocked if CARDS[c]["kind"] == "unit"]
    events = [c for c in unlocked if CARDS[c]["kind"] == "event"]
    pool = units * 2
    rng.shuffle(pool)
    selected = []
    expensive = [c for c in units if CARDS[c]["cost"] >= 5]
    rng.shuffle(expensive)
    for c in expensive[:3]: selected.append(c); pool.remove(c)
    starter = next((c for c in pool if CARDS[c]["cost"] <= 1), None)
    if starter is not None:
        selected.append(starter)
        pool.remove(starter)
    cheap = [c for c in pool if CARDS[c]["cost"] <= 2]
    for c in cheap[:5 if starter is None else 4]: selected.append(c); pool.remove(c)
    selected += pool[:max(0, 18-len(selected))]
    epool = events * 2
    rng.shuffle(epool)
    selected += epool[:6]
    if len(selected) < 24:
        leftovers = list((Counter(units*2+events*2)-Counter(selected)).elements())
        selected += leftovers[:24-len(selected)]
    rng.shuffle(selected)
    return selected


def auto_deck(offer):
    units = sorted((c for c in offer if CARDS[c]["kind"] == "unit"), key=lambda c: (CARDS[c]["cost"], c))
    events = sorted((c for c in offer if CARDS[c]["kind"] == "event"), key=lambda c: CARDS[c]["cost"])
    # Maintain an affordable opening while keeping finishers and optional events.
    deck = units[:5] + units[-3:]
    remaining = list((Counter(units)-Counter(deck)).elements())
    deck += remaining[:max(0, 15-len(deck))]
    deck += events[:18-len(deck)]
    deck += list((Counter(units)-Counter(deck)).elements())[:18-len(deck)]
    return deck
