"""Reproducible AI-vs-AI smoke/balance report across all encounter rules."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tabota.engine import Match, ai_plan, campaign_difficulty, draft_offer, auto_deck
from tabota.content import CARDS, ENCOUNTERS

parser=argparse.ArgumentParser()
parser.add_argument("--games",type=int,default=100)
parser.add_argument("--difficulty",choices=["easy","normal","hard"],default="normal")
parser.add_argument("--output",default="test-artifacts/simulation.json")
parser.add_argument("--mode", choices=["rules", "campaign"], default="rules",
                    help="campaign uses the actual enemy levels and full-collection HARD drafts")
parser.add_argument("--missions", type=int, nargs="+", default=list(range(1, 21)))
parser.add_argument("--seed-offset", type=int, default=0)
args=parser.parse_args()
rows=[]
start=time.perf_counter()
for mission in args.missions:
    for hard in [False,True]:
        results=Counter()
        winning_seed = None
        count = max(1, args.games // (2 * len(args.missions)))
        for i in range(count):
            seed = mission*100000 + args.seed_offset + i
            decks = None
            enemy_level = args.difficulty
            if args.mode == "campaign":
                enemy_level = campaign_difficulty(mission, hard)
                if hard:
                    pool = [c for c in CARDS if CARDS[c]["kind"] != "token"]
                    decks = [auto_deck(draft_offer(pool, seed)), ENCOUNTERS[mission-1]["enemyDeck"]]
            m=Match(mission,hard,seed=seed,decks=decks)
            while not m.s["finished"]:
                plans=[ai_plan(m,0,args.difficulty), ai_plan(m,1,enemy_level)]
                m.commit(plans)
                while m.s["choices"]:
                    p=m.s["choices"][0]["owner"]
                    m.discard_choice(min(m.s["hand"][p],key=lambda u: u["card"])["uid"])
                for p in range(2):
                    assert 0<=m.s["energy"][p]<=m.s["turn"]
                    assert len(m.s["hand"][p])<=10
                    for lane in range(3):
                        assert len(m.units(p,lane))<=m.capacity(lane)
                        assert all(-4<=u["buff"]<=4 and m.power(u)>=0 for u in m.units(p,lane))
            results[str(m.s["winner"])]+=1
            if m.s["winner"] == 0 and winning_seed is None: winning_seed = seed
        rows.append(dict(mission=mission,hard=hard,results=dict(results), winningSeed=winning_seed,
                         winRate=round(results['0']/count, 3)))
report=dict(games=sum(sum(row["results"].values()) for row in rows),difficulty=args.difficulty,
            mode=args.mode, seedOffset=args.seed_offset,
            seconds=round(time.perf_counter()-start,3),rows=rows)
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"{report['games']} completed games, all invariants passed, {report['seconds']} s. Report: {path}")
