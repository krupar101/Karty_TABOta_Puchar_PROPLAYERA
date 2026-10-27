"""Audit only NORMAL story mode using the production rules and assigned decks.

Run: .venv/bin/python scripts/audit_campaign.py --games-per-duel 100 --workers 4
The player uses normal public-information heuristics on 80% of turns and the
less accurate easy heuristic on 20%. This is a reproducible proxy, not a claim
about measured human win rates. No simulation-only rule or deck substitutions.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
import hashlib
import json
import multiprocessing
from pathlib import Path
import random
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tabota.content import CARDS, ENCOUNTERS, encounter_rule, validate_deck
from tabota.engine import Match, ai_plan, campaign_difficulty, definition
from tabota.storage import Storage, new_profile


def player_plan(match, rng):
    lesson = match.tutorial_move()
    if lesson:
        return [match.candidates(0, lesson['uid'], lesson['lane'])[0]], False
    usual = ai_plan(match, 0, 'normal')
    if rng.random() < .2:
        alternative = ai_plan(match, 0, 'easy')
        return alternative, alternative != usual
    return usual, False


def invariants(match):
    s = match.s
    assert 1 <= s['turn'] <= s['maxTurns']
    for p in range(2):
        assert 0 <= s['energy'][p] <= s['turn']
        assert len(s['hand'][p]) <= 10
        cards = s['hand'][p] + s['discard'][p] + match.units(p)
        assert all(u['owner'] == p for u in cards)
        # Tokens are created by effects; all original cards must be conserved.
        actual = Counter(s['deck'][p]) + Counter(u['card'] for u in cards if definition(u)['kind'] != 'token')
        if not s['tutorial']:
            assert actual == Counter(s['initialDecks'][p]), (s['mission'], p, actual)
        for lane in range(3):
            assert len(match.units(p, lane)) <= match.capacity(lane)
            assert all(u['lane'] == lane and -4 <= u['buff'] <= 4 and match.power(u) >= 0
                       for u in match.units(p, lane))
    ids = [u['uid'] for p in range(2) for u in s['hand'][p] + s['discard'][p] + match.units(p)]
    assert len(ids) == len(set(ids))


def play(mission, seed, tutorial=False):
    match = Match(mission, hard=False, seed=seed, tutorial=tutorial)
    match.s['mode'] = 'story'
    rng = random.Random(seed ^ 0x2030AB)
    # Keep the guaranteed cheap opener; exchange up to two expensive cards.
    exchange = [] if tutorial else [u['uid'] for u in sorted(match.s['hand'][0],
                key=lambda u: definition(u)['cost'], reverse=True) if definition(u)['cost'] >= 4][:2]
    match.mulligan(0, exchange)
    match.mulligan(1, [])  # Same as Bridge.begin_match.
    trace = dict(mission=mission, seed=seed, tutorial=tutorial, exchange=exchange, turns=[])
    mistakes = 0
    for _ in range(match.s['maxTurns']):
        plan, imperfect = player_plan(match, rng)
        mistakes += imperfect
        enemy = ai_plan(match, 1, campaign_difficulty(mission, selected='normal'))
        # commit validates both sealed plans via project before actual resolution.
        entry = dict(plans=deepcopy([plan, enemy]), discards=[])
        match.commit([plan, enemy])
        while match.s['choices']:
            p = match.s['choices'][0]['owner']
            hand = match.s['hand'][p]
            assert hand, 'Unresolvable discard prompt'
            # Enemy uses exactly Bridge.finish_turn's policy.
            u = min(hand, key=lambda u: definition(u)['power']) if p == 1 else min(
                hand, key=lambda u: (definition(u)['power'], -definition(u)['cost']))
            entry['discards'].append(u['uid'])
            match.discard_choice(u['uid'])
        trace['turns'].append(entry)
        invariants(match)
        if match.s['finished']:
            break
    assert match.s['finished'] and not match.s['choices'], 'Duel did not finish'
    assert len(trace['turns']) == match.s['maxTurns']
    trace.update(winner=match.s['winner'], scores=match.scores())
    return trace, mistakes


def replay(trace):
    m = Match(trace['mission'], seed=trace['seed'], tutorial=trace['tutorial'])
    m.mulligan(0, trace['exchange'])
    m.mulligan(1, [])
    for turn in trace['turns']:
        m.commit(turn['plans'])
        for uid in turn['discards']:
            m.discard_choice(uid)
        invariants(m)
    assert m.s['finished'] and m.s['winner'] == trace['winner']
    assert m.scores() == trace['scores']
    return m


def audit_duel(args):
    mission, games, offset = args
    counts = Counter()
    win = None
    mistakes = 0
    failures = []
    for i in range(games):
        seed = mission * 100000 + offset + i
        try:
            trace, n = play(mission, seed)
            mistakes += n
            counts[str(trace['winner'])] += 1
            if trace['winner'] == 0 and win is None:
                win = trace
        except Exception as exc:
            failures.append(dict(seed=seed, error=f'{type(exc).__name__}: {exc}'))
    e = ENCOUNTERS[mission-1]
    return dict(mission=mission, opponent=e['short'], act=(mission-1)//5+1,
                enemyDifficulty=campaign_difficulty(mission), rule=encounter_rule(mission),
                playerDeck=e['storyDeck'], enemyDeck=e['enemyDeck'], games=games,
                wins=counts['0'], losses=counts['1'], draws=counts['-1'],
                winRate=counts['0']/games, imperfectTurns=mistakes,
                failures=failures, winningReplay=win)


def campaign_path(rows):
    """Replay every witness, awarding/unlocking through the real persistence API."""
    with tempfile.TemporaryDirectory(prefix='tabota-story-audit-') as directory:
        store = Storage(directory)
        store.data['slots'][0] = new_profile()
        for row in rows:
            mission = row['mission']
            assert mission == 1 or mission-1 in store.profile['completed']
            assert not validate_deck(row['playerDeck'], store.profile['unlocked'])
            assert row['winningReplay'], f'No winning witness for {mission}'
            assert replay(row['winningReplay']).s['winner'] == 0
            store.reward(mission)
        store.write('campaign.json', store.data)
        restored = Storage(directory)
        assert restored.profile['completed'] == list(range(1, 21))
        return dict(completed=restored.profile['completed'], saveReloadPassed=True,
                    note='Legal winning path with retries allowed; not a no-loss campaign run.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--games-per-duel', type=int, default=100)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--seed-offset', type=int, default=0)
    parser.add_argument('--output', default='test-artifacts/story-normal-final.json')
    args = parser.parse_args()
    if args.games_per_duel < 1 or args.workers < 1:
        parser.error('games-per-duel and workers must be positive')
    start = time.monotonic()
    jobs = [(i, args.games_per_duel, args.seed_offset) for i in range(1, 21)]
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context('spawn')) as pool:
        rows = []
        for row in pool.map(audit_duel, jobs):
            rows.append(row)
            print(f"{row['mission']:02}: {row['wins']}W {row['losses']}L {row['draws']}D; errors={len(row['failures'])}", flush=True)
    acts = []
    for act in range(1, 5):
        subset = [r for r in rows if r['act'] == act]
        wins = sum(r['wins'] for r in subset)
        games = sum(r['games'] for r in subset)
        acts.append(dict(act=act, games=games, wins=wins, winRate=wins/games))
    errors = []
    try:
        path = campaign_path(rows)
    except Exception as exc:
        path = None
        errors.append(f'{type(exc).__name__}: {exc}')
    # Optional onboarding has a documented demonstrator deck; report separately.
    tutorial, _ = play(1, 2030, tutorial=True)
    replay(tutorial)
    if tutorial['winner'] != 0:
        errors.append('Tutorial witness did not win')
    report = dict(mode='story', difficulty='normal', gamesPerDuel=args.games_per_duel,
                  seedOffset=args.seed_offset, playerPolicy='80% normal / 20% easy per turn; public information only',
                  sourceHashes={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
                                ['tabota/engine.py', 'tabota/content.py', 'Game_Design.md', 'scripts/audit_campaign.py']},
                  rows=rows, acts=acts, campaignPath=path, tutorialReplay=tutorial, errors=errors,
                  difficultyIncreasesByAct=all(a['winRate'] > b['winRate'] for a,b in zip(acts, acts[1:])),
                  seconds=round(time.monotonic()-start, 2))
    report['passed'] = not errors and all(r['wins'] and not r['failures'] for r in rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['passed', 'acts', 'difficultyIncreasesByAct', 'errors', 'seconds']}, ensure_ascii=False), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
