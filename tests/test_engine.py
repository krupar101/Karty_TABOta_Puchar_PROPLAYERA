import json
import random
import unittest
from collections import Counter
from copy import deepcopy

from tabota.content import CARDS, ENCOUNTERS, FORTUNES, STARTER, validate_deck
from tabota.engine import Match, IllegalMove, ai_plan, auto_deck, draft_offer


def empty(mission=1, hard=False, turn=6):
    m = Match(mission, hard, 2030)
    m.s["board"] = [[[], [], []], [[], [], []]]
    m.s["hand"] = [[], []]
    m.s["deck"] = [[], []]
    m.s["turn"] = turn
    m.s["energy"] = [turn, turn]
    m.s["log"] = []
    return m


def place(m, cid, p=0, lane=0):
    u = m.new_unit(cid, p, lane)
    m.units(p, lane).append(u)
    return u


def play(m, cid, p=0, lane=0, target=None, dest=None):
    u = m.new_unit(cid, p)
    m.s["hand"][p].append(u)
    options = m.candidates(p, u["uid"], lane)
    if target is not None: options = [a for a in options if target["uid"] in a["targets"]]
    if dest is not None: options = [a for a in options if a["dest"] == dest]
    if not options: raise AssertionError(f"No legal action for {cid}")
    m.apply(p, options[0])
    return u


class ContentTests(unittest.TestCase):
    def test_complete_catalog_assets_rewards(self):
        from pathlib import Path
        self.assertEqual(len(FORTUNES), 52)
        self.assertEqual(sum(c["kind"] == "unit" for c in CARDS.values()), 52)
        self.assertEqual(sum(c["kind"] == "event" for c in CARDS.values()), 24)
        available = set(STARTER)
        for e in ENCOUNTERS:
            self.assertEqual(validate_deck(e["storyDeck"], available), [], e["id"])
            self.assertEqual(validate_deck(e["enemyDeck"]), [])
            self.assertEqual(len(e["dialogue"]), 6)
            self.assertTrue(e["rule"] and e["hardRule"])
            available.update(e["unlocks"])
        self.assertEqual(len(available), 76)
        for cid in FORTUNES: self.assertTrue(Path(CARDS[cid]["image"]).is_file())

    def test_deck_validation(self):
        good = ENCOUNTERS[0]["storyDeck"]
        self.assertFalse(validate_deck(good))
        for bad in [[], good + ["01"], ["01"]*18, ["E01"]*18, good[:-1]+["T1"], good[:-1]+["99"]]:
            self.assertTrue(validate_deck(bad))
        self.assertTrue(validate_deck(good, []))
        self.assertTrue(validate_deck(good, offer=["01"]*24))

    def test_draft_always_buildable(self):
        unlocked = [c for c in CARDS if CARDS[c]["kind"] != "token"]
        for pool in [STARTER, unlocked]:
            for seed in range(100):
                offer = draft_offer(pool, seed)
                self.assertEqual(len(offer), 24)
                self.assertLessEqual(max(Counter(offer).values()), 2)
                self.assertGreaterEqual(sum(CARDS[c]["kind"] == "unit" for c in offer), 16)
                self.assertGreaterEqual(sum(CARDS[c]["cost"] <= 2 for c in offer), 5)
                self.assertFalse(validate_deck(auto_deck(offer), pool, offer))
                if pool is unlocked:
                    self.assertGreaterEqual(len({c for c in offer if CARDS[c]["cost"] >= 5}), 3)


