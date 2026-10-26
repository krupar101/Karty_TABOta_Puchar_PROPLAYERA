"""Deterministic mapping between UI screens and the provided original OST."""
from pathlib import Path
from .content import ROOT

MUSIC_DIR = ROOT / "music"


def soundtrack_for(screen, mission=1):
    """One theme per context; pause shares its duel track, result returns to map."""
    if screen in ("battle", "pause"):
        return f"Stage{max(1, min(20, int(mission))):02}.mp3"
    if screen in ("map", "briefing", "result", "ending"):
        return "M02.mp3"
    if screen in ("collection", "builder"):
        return "M03.mp3"
    if screen in ("fortune", "reading", "history"):
        return "M04.mp3"
    return "M01.mp3"


def soundtrack_path(screen, mission=1):
    return MUSIC_DIR / soundtrack_for(screen, mission)
