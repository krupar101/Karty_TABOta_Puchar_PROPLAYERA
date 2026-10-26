"""100 deterministic normal-campaign games, plus opponent collection audit."""
import sys,json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tabota.engine import Match,ai_plan,campaign_difficulty
from tabota.content import ENCOUNTERS,STARTER
rows=[];unlocked=set(STARTER)
for mission in range(1,21):
 counts=Counter()
 for seed in range(5):
  m=Match(mission,seed=mission*100000+seed)
  while not m.s['finished']:
   m.commit([ai_plan(m,0,'normal'),ai_plan(m,1,campaign_difficulty(mission))])
   while m.s['choices']:
    p=m.s['choices'][0]['owner'];m.discard_choice(m.s['hand'][p][0]['uid'])
  counts[str(m.s['winner'])]+=1
 e=ENCOUNTERS[mission-1];rows.append(dict(mission=mission,level=campaign_difficulty(mission),results=dict(counts),enemyLockedCards=sorted(set(e['enemyDeck'])-unlocked)))
 unlocked.update(e['unlocks'])
 print(mission,dict(counts),flush=True)
output = Path(__file__).resolve().parents[1] / 'test-artifacts/balance-fixes.json'
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(rows, indent=2), encoding='utf-8')
