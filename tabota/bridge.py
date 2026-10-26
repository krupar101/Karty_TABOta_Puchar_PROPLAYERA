"""Qt adapter: UI commands, sealed plans, persistence and playback snapshots."""
from collections import Counter, deque
from copy import deepcopy
import json
import os
from time import perf_counter
from pathlib import Path
import secrets
import traceback

from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl, QTimer, QRunnable, QThreadPool
from PySide6.QtWidgets import QFileDialog

from .content import ROOT, CARDS, ENCOUNTERS, LANES, ACTS, STARTER, FORTUNES, validate_deck, encounter_rule
from .engine import Match, IllegalMove, ai_plan, prepare_turn, draft_offer, auto_deck, definition
from .storage import Storage, make_reading, new_profile, stamp, SCHEMA


class WorkerSignals(QObject):
    done = Signal(object)
    error = Signal(str)


class Thinker(QRunnable):
    def __init__(self, match, difficulty, player_plan):
        super().__init__()
        self.match, self.difficulty = match.clone(False), difficulty
        self.player_plan = deepcopy(player_plan)
        self.signals = WorkerSignals()

    def run(self):
        # Work on a detached match. Both AI search AND turn resolution / frame
        # preparation run off the Qt GUI thread. Never touch QObjects here.
        try:
            start = perf_counter()
            outcome = prepare_turn(self.match, self.player_plan, self.difficulty)
            self.signals.done.emit((*outcome, (perf_counter() - start) * 1000))
        except Exception:
            traceback.print_exc()
            self.signals.error.emit("Nie udało się rozegrać tury przeciwnika. Możesz ponowić turę.")


