"""Optional hardware smoke: play the real OST, inspect PCM, verify mute.

Run with access to a desktop sound device: python scripts/check_audio.py --sfx
Unit tests do not require an audio server; this check deliberately does.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QCoreApplication, QTimer
from tabota.audio import Audio

parser = argparse.ArgumentParser()
parser.add_argument("--sfx", action="store_true", help="Also play hover, click, card, undo and ritual sounds.")
args = parser.parse_args()
app = QCoreApplication([])
audio = Audio(dict(music=True, musicVolume=.35, reduced=False, sound=True, volume=.4))
peaks = []
audio.music.spectrumChanged.connect(lambda bands: peaks.append(max(bands)))
audio.sync("menu", 1)
if args.sfx:
    assert audio.sink is not None, "No supported SFX output device"
    for i, cue in enumerate(["hover", "click", "card", "undo", "ritual"]):
        QTimer.singleShot(400+i*500, lambda cue=cue: audio.play(cue))
QTimer.singleShot(3200, app.quit)
app.exec()
for player in audio.music.players: player.stop()
assert max(peaks, default=0) > 0, "No spectrum received from M01.mp3"
audio.settings["music"] = False
audio.music.apply_volume()
assert peaks[-1] == 0, "Muting must clear the visualiser"
print(f"PASS: {len(peaks)} spectrum frames from real MP3; peak {max(peaks):.3f}; mute clears response.")
if args.sfx: print("PASS: five synthesized cues submitted to the audio sink.")