class RulesTests(unittest.TestCase):
    def test_tutorial_exact_gdd_result(self):
        m = Match(tutorial=True)
        script = [[("06",0)],[("04",1)],[("10",2)],[("41",0),("E01",0),("31",2)],[("10",1),("04",2)],[("01",0)]]
        for moves in script:
            projected, plan = m.clone(), []
            for cid, lane in moves:
                u = next(u for u in projected.s["hand"][0] if u["card"] == cid)
                options = projected.candidates(0, u["uid"], lane)
                if cid == "E01": options = [a for a in options if projected.find(a["targets"][0])["card"] == "06"]
                plan.append(options[0])
                projected.apply(0, options[0])
            m.commit([plan, ai_plan(m)])
        self.assertEqual(m.scores(), [[15,10,13],[20,8,5]])
        self.assertEqual(m.s["winner"], 0)

    def test_scoring_lanes_before_total(self):
        m = empty()
        m.s["points"] = [[9,8,2],[8,7,30]]
        m.finals()
        self.assertEqual(m.s["winner"], 0)
        m = empty()
        m.s["points"] = [[9,4,2],[8,7,2]]
        m.finals()
        self.assertEqual(m.s["winner"], 1)
        m = empty(); m.finals(); self.assertEqual(m.s["winner"], -1)

    def test_auras_all_six(self):
        m = empty()
        h = place(m,"04"); self.assertEqual(m.power(h),5)
        other=place(m,"06"); self.assertEqual(m.power(h),3)
        widz=place(m,"10"); self.assertEqual(m.power(other),3)
        m=empty(); n=place(m,"08"); place(m,"07"); self.assertEqual(m.power(n),5)
        m=empty(); n=place(m,"13"); place(m,"39"); self.assertEqual(m.power(n),6)
        m=empty(); n=place(m,"20"); place(m,"35"); place(m,"33"); self.assertEqual(m.power(n),8)
        m=empty(); n=place(m,"30"); self.assertEqual(m.power(n),5); place(m,"02"); self.assertEqual(m.power(n),3)
        m=empty(); n=place(m,"31",lane=2); self.assertEqual(m.power(n),3)

    def test_protection_consumed_once_and_silence_keeps_entry(self):
        m=empty(); u=place(m,"21"); m.buff(u,2); u["protected"]=True
        m.silence(u); self.assertFalse(u["silenced"]); self.assertFalse(u["protected"])
        m.silence(u); self.assertTrue(u["silenced"]); self.assertEqual(m.power(u),5)
        m=empty(); u=place(m,"04"); m.silence(u); self.assertEqual(m.power(u),3)

    def test_modifier_caps_and_minimum(self):
        m=empty(); u=place(m,"02")
        m.buff(u,99); self.assertEqual(u["buff"],4)
        m.buff(u,-99); self.assertEqual(u["buff"],-4); self.assertEqual(m.power(u),0)

    def test_cydyn_zero_one_two_tokens(self):
        for n, expected in [(0,3),(2,4),(3,4)]:
            m=empty()
            for _ in range(n): place(m,"10")
            play(m,"50")
            self.assertEqual(len(m.units(0,0)),expected)
            self.assertEqual(sum(u["card"]=="T3" for u in m.units(0,0)),min(2,3-n))

    def test_refund_when_slot_filled_before_resolution(self):
        m=empty()
        u=m.new_unit("10",0); m.s["hand"][0].append(u)
        a=m.candidates(0,u["uid"],0)[0]
        for _ in range(4): place(m,"06")
        m.apply(0,a)
        self.assertIn(u,m.s["hand"][0]); self.assertEqual(m.s["energy"][0],6)

    def test_failed_move_does_not_delete(self):
        m=empty(); u=place(m,"10")
        for _ in range(4): place(m,"06",lane=1)
        self.assertFalse(m.move(u,1)); self.assertIn(u,m.units(0,0))

    def test_mulligan_once_and_seeded(self):
        for seed in [1,2,3]:
            a,b=Match(seed=seed),Match(seed=seed)
            ids=[u["uid"] for u in a.s["hand"][0]][:2]
            a.mulligan(0,ids); b.mulligan(0,ids)
            self.assertEqual(a.s,b.s); self.assertEqual(len(a.s["hand"][0]),5)
            with self.assertRaises(IllegalMove): a.mulligan(0,[])

    def test_draw_limits_empty_and_preview_privacy(self):
        m=Match(); projected=m.clone(); before=deepcopy(projected.s); projected.draw(0,2)
        self.assertEqual(projected.s,before)
        m.draw(0,18); self.assertEqual(len(m.s["hand"][0]),10); self.assertEqual(len(m.s["discard"][0]),8)
        m.draw(0,5); self.assertEqual(len(m.s["hand"][0]),10)

    def test_plan_double_card_and_energy_rejected(self):
        m=empty(turn=1); u=m.new_unit("02",0); m.s["hand"][0].append(u)
        a=m.candidates(0,u["uid"],0)[0]
        with self.assertRaises(IllegalMove): m.project(0,[a,a])
        u=m.new_unit("01",0); m.s["hand"][0].append(u)
        self.assertFalse(m.candidates(0,u["uid"],0))

    def test_ritual_and_remixes(self):
        for mission in [1,2,3]: self.assertFalse(empty(mission,turn=4).ritual_options(0))
        m=empty(4,turn=4); m.apply(0,m.ritual_options(0)[0]); self.assertEqual(m.s["points"][0][0],3); self.assertEqual(m.s["energy"][0],4)
        self.assertFalse(m.ritual_options(0))
        m=empty(13,turn=4); m.apply(0,m.ritual_options(0)[0]); self.assertEqual(m.s["points"][0][0],5)
        m=empty(17,True,4); place(m,"04",1); self.assertFalse(any(a["special"]=="ban" for a in m.ritual_options(0)))

    def test_final_bot_only_first_entry(self):
        m=empty(20,turn=2); m.s["energy"]=[6,6]
        first=play(m,"21",lane=0); second=play(m,"43",lane=0)
        self.assertEqual(first["buff"],0); self.assertEqual(second["buff"],2)
        self.assertEqual(first["card"],"21")
        m=empty(20,turn=2); h=play(m,"04",lane=0); self.assertEqual(m.power(h),5)

    def test_final_bot_event_consumes_glitch(self):
        m=empty(20,turn=2); m.s["energy"]=[6,6]; t=place(m,"10")
        play(m,"E01",target=t); self.assertEqual(t["buff"],0)
        play(m,"E01",target=t); self.assertEqual(t["buff"],1)

    def test_final_order_snapshot_and_silencing(self):
        m=empty(); u=place(m,"01"); place(m,"10",lane=1); place(m,"10",lane=2)
        m.finals(); self.assertEqual(m.s["points"][0],[1,1,1])
        m=empty(); u=place(m,"01"); m.silence(u); m.finals(); self.assertEqual(m.s["points"][0],[0,0,0])

    def test_event_target_lost_spends_cost(self):
        m=empty(); victim=place(m,"04",1); u=m.new_unit("E07",0);m.s["hand"][0].append(u)
        a=m.candidates(0,u["uid"],0)[0]; m.units(1,0).remove(victim);m.apply(0,a)
        self.assertEqual(m.s["energy"][0],4);self.assertIn(u,m.s["discard"][0])

    def test_ink_ribbon_blocks_later_events(self):
        m=empty(); play(m,"E02")
        u=m.new_unit("E15",0);m.s["hand"][0].append(u)
        self.assertFalse(m.candidates(0,u["uid"],0))

    def test_explicit_entry_effects(self):
        for cid, amount in [("12",-1),("40",-2),("44",-2),("48",-2),("E07",-2),("E20",-1)]:
            with self.subTest(cid=cid):
                m=empty(); t=place(m,"10",1); play(m,cid,target=t); self.assertEqual(t["buff"],amount)
        for cid, amount in [("03",1),("14",2),("24",2),("37",2),("39",1),("E01",1),("E04",1),("E13",3)]:
            with self.subTest(cid=cid):
                m=empty();t=place(m,"10");play(m,cid,target=t);self.assertEqual(t["buff"],amount)
        m=empty();t=place(m,"10");t["buff"]=-3;play(m,"26",target=t);self.assertEqual(t["buff"],-1)
        m=empty();play(m,"17");u=play(m,"06");self.assertEqual(u["buff"],2)
        m=empty();play(m,"28");self.assertEqual(m.units(0,0)[1]["card"],"T1")
        m=empty();play(m,"34");self.assertEqual(m.units(0,0)[1]["card"],"T2")

    def test_each_card_legal_resolution_and_limits(self):
        # Exhaust every card's legal targets against different board compositions.
        for cid, card in CARDS.items():
            if card["kind"] == "token": continue
            tested = False
            for tag_card in ["10","13","20","04","31","T3"]:
                m=empty()
                for l in range(3):
                    own=place(m,tag_card,lane=l); own["buff"]=-1
                    place(m,tag_card,1,l)
                u=m.new_unit(cid,0);m.s["hand"][0].append(u)
                for lane in range(3):
                    options=m.candidates(0,u["uid"],lane)
                    for a in options:
                        n=m.clone(False);n.apply(0,a); tested=True
                        self.assertGreaterEqual(n.s["energy"][0],0,cid)
                        for p in range(2):
                            for row in n.s["board"][p]:
                                self.assertLessEqual(len(row),4,cid)
                                for v in row:
                                    self.assertGreaterEqual(n.power(v),0,cid)
                                    self.assertTrue(-4<=v["buff"]<=4,cid)
            self.assertTrue(tested,cid)

    def test_all_bosses_and_hard_terminate(self):
        for hard in [False, True]:
            for mission in range(1,21):
                m=Match(mission,hard,mission*2030)
                while not m.s["finished"]:
                    m.commit([ai_plan(m,0,"easy"),ai_plan(m,1,"easy")])
                    while m.s["choices"]:
                        p=m.s["choices"][0]["owner"]
                        m.discard_choice(m.s["hand"][p][0]["uid"])
                self.assertEqual(len(m.s["actions"]),7 if mission==16 else 6)
                self.assertIn(m.s["winner"],[-1,0,1])

    def test_ai_does_not_observe_hidden_information(self):
        m=Match(8,seed=222)
        a=ai_plan(m)
        n=m.clone(False)
        n.s["deck"][0].reverse(); n.s["deck"][1].reverse()
        for u in n.s["hand"][0]:u["card"]="01"
        self.assertEqual(a,ai_plan(n))

    def test_determinism_after_json_roundtrip(self):
        a=Match(5,True,76)
        b=Match.restore(json.loads(json.dumps(a.s)))
        while not a.s["finished"]:
            plans=[ai_plan(a,p,"easy") for p in range(2)]
            a.commit(plans);b.commit(plans)
            while a.s["choices"]:
                p=a.s["choices"][0]["owner"];uid=a.s["hand"][p][0]["uid"]
                a.discard_choice(uid);b.discard_choice(uid)
            self.assertEqual(a.s,b.s)

    def test_seventh_turn_and_hard_event_ban(self):
        m=Match(16,True)
        for _ in range(6):m.commit([[],[]])
        self.assertEqual(m.s["energy"],[7,7]);self.assertFalse(m.s["finished"])
        u=m.new_unit("E01",0);m.s["hand"][0].append(u);place(m,"10")
        self.assertFalse(m.candidates(0,u["uid"],0));m.commit([[],[]]);self.assertTrue(m.s["finished"])

    def test_boss_entry_rules_and_once_limits(self):
        cases=[(1,True,"08",1,2,1),(2,False,"31",0,2,2),(2,True,"31",2,2,2),
               (3,False,"10",1,3,1),(4,False,"43",0,3,1),(5,False,"06",1,2,1),
               (7,False,"06",2,1,1),(7,True,"06",2,1,2),(8,False,"10",0,3,1),
               (8,True,"02",0,3,1),(10,False,"35",0,5,2),(10,True,"35",2,6,2),
               (17,False,"08",1,2,1)]
        for mission,hard,cid,lane,turn,buff in cases:
            with self.subTest(mission=mission,hard=hard):
                m=empty(mission,hard,turn);m.s["energy"]=[7,7]
                u=play(m,cid,lane=lane)
                self.assertEqual(u["buff"],buff)
                m.s["energy"][0]=7
                v=play(m,cid,lane=lane)
                self.assertEqual(v["buff"],0)
                if mission==17:self.assertTrue(u["protected"])

    def test_boss_end_round_rules(self):
        m=empty(3,True,3);a=play(m,"02",lane=1);m.end_rule();self.assertEqual(a["buff"],-1)
        for hard,amount in [(False,2),(True,1)]:
            m=empty(6,hard,3)
            for l in range(3):place(m,"10",lane=l)
            m.end_rule();self.assertEqual(m.s["points"][0],[amount,0,0])
        m=empty(9,turn=3);m.end_rule();self.assertEqual(m.units(0,1)[0]["card"],"T3")
        m=empty(9,True,3);place(m,"10",lane=1);m.end_rule();self.assertEqual(m.units(0,0)[0]["card"],"T3")
        m=empty(15,turn=4);a=place(m,"06");a["protected"]=True;place(m,"10");m.end_rule()
        self.assertEqual(a["buff"],-1);self.assertTrue(a["protected"])
        m=empty(18,turn=2);place(m,"10",lane=2);m.end_rule();self.assertEqual(m.s["points"][0][2],1)
        m=empty(18,turn=2);m.end_rule();self.assertEqual(m.s["points"],[[0,0,0],[0,0,0]])

    def test_boss_movement_shields_and_final_penalty(self):
        m=empty(11);u=place(m,"10");m.move(u,1);self.assertEqual(u["buff"],2);m.move(u,2);self.assertEqual(u["buff"],2)
        m=empty(11,True);u=place(m,"10");v=place(m,"06");m.move(u,1);m.move(u,2);m.move(v,1)
        self.assertEqual((u["buff"],v["buff"]),(1,1))
        m=empty(12,turn=4);u=place(m,"10");options=m.flight_options(0);self.assertEqual(len(options),2)
        m.apply(0,options[0]);self.assertEqual(m.s["energy"][0],4);self.assertFalse(m.flight_options(0))
        m=empty(14);u=play(m,"31",lane=2);self.assertTrue(u["protected"])
        m=empty(14,True);m.s["hand"][0].append(m.new_unit("11",0));u=play(m,"31");self.assertTrue(u["protected"])
        for hard,penalty in [(False,-2),(True,-3)]:
            m=empty(19,hard)
            for _ in range(3):place(m,"10")
            m.finals();self.assertEqual(m.s["points"][0][0],penalty)

    def test_discard_choice_precedes_next_turn_draw(self):
        m=empty(turn=3)
        m.s["deck"][0]=["02","04","06"]
        m.s["hand"][0]=[m.new_unit("E14",0)]
        a=m.candidates(0,m.s["hand"][0][0]["uid"],0)[0]
        m.commit([[a],[]])
        self.assertEqual(m.s["turn"],3)
        self.assertEqual([u["card"] for u in m.s["hand"][0]],["02","04"])
        restored=Match.restore(json.loads(json.dumps(m.s)))
        restored.discard_choice(restored.s["hand"][0][0]["uid"])
        self.assertEqual(restored.s["turn"],4)
        self.assertEqual([u["card"] for u in restored.s["hand"][0]],["04","06"])


if __name__ == "__main__": unittest.main()