class Bridge(QObject):
    changed = Signal()
    boardChanged = Signal()
    spectrumChanged = Signal()
    soundRequested = Signal(str)
    quitRequested = Signal()

    def __init__(self, directory=None):
        super().__init__()
        self.store = Storage(directory)
        self.screen = "menu"
        self.match = None
        self.plan = []
        self.selected = ""
        self.options = []
        self.detail = ""
        self.detail_tarot = False
        self.notice = " · ".join(self.store.warnings)
        self.confirmation = ""
        self.pending = None
        self.mission = 1
        self.hard = False
        self.free = False
        self.difficulty = "normal"
        self.draft = False
        self.offer = []
        self.deck = []
        self.reading = None
        self.busy = False
        self.frames = deque()
        self.display_match = None
        self.mulligan_ids = []
        self.saved_result = False
        self.dialogue = ""
        self.dialogue_seen = set()
        self.collection_query = ""
        self.collection_tag = "Wszystkie"
        self.history_query = ""
        self.return_screen = "menu"
        self.play_timer = QTimer(self)
        self.play_timer.timeout.connect(self.advance)
        # Coalesce frequent plan edits into one safe, atomic disk write.
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(650)
        self.save_timer.timeout.connect(self.flush_debounced_save)
        self.worker = None
        self._state = {}
        self._battle_board = {}
        self._spectrum = [0.0] * 24
        self._profile_turns = os.environ.get("TABOTA_PROFILE_TURNS") == "1"
        self._last_frame_time = None
        self.refresh()

    @Property("QVariantMap", notify=changed)
    def state(self): return self._state

    @Property("QVariantMap", notify=boardChanged)
    def battleBoard(self): return self._battle_board

    @Property("QVariantList", notify=spectrumChanged)
    def musicSpectrum(self): return self._spectrum

    @Slot(list)
    def updateSpectrum(self, bands):
        self._spectrum = bands
        self.spectrumChanged.emit()

    @Slot(str)
    def uiSound(self, kind):
        if kind in ("hover", "click", "shuffle"):
            self.soundRequested.emit(kind)

    def player_text(self, text):
        return (text or "").replace("nameKey", "nazwie karty (bez polskich znaków)")

    def status_badge(self, cid, match=None):
        active = match or self.match
        # Gumbox's Aura uses names in ANY encounter. Only inspect public cards
        # and our hand; never reveal whether the enemy holds a hidden Gumbox.
        name_aura = active and any(u["card"] == "30" and not u["silenced"]
                                  for u in active.units(0) + active.units(1) + active.s["hand"][0])
        if active and (active.s.get("mission") == 3 or name_aura) and CARDS[cid]["kind"] in ("unit", "token"):
            has_a = "a" in CARDS[cid]["nameKey"]
            return ("A" if has_a else "BEZ A",
                    ("Ta karta ma literę A w nazwie." if has_a else "Ta karta nie ma litery A w nazwie.") +
                    " Polskie znaki liczą się jak ich podstawowe litery (Ą = A)." +
                    (" Aura Gumboxa sprawdza nazwy pozostałych własnych kart w jego strefie." if name_aura else ""))
        return ("", "")

    def locate_uid(self, uid, match=None):
        view = match or self.match
        if not view:
            return None, -1
        for p in range(2):
            for u in view.units(p):
                if u["uid"] == uid:
                    return u, p
        for p in range(2):
            found = next((u for u in view.s["hand"][p] if u["uid"] == uid), None)
            if found:
                return found, p
        return None, -1

    def card(self, cid, unit=None, match=None):
        data = dict(CARDS[cid])
        data["description"] = self.player_text(data.get("description", ""))
        data["image"] = QUrl.fromLocalFile(data["image"]).toString() if data["image"] else ""
        data["unlocked"] = cid in (self.store.profile["unlocked"] if self.store.profile else STARTER)
        data["uid"] = unit["uid"] if unit else ""
        data["currentPower"] = match.power(unit) if unit and match and unit["lane"] >= 0 else data["power"]
        data["buff"] = unit["buff"] if unit else 0
        data["aura"] = match.aura(unit) if unit and match and unit["lane"] >= 0 else 0
        data["protected"] = unit["protected"] if unit else False
        data["silenced"] = unit["silenced"] if unit else False
        badge, hint = self.status_badge(cid, match)
        data["nameRuleBadge"] = badge
        data["nameRuleHint"] = hint
        data["pending"] = bool(unit and self.match and not self.match.find(unit["uid"]) and unit["lane"] >= 0)
        data["fortune"] = FORTUNES.get(cid, "")
        data["source"] = "Dostępna od początku" if cid in STARTER else next((f"Nagroda: wyzwanie {e['id']:02} · {e['short']}" for e in ENCOUNTERS if cid in e["unlocks"]), "Żeton")
        return data

    def action_effect(self, action, match=None):
        if "special" in action:
            return {
                "hymn": "Rytuał Hymn: dodaj punkty do wybranej strefy.",
                "ban": "Rytuał Ban: wycisz wybraną kartę przeciwnika. Jej Aura i Finał przestają działać.",
                "clip": "Rytuał Klip: dobierz dodatkowe karty na przyszłą turę.",
                "flight": "Darmowy lot: przenieś wybraną własną kartę do innej strefy z wolnym miejscem.",
            }[action["special"]]
        unit, _ = self.locate_uid(action.get("uid", ""), match)
        if unit:
            return self.player_text(CARDS[unit["card"]]["description"])
        return "Wybierz poprawny cel działania tej karty."

    def describe_option(self, action, index, match):
        targets, owners = [], set()
        for uid in action.get("targets", []):
            unit, owner = self.locate_uid(uid, match)
            if not unit:
                continue
            info = self.card(unit["card"], unit, match if unit.get("lane", -1) >= 0 else None)
            info["owner"] = owner
            targets.append(info)
            owners.add(owner)
        if "special" in action:
            source = {}
            source_title = {"hymn": "Rytuał Hymn", "ban": "Rytuał Ban", "clip": "Rytuał Klip", "flight": "Darmowy lot"}[action["special"]]
        else:
            source_unit, _ = self.locate_uid(action.get("uid", ""), match)
            source = self.card(source_unit["card"], source_unit, match if source_unit and source_unit.get("lane", -1) >= 0 else None) if source_unit else {}
            source_title = source.get("name", "Karta")
        target_side = "twoja karta" if owners == {0} else "karta przeciwnika" if owners == {1} else "zestaw kart" if owners else "bez dodatkowego celu"
        choice = "Kliknij, aby wybrać ten cel."
        if len(targets) == 1:
            choice = "Kliknij tę kartę, aby nałożyć efekt."
        elif len(targets) > 1:
            choice = "Kliknij ten zaznaczony zestaw kart."
        elif action.get("special") == "clip":
            choice = "Ta akcja nie wymaga celu - po prostu zatwierdź ją."
        elif action.get("special") == "hymn":
            choice = "Kliknij strefę, do której trafi Hymn."
        return dict(
            index=index,
            label=(match.action_label(action) if match else ""),
            title="Wybierz cel efektu",
            effect=self.action_effect(action, match),
            source=source,
            sourceTitle=source_title,
            laneName=LANES[action["lane"]],
            destName=LANES[action["dest"]] if action.get("dest", -1) >= 0 else "",
            targets=targets,
            targetSideLabel=target_side.upper(),
            choiceLabel=choice,
            emptyLabel="Bez dodatkowego celu" if not targets else "",
            secondaryText=("Przeniesienie do: " + LANES[action["dest"]]) if action.get("dest", -1) >= 0 else ""
        )

    def catalog_card(self, cid):
        """Locked cards never expose art, name, effects or numerical statistics to QML."""
        c = self.card(cid)
        if c["unlocked"]:
            return c
        return dict(id=cid, unlocked=False, image="", name="Nieodkryta karta",
                    unlockHint=next((f"Wygraj wyzwanie {e['id']:02}: {e['short']}" for e in ENCOUNTERS if cid in e["unlocks"]),
                                    "Odblokuj podczas kampanii"),
                    kind="locked")

    def _make_board(self, prepared=None):
        """Only battle data. Playback skips expensive legality previews.

        An already validated projection can be reused by the drop path, so
        we do not clone and resolve the whole plan a second time on release.
        """
        board = {}
        if self.match:
            m = self.display_match or self.match
            try:
                projected = m if self.busy else (prepared if prepared is not None and m is self.match else m.project(0, self.plan))
            except IllegalMove: projected = m
            lanes = []
            scores, prediction = m.scores(), projected.scores()
            for lane in range(3):
                lanes.append(dict(name=LANES[lane], index=lane, player=scores[0][lane], enemy=scores[1][lane],
                    predicted=prediction[0][lane], predictedEnemy=prediction[1][lane], capacity=m.capacity(lane),
                    playerUnits=[self.card(u["card"], u, projected) for u in projected.units(0, lane)],
                    enemyUnits=[self.card(u["card"], u, projected) for u in projected.units(1, lane)],
                    points=m.s["points"][0][lane], enemyPoints=m.s["points"][1][lane],
                    legal=bool(self.selected and projected.candidates(0, self.selected, lane))))
            hand = []
            for u in m.s["hand"][0]:
                c = self.card(u["card"], u)
                c["planned"] = any(a.get("uid") == u["uid"] for a in self.plan)
                c["selected"] = self.selected == u["uid"]
                c["exchange"] = u["uid"] in self.mulligan_ids
                c["legalLanes"] = ([False, False, False] if self.busy or c["planned"] else
                    [bool(projected.candidates(0, u["uid"], l)) for l in range(3)])
                c["playable"] = self.busy or any(c["legalLanes"])
                hand.append(c)
            ritual = [] if self.busy else projected.ritual_options(0)
            choice = self.match.s["choices"][0] if self.match.s["choices"] else {}
            lesson = m.tutorial_move(0) if not self.busy else None
            guided = lesson is not None
            phase = "submit" if self.plan else "lane" if self.selected else "card"
            board = dict(lanes=lanes, hand=hand, turn=m.s["turn"], maxTurns=m.s["maxTurns"], energy=projected.s["energy"][0],
                tutorialGuided=guided, tutorialPractice=m.s["tutorial"] and m.s["turn"] == 4,
                tutorialPhase=phase if guided else "", tutorialTargetUid=lesson["uid"] if guided else "",
                tutorialTargetCard=lesson["card"] if guided else "", tutorialLane=lesson["lane"] if guided else -1,
                deckCount=len(m.s["deck"][0]), enemyDeck=len(m.s["deck"][1]), enemyHand=len(m.s["hand"][1]),
                discardCount=len(m.s["discard"][0]), log=m.s["log"][-100:], finished=m.s["finished"], winner=m.s["winner"],
                wins=[m.wins(0), m.wins(1)], total=[sum(scores[0]), sum(scores[1])], seed=m.s["seed"],
                plan=[self.match.action_label(a) for a in self.plan], ritual=bool(ritual),
                ritualKinds=list(dict.fromkeys(a["special"] for a in ritual)),
                flight=False if self.busy else bool(projected.flight_options(0)), tutorial=m.s["tutorial"],
                rulePending=self.rule_pending(),
                mulligan=not m.s["mulligan"][0] and not m.s["tutorial"],
                exchangeCount=len(self.mulligan_ids), choice=bool(choice and choice["owner"] == 0),
                hint=self.tutorial_hint() if m.s["tutorial"] else
                    "Wybierz kartę i strefę. Cofaj ruchy bez kary. „Zakończ turę” ujawnia oba plany i wykonuje zagrania.",
                selected=self.card(next(u["card"] for u in m.s["hand"][0] if u["uid"] == self.selected)) if self.selected and any(u["uid"] == self.selected for u in m.s["hand"][0]) else {},
                enemyPreview=self.enemy_preview(m))
        return board

    def refresh_frame(self):
        """Frame updates affect only Battle.qml; avoid rebinding every screen,
        modal, collection image, history entry and audio sync each action."""
        self._battle_board = self._make_board()
        self.boardChanged.emit()

    def refresh_battle(self, prepared=None):
        """Refresh the board after hand selection/planning, not the 76-card
        catalog, 20 encounters, reading history and all global QML screens."""
        self._battle_board = self._make_board(prepared)
        self.boardChanged.emit()
        # Keep compatibility with code that reads api.state['board'] directly.
        self._state["board"] = self._battle_board

    def refresh_options(self, projected=None):
        if self.options and projected is None and self.match:
            projected = self.match.project(0, self.plan)
        self._state["options"] = [self.describe_option(action, i, projected)
                                  for i, action in enumerate(self.options)]
        self.changed.emit()

    def schedule_save(self):
        """Autosave a completed plan after interaction has gone idle."""
        self.save_timer.start()

    def flush_debounced_save(self):
        if not self.safe_save():
            # File failures remain visible rather than silently lost in a timer.
            self.refresh()

    def refresh(self):
        p = self.store.profile
        encounter = deepcopy(ENCOUNTERS[self.mission-1])
        encounter["activeRule"] = encounter_rule(self.mission, self.hard,
            bool(self.match and self.match.s["mission"] == self.mission and self.match.s["tutorial"]
                 and self.screen in ("battle", "pause", "result")))
        encounter["actIntroText"] = {
            1: "Nysmo czeka w poczekalni. Najpierw nauka zasad!",
            6: "Drugi akt: każdy przeciwnik pokazuje własną, absurdalną metę.",
            11: "Trzeci akt: otwarto wolną strefę eksperymentalnych wyzwań.",
            16: "Czwarty akt: ostateczny finał. Naprawdę. Chyba.",
            20: "OSTATNI UCZESTNIK - TOŻSAMOŚĆ UKRYTA. ELTABOBOT: „JESTEM NIM JA.”",
        }.get(self.mission, "")
        encounter["actFinalText"] = {
            5: "ELTABOBOT: „Gratulacje. Ukończono etap podstawowy.”   TABO: „JAK TO PODSTAWOWY?!”",
            10: "NAGRODA ZA DRUGI AKT: BRĄZOWY TABORET.   TABO: „Dziesięciu pokonałem i dajesz mi brązowy stołek?!”",
            15: "FINAŁ TURNIEJU!   ...Pomyłka. PIERD0LA: „No cześć. To który to już finał?”",
        }.get(self.mission, "")
        encounter["image"] = self.card(encounter["portrait"])["image"]
        unlocked = p["unlocked"] if p else STARTER
        completed = p["hardCompleted" if self.hard else "completed"] if p else []
        missions = []
        for e in ENCOUNTERS:
            item = dict(e)
            item["image"] = self.card(e["portrait"])["image"]
            item["done"] = e["id"] in completed
            item["available"] = (e["id"] in (p["completed"] if p else []) or e["id"] == 1) if self.free else (e["id"] == 1 or e["id"]-1 in completed)
            missions.append(item)
        slots = [dict(index=i, name=s["name"] if s else "Pusty slot", progress=len(s["completed"]) if s else 0,
                      updated=s["updated"][:16].replace("T", "  ") if s else "Rozpocznij nową historię", exists=s is not None) for i, s in enumerate(self.store.data["slots"])]
        catalog = []
        for cid, d in CARDS.items():
            if d["kind"] == "token": continue
            known = cid in unlocked
            search_text = (d["name"] + " " + d["description"]) if known else (cid + " nieodkryta")
            if self.collection_query.lower() not in search_text.lower(): continue
            if self.collection_tag != "Wszystkie" and (not known or d["tag"] != self.collection_tag): continue
            c = self.catalog_card(cid)
            c["count"] = self.deck.count(cid)
            c["offered"] = self.offer.count(cid) if self.draft else (2 if cid in unlocked else 0)
            if self.screen == "builder" and (not c["offered"] or not c["unlocked"]): continue
            catalog.append(c)
        deck_counts = Counter(self.deck)
        deckview = [dict(self.card(cid), count=count) for cid, count in sorted(deck_counts.items(), key=lambda x: (CARDS[x[0]]["cost"], x[0]))]
        history = [dict(r, date=r["created"][:16].replace("T", "  "), complete=len(r["revealed"]) == r["count"])
                   for r in sorted(self.store.tarot["readings"], key=lambda r: r["created"], reverse=True)
                   if self.history_query.lower() in (r["question"]+" "+r["created"]+" "+str(r["count"])).lower()]
        reading = deepcopy(self.reading) if self.reading else {}
        if reading:
            reading["items"] = [dict(self.card(cid), position=reading["positions"][i], interpretation=reading["interpretations"][i], revealed=i in reading["revealed"], index=i) for i, cid in enumerate(reading["cards"])]
            reading["complete"] = len(reading["revealed"]) == reading["count"]
        board = self._make_board()
        detail = self.card(self.detail) if self.detail else {}
        if self.match:
            try: projected = self.match.project(0, self.plan)
            except IllegalMove: projected = self.match
        else:
            projected = None
        self._state = dict(screen=self.screen, notice=self.notice, confirmation=self.confirmation, busy=self.busy,
            profile=bool(p), activeSlot=self.store.data["active"], profileName=p["name"] if p else "Gość", slots=slots,
            back=QUrl.fromLocalFile(str(ROOT/"karty-rewers.png")).toString(), hero=self.card("01")["image"],
            settings=dict(self.store.settings), dataPath=str(self.store.root), missions=missions, encounter=encounter,
            completed=len(completed), unlocked=len(unlocked), hard=self.hard, free=self.free,
            hardAvailable=bool(self.store.settings["veteran"] or p and len(p["completed"]) == 20), difficulty=self.difficulty,
            board=board, options=[self.describe_option(a, i, projected if self.match else None) for i, a in enumerate(self.options)],
            detail=detail, detailTarot=self.detail_tarot, catalog=catalog, deck=deckview, deckCount=len(self.deck),
            deckUnits=sum(CARDS[c]["kind"] == "unit" for c in self.deck),
            curve=[sum(CARDS[c]["cost"] == cost for c in self.deck) for cost in range(1, 7)],
            deckErrors=validate_deck(self.deck, unlocked, self.offer if self.draft else None),
            presets=p["presets"] if p else [], draft=self.draft, offerCount=len(self.offer),
            reading=reading, history=history, dialogue=self.dialogue,
            resumable=bool(p and p["match"] and not p["match"]["finished"]),
            journal=[dict(e, image=self.card(e["portrait"])["image"]) for e in ENCOUNTERS if p and e["id"] in p["completed"]])
        self._battle_board = board
        self.boardChanged.emit()
        self.changed.emit()

    def safe_save(self):
        self.save_timer.stop()  # A forced save supersedes the pending debounce.
        try:
            p = self.store.profile
            if p:
                p["updated"] = stamp()
                if self.match:
                    p["match"] = deepcopy(self.match.s)
                    p["plan"] = deepcopy(self.plan)
                    p["mode"] = self.match.s.get("mode", "free" if self.free else "story")
                self.store.campaign()
            return True
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.notice = f"Nie zapisano na dysku: {exc}. Stan pozostaje w pamięci. Użyj eksportu w Opcjach."
            return False

    def fail(self, message):
        self.soundRequested.emit("error")
        self.notice = str(message)
        self.busy = False
        self.refresh()

    @Slot(str)
    def navigate(self, target):
        if self.busy: return
        self.detail = ""
        self.options = []
        if target in ["map", "collection", "builder"] and not self.store.profile:
            target = "slots"
        if self.screen == "battle": self.safe_save()
        if target == "fortune" and self.reading:
            self.save_reading()
        self.screen = target
        self.soundRequested.emit("click")
        self.refresh()

    @Slot(str)
    def inspect(self, cid):
        if cid not in CARDS: return
        if self.screen in ("collection", "builder") and cid not in (self.store.profile["unlocked"] if self.store.profile else STARTER):
            return  # Only the card back and unlock instructions are visible.
        self.detail = cid
        self.soundRequested.emit("select")
        self.detail_tarot = self.screen in ["fortune", "reading", "history"]
        # A modal shouldn't trigger the full encounter, collection and hand
        # recomputation just to display the already known card.
        self._state["detail"] = self.card(cid)
        self._state["detailTarot"] = self.detail_tarot
        self.changed.emit()

    @Slot()
    def closeDetail(self):
        self.detail = ""
        self._state["detail"] = {}
        self.changed.emit()

    @Slot()
    def dismiss(self):
        self.notice = ""
        self.refresh()

    @Slot(int, str)
    def newGame(self, slot, name):
        if slot not in range(3): return
        if self.store.data["slots"][slot]:
            self.confirmation = "Zastąpić kampanię w tym slocie? Historia wróżb jest przechowywana osobno."
            self.pending = ("new", slot, name)
        else: self.create_profile(slot, name)
        self.refresh()

    def create_profile(self, slot, name):
        self.store.data["active"] = slot
        self.store.data["slots"][slot] = new_profile(name or "Taboret")
        self.match, self.plan = None, []
        self.hard, self.free = False, False
        self.mission = 1
        self.safe_save()
        self.screen = "intro"

    @Slot(bool)
    def confirm(self, accepted):
        pending = self.pending
        self.confirmation, self.pending = "", None
        if accepted and pending:
            if pending[0] == "new": self.create_profile(pending[1], pending[2])
            elif pending[0] == "deleteReading":
                self.store.tarot["readings"] = [r for r in self.store.tarot["readings"] if r["id"] != pending[1]]
                if self.reading and self.reading["id"] == pending[1]: self.reading = None
                try: self.store.readings()
                except OSError as e: self.notice = str(e)
                self.screen = "history"
            elif pending[0] == "clearReadings":
                self.store.tarot["readings"] = []
                self.reading = None
                try: self.store.readings()
                except OSError as e: self.notice = str(e)
            elif pending[0] == "abandon":
                self.match = None
                self.plan = []
                self.store.profile["match"] = None
                self.store.profile["plan"] = []
                self.safe_save()
                self.screen = "map"
            elif pending[0] == "replaceMatch": self.begin_match(pending[1])
            elif pending[0] == "import": self.do_import(pending[1], pending[2])
        self.refresh()

    @Slot(int)
    def loadSlot(self, slot):
        if slot not in range(3) or not self.store.data["slots"][slot]: return
        self.store.data["active"] = slot
        p = self.store.profile
        self.hard = p["hard"]
        self.offer, self.deck = p["offer"][:], p["deck"][:]
        self.match = Match.restore(p["match"]) if p["match"] else None
        self.plan = deepcopy(p["plan"]) if self.match else []
        self.free = p["mode"] == "free"
        if self.match:
            self.mission = self.match.s["mission"]
            self.hard = self.match.s["hard"]
            if self.match.s["finished"] and self.match.s["winner"] == 0 and not self.free:
                self.store.reward(self.mission, self.hard)
        self.screen = "battle" if self.match and not self.match.s["finished"] else "result" if self.match else "map"
        self.selected, self.options = "", []
        self.display_match = None
        self.dialogue = ""
        self.safe_save()
        self.refresh()

    @Slot(bool, bool)
    def campaignMode(self, hard, free):
        if hard and not self._state["hardAvailable"]:
            return self.fail("Ukończ FABUŁĘ lub włącz tryb weterana w Opcjach.")
        self.hard, self.free = hard, free
        if self.store.profile:
            self.store.profile["hard"] = hard
            self.safe_save()
        self.screen = "map"
        self.refresh()

    @Slot(str)
    def setDifficulty(self, difficulty):
        if difficulty in ["easy", "normal", "hard"]: self.difficulty = difficulty
        self.refresh()

    @Slot(int)
    def chooseMission(self, mission):
        if not 1 <= mission <= 20 or not self._state["missions"][mission-1]["available"]: return
        self.mission = mission
        self.dialogue = ENCOUNTERS[mission-1]["dialogue"].get("START", "")
        self.screen = "briefing"
        self.soundRequested.emit("click")
        self.refresh()

    @Slot(bool)
    def start(self, tutorial=False):
        if self.match and not self.match.s["finished"]:
            self.pending = ("replaceMatch", tutorial)
            self.confirmation = "Rozpocząć nowy pojedynek i zastąpić zapis trwającego meczu?"
            return self.refresh()
        self.begin_match(tutorial)

    def begin_match(self, tutorial=False):
        if not self.store.profile: return
        if self.hard and not self.free and not self.draft:
            return self.openDraft(False)
        e = ENCOUNTERS[self.mission-1]
        deck = self.deck if (self.hard or self.free) and not validate_deck(self.deck, self.store.profile["unlocked"], self.offer if self.hard and not self.free else None) else e["storyDeck"]
        if self.hard and not self.free:
            errors = validate_deck(deck, self.store.profile["unlocked"], self.offer)
            if errors: return self.fail(" ".join(errors))
        self.match = Match(self.mission, self.hard, secrets.randbits(31), [deck, e["enemyDeck"]], tutorial and self.mission == 1 and not self.hard)
        self.match.s["mode"] = "free" if self.free else "story"
        # Saved inside the match: returning to an unfinished duel won't reopen a dismissed modal.
        self.match.s["flags"]["ruleBriefingSeen"] = False
        self.plan, self.options, self.mulligan_ids = [], [], []
        self.selected = ""
        self.saved_result = False
        self.display_match = None
        self.draft = False
        self.dialogue_seen = set()
        self.dialogue = e["dialogue"].get("START", "")
        self.screen = "battle"
        if self.match.s["tutorial"]:
            self.match.s["mulligan"] = [True, True]
        self.match.mulligan(1, []) if not self.match.s["mulligan"][1] else None
        self.safe_save()
        self.soundRequested.emit("start")
        self.refresh()

    def rule_pending(self):
        return bool(self.match and not self.match.s["tutorial"] and self.match.s["flags"].get("ruleBriefingSeen", True) is False)

    @Slot()
    def acknowledgeRule(self):
        if not self.rule_pending() or self.busy: return
        self.match.s["flags"]["ruleBriefingSeen"] = True
        self.safe_save()
        self.soundRequested.emit("click")
        self.refresh()

    @Slot(str)
    def selectCard(self, uid):
        if self.rule_pending(): return
        if self.busy or not self.match or self.match.s["finished"]: return
        if self.match.s["choices"]:
            try: self.match.discard_choice(uid)
            except IllegalMove as e: return self.fail(e)
            self.soundRequested.emit("card")
            self.finish_turn()
            self.safe_save()
            return self.refresh()
        if not self.match.s["mulligan"][0]:
            if uid in self.mulligan_ids: self.mulligan_ids.remove(uid)
            elif len(self.mulligan_ids) < 2: self.mulligan_ids.append(uid)
            else: return self.fail("Możesz wymienić najwyżej 2 karty. Odznacz jedną, aby wybrać inną.")
            self.soundRequested.emit("select")
            return self.refresh_battle()
        if any(a.get("uid") == uid for a in self.plan): return
        lesson = self.match.tutorial_move()
        if lesson and uid != lesson["uid"]:
            return self.fail("W tej części nauki wybierz podświetloną kartę. Po turze 3 zagrasz samodzielnie.")
        self.selected = "" if self.selected == uid else uid
        self.options = []
        self.soundRequested.emit("select")
        self.refresh_battle()

    @Slot()
    def exchange(self):
        if self.rule_pending(): return
        if not self.match or self.busy: return
        try: self.match.mulligan(0, self.mulligan_ids)
        except IllegalMove as e: return self.fail(e)
        self.mulligan_ids = []
        self.soundRequested.emit("shuffle")
        self.safe_save()
        self.refresh()

    @Slot(str, int)
    def dropCard(self, uid, lane):
        """Single bridge call when a card is actually dropped onto a lane.

        No global UI refresh or filesystem operation is performed while the
        pointer is moving. Click-to-select still uses selectCard/chooseLane.
        """
        if self.rule_pending() or self.busy or not self.match or self.match.s["finished"]:
            return
        if not self.match.s["mulligan"][0] or self.match.s["choices"]:
            return
        if lane not in range(3) or any(a.get("uid") == uid for a in self.plan):
            return
        if not any(u["uid"] == uid for u in self.match.s["hand"][0]):
            return
        lesson = self.match.tutorial_move()
        if lesson and uid != lesson["uid"]:
            return self.fail("W tej części nauki zagraj podświetloną kartę.")
        self.selected = uid
        self.options = []
        self.chooseLane(lane)

    @Slot(int)
    def chooseLane(self, lane):
        if self.rule_pending(): return
        if not self.match or not self.selected or self.busy: return
        lesson = self.match.tutorial_move()
        if lesson and lane != lesson["lane"]:
            return self.fail("Teraz zagraj kartę do podświetlonej strefy: " + LANES[lesson["lane"]] + ".")
        projected = self.match.project(0, self.plan)
        self.options = projected.candidates(0, self.selected, lane)
        if not self.options: return self.fail("Nie można zagrać tu tej karty: sprawdź Energię, wolne sloty i wymagany cel.")
        if len(self.options) == 1: return self.chooseOption(0)
        self.refresh_battle(projected)
        self.refresh_options(projected)

    @Slot(int)
    def chooseOption(self, index):
        if self.rule_pending(): return
        if self.busy or not 0 <= index < len(self.options): return
        action = self.options[index]
        if "special" in action:
            self.plan.insert(0, action)
            self.plan.sort(key=lambda a: 0 if a.get("special") == "flight" else 1 if "special" in a else 2)
        else: self.plan.append(action)
        try: projected = self.match.project(0, self.plan)
        except IllegalMove as e:
            self.plan.remove(action)
            return self.fail(e)
        was_modal_open = bool(self._state.get("options"))
        self.selected, self.options = "", []
        self.soundRequested.emit("ritual" if "special" in action else "card")
        self.schedule_save()
        self.refresh_battle(projected)
        if was_modal_open:
            self.refresh_options()

    @Slot(str)
    def ritual(self, kind):
        if self.rule_pending(): return
        if self.busy or not self.match: return
        projected = self.match.project(0, self.plan)
        self.options = projected.flight_options(0) if kind == "flight" else [a for a in projected.ritual_options(0) if a["special"] == kind]
        if not self.options: return self.fail("Ta akcja nie ma teraz legalnego celu.")
        if kind == "clip": self.notice = "Dociąg nastąpi przy ujawnieniu. Nowe karty będą dostępne do planowania w następnej turze; limit ręki: 10."
        if len(self.options) == 1: return self.chooseOption(0)
        self.refresh()

    @Slot()
    def cancelOptions(self):
        self.options = []
        self.refresh()

    @Slot()
    def undo(self):
        if self.rule_pending(): return
        if self.busy: return
        if self.plan:
            self.plan.pop()
            self.soundRequested.emit("undo")
        self.options, self.selected = [], ""
        self.safe_save()
        self.refresh()

    @Slot()
    def submit(self):
        if self.rule_pending(): return
        if self.busy or not self.match or self.match.s["finished"] or self.match.s["choices"]: return
        if not self.match.s["mulligan"][0]: return self.exchange()
        lesson = self.match.tutorial_move()
        if lesson and (len(self.plan) != 1 or self.plan[0].get("uid") != lesson["uid"] or self.plan[0].get("lane") != lesson["lane"]):
            return self.fail("Najpierw zagraj wskazaną kartę do strefy " + LANES[lesson["lane"]] + ".")
        try: self.match.project(0, self.plan)
        except IllegalMove as e: return self.fail(e)
        # Do not let a debounced disk write fire during the next turn's animation.
        if self.save_timer.isActive():
            self.safe_save()
        self.busy = True
        self.soundRequested.emit("turn")
        self.selected, self.options = "", []
        self.refresh()
        self.worker = Thinker(self.match, "hard" if self.hard else ("easy" if self.mission <= 2 and not self.free else self.difficulty), self.plan)
        self.worker.signals.done.connect(self.resolve)
        self.worker.signals.error.connect(self.fail)
        QThreadPool.globalInstance().start(self.worker)

    @Slot(object)
    def resolve(self, outcome):
        try:
            final_state, frames, cpu_ms = outcome
            if self._profile_turns:
                print(f"[TABOt perf] AI + przygotowanie tury: {cpu_ms:.1f} ms, klatki ruchów: {len(frames)}", flush=True)
            self._last_frame_time = None
            before = self.match
            self.match = Match.restore(final_state)
            self.frames = deque(frames)
            self.plan = []
            self.display_match = before
            if self.match.s["finished"] and self.match.s["winner"] == 0 and not self.free:
                self.store.reward(self.mission, self.hard)
                self.saved_result = True
            self.safe_save()
            self.play_timer.start(65 if self.store.settings["reduced"] else 520)
        except Exception as exc:
            traceback.print_exc()
            self.fail(exc)

    @Slot()
    def advance(self):
        if self.frames:
            start = perf_counter() if self._profile_turns else 0
            interval = (start - self._last_frame_time) * 1000 if self._last_frame_time is not None else 0
            before = self.display_match
            self.display_match = Match.restore(self.frames.popleft())
            if before and before.s["turn"] != self.display_match.s["turn"]:
                self.soundRequested.emit("turn")
            elif before and any(len(before.s["hand"][p]) > len(self.display_match.s["hand"][p]) for p in range(2)):
                self.soundRequested.emit("card")
            self.refresh_frame()
            if self._profile_turns:
                # Frame interval shows event-loop delays; processing is just
                # Python snapshot conversion + synchronous QML notifications,
                # not the time of the eventual GPU render.
                work_ms = (perf_counter() - start) * 1000
                print(f"[TABOt perf] Odstęp klatek ruchów: {interval:.0f} ms; aktualizacja planszy: {work_ms:.1f} ms", flush=True)
                self._last_frame_time = start
        else:
            self.play_timer.stop()
            self.display_match = None
            self.busy = False
            self.finish_turn()
            self.refresh()

    def finish_turn(self):
        while self.match.s["choices"] and self.match.s["choices"][0]["owner"] == 1:
            uid = min(self.match.s["hand"][1], key=lambda u: definition(u)["power"])["uid"]
            self.match.discard_choice(uid)
        e = ENCOUNTERS[self.mission-1]
        if self.match.s["choices"]:
            self.screen = "battle"
            self.safe_save()
            return
        if self.match.s["finished"]:
            if self.match.s["winner"] == 0 and not self.free and not self.saved_result:
                self.store.reward(self.mission, self.hard)
            self.saved_result = True
            self.dialogue = e["dialogue"].get("LOSE" if self.match.s["winner"] == 0 else "WIN", "")
            self.screen = "result"
            self.soundRequested.emit({0: "win", 1: "lose", -1: "draw"}[self.match.s["winner"]])
        elif 3 <= self.match.s["turn"]-1 <= 5:
            trigger = "LEAD" if self.match.wins(1) >= 2 else "TRAIL" if self.match.wins(0) >= 2 else ""
            if trigger and trigger not in self.dialogue_seen:
                self.dialogue_seen.add(trigger)
                self.dialogue = e["dialogue"].get(trigger, "")
        self.safe_save()

    @Slot()
    def skipAnimation(self):
        # Planning may still run. Do not finish a turn until its result exists.
        if self.frames:
            self.frames.clear()
            self.advance()

    @Slot()
    def nextMission(self):
        if self.mission == 20 and self.match and self.match.s["winner"] == 0 and not self.free:
            self.screen = "ending"
        else: self.screen = "map"
        self.refresh()

    @Slot()
    def abandon(self):
        self.confirmation = "Poddać bieżący pojedynek? Zachowasz kolekcję i ukończone wyzwania."
        self.pending = ("abandon",)
        self.refresh()

    def enemy_preview(self, m):
        if self.busy:
            return "UJAWNIANIE PLANÓW · obie strony wykonują wcześniej zatwierdzone ruchy."
        if m.s["choices"]:
            return "SPRAWDŹ PŁYTY · odrzuć kartę przed przejściem do następnej tury."
        if m.s["tutorial"] and m.s["turn"] <= 3:
            return "JAWNY PLAN NAUKI: " + " · ".join(m.action_label(a) for a in ai_plan(m))
        if m.s["mission"] == 4 and m.s["turn"] == 4 and not m.s["hard"]:
            return "PODPOWIEDŹ RYTUAŁU: " + " · ".join(m.action_label(a) for a in ai_plan(m) if "special" in a)
        return "Plan rywala pozostaje ukryty do ujawnienia."

    def tutorial_hint(self):
        lesson = self.match.tutorial_move()
        if lesson:
            card = CARDS[lesson["card"]]
            lane = LANES[lesson["lane"]]
            if self.plan:
                return "Dobrze! Kliknij «Zakończ turę», aby rozegrać zaplanowany ruch."
            if self.selected:
                return f"Teraz kliknij podświetloną strefę {lane} na stole."
            return f"Znajdź w ręce podświetloną kartę «{card['name']}» (⚡ {card['cost']}) i kliknij ją."
        if self.match.s["turn"] == 4:
            return "Teraz grasz samodzielnie! Wybieraj karty i strefy, aby wygrać co najmniej 2 strefy. Możesz cofać ruchy."
        return "Sam decydujesz, które karty zagrać. Pamiętaj: 2 wygrane strefy są ważniejsze niż suma punktów."

    @Slot(bool)
    def openDraft(self, reuse=False):
        if not self.store.profile: return
        self.draft = True
        if not reuse or not self.offer:
            self.offer = draft_offer(self.store.profile["unlocked"], secrets.randbits(31))
            self.deck = auto_deck(self.offer)
        self.store.profile["offer"], self.store.profile["deck"] = self.offer[:], self.deck[:]
        self.collection_query, self.collection_tag = "", "Wszystkie"
        self.screen = "builder"
        self.safe_save()
        self.refresh()

    @Slot()
    def openBuilder(self):
        if not self.store.profile: return self.navigate("slots")
        self.draft = False
        if not self.deck: self.deck = ENCOUNTERS[0]["storyDeck"][:]
        self.screen = "builder"
        self.collection_query, self.collection_tag = "", "Wszystkie"
        self.refresh()

    @Slot(str, int)
    def deckChange(self, cid, change):
        if cid not in CARDS or not self.store.profile: return
        limit = self.offer.count(cid) if self.draft else 2
        if change > 0 and len(self.deck) < 18 and self.deck.count(cid) < limit and cid in self.store.profile["unlocked"]:
            self.deck.append(cid)
        elif change < 0 and cid in self.deck: self.deck.remove(cid)
        self.store.profile["deck"] = self.deck[:]
        self.safe_save()
        self.refresh()

    @Slot()
    def autoDeck(self):
        self.deck = auto_deck(self.offer if self.draft else self.store.profile["unlocked"]*2)
        self.store.profile["deck"] = self.deck[:]
        self.safe_save()
        self.refresh()

    @Slot()
    def clearDeck(self):
        self.deck = []
        self.refresh()

    @Slot(str)
    def savePreset(self, name):
        p = self.store.profile
        if not p: return
        errors = validate_deck(self.deck, p["unlocked"])
        if errors: return self.fail(" ".join(errors))
        if len(p["presets"]) >= 8: return self.fail("Masz już 8 presetów. Usuń jeden przyciskiem obok jego nazwy.")
        p["presets"].append(dict(name=(name or f"Talia {len(p['presets'])+1}")[:60], cards=self.deck[:]))
        self.safe_save()
        self.notice = "Talia zapisana."
        self.refresh()

    @Slot(int, bool)
    def preset(self, index, delete=False):
        presets = self.store.profile["presets"]
        if not 0 <= index < len(presets): return
        if delete:
            presets.pop(index)
            self.safe_save()
        else:
            cards = presets[index]["cards"]
            if self.draft and Counter(cards)-Counter(self.offer): return self.fail("Ten preset nie mieści się w aktualnej ofercie draftu.")
            self.deck = cards[:]
        self.refresh()

    @Slot(str, str)
    def filterCards(self, query, tag):
        self.collection_query, self.collection_tag = query, tag
        self.refresh()

    @Slot(str, int, int)
    def divine(self, question, count, cut):
        try: self.reading = make_reading(question, count, cut)
        except ValueError as e: return self.fail(e)
        self.screen = "reading"
        self.save_reading()
        self.soundRequested.emit("start")
        self.refresh()

    def save_reading(self, force=False):
        if not self.reading or (not force and not self.store.settings["autoReadings"]): return
        readings = self.store.tarot["readings"]
        old = next((i for i, r in enumerate(readings) if r["id"] == self.reading["id"]), -1)
        if old >= 0: readings[old] = deepcopy(self.reading)
        else: readings.append(deepcopy(self.reading))
        try: self.store.readings()
        except (OSError, ValueError) as e: self.notice = f"Wróżba pozostaje w pamięci; zapis nie powiódł się: {e}. Wyeksportuj ją w Opcjach."

    @Slot(int)
    def reveal(self, index):
        if not self.reading or not 0 <= index < self.reading["count"]: return
        if index not in self.reading["revealed"]:
            self.reading["revealed"].append(index)
            self.save_reading()
            self.soundRequested.emit("reveal")
        else: return self.inspect(self.reading["cards"][index])
        self.refresh()

    @Slot(str)
    def saveNote(self, note):
        if self.reading:
            self.reading["note"] = note[:5000]
            self.save_reading(True)
            self.notice = "Notatka i układ zapisane lokalnie."
            self.refresh()

    @Slot(str)
    def openReading(self, rid):
        record = next((r for r in self.store.tarot["readings"] if r["id"] == rid), None)
        if record:
            self.reading = deepcopy(record)
            self.screen = "reading"
            self.refresh()

    @Slot(str)
    def filterHistory(self, query):
        self.history_query = query
        self.refresh()

    @Slot(str)
    def deleteReading(self, rid):
        self.pending = ("deleteReading", rid) if rid else ("clearReadings",)
        self.confirmation = "Usunąć tę wróżbę z lokalnej historii?" if rid else "Usunąć całą historię wróżb z tego urządzenia?"
        self.refresh()

    @Slot(str, "QVariant")
    def setting(self, name, value):
        if name not in self.store.settings or name == "schema": return
        if name in ("volume", "musicVolume"): value = max(0, min(1, float(value)))
        else: value = bool(value)
        self.store.settings[name] = value
        if name not in ("volume", "musicVolume"):
            self.soundRequested.emit("click")
        try: self.store.write("settings.json", self.store.settings)
        except OSError as e: self.notice = str(e)
        self.refresh()

    @Slot(str)
    def exportData(self, kind):
        value = self.store.data if kind == "campaign" else dict(schema=SCHEMA, readings=[self.reading]) if kind == "reading" and self.reading else self.store.tarot
        path, _ = QFileDialog.getSaveFileName(None, "Eksport danych Kart TABOta", f"tabota-{kind}.json", "JSON (*.json)")
        if not path: return
        try:
            Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
            self.notice = "Eksport zapisany: " + path
        except OSError as e: self.notice = str(e)
        self.refresh()

    @Slot(str)
    def importData(self, kind):
        path, _ = QFileDialog.getOpenFileName(None, "Import danych Kart TABOta", "", "JSON (*.json)")
        if not path: return
        if kind == "campaign":
            self.pending = ("import", path, kind)
            self.confirmation = "Import zastąpi trzy sloty kampanii. Obecny plik zostanie zachowany jako .bak. Kontynuować?"
            self.refresh()
        else: self.do_import(path, kind)

    def do_import(self, path, kind):
        try:
            self.store.import_file(path, kind)
            if kind == "campaign": self.match, self.plan = None, []
            self.notice = "Dane zaimportowane i zwalidowane."
        except (OSError, ValueError, KeyError, TypeError, IndexError) as e: self.notice = f"Import odrzucony: {e}"
        self.refresh()

    @Slot()
    def quit(self):
        # Resolution is computed before playback; saving never serializes half a turn.
        self.safe_save()
        self.save_reading()
        self.quitRequested.emit()
