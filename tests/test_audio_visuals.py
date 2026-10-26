"""PCM analysis, settings gating and independent audio notifications."""
import math
import struct
import tempfile
import unittest
from unittest.mock import Mock, patch

from PySide6.QtCore import QCoreApplication, QByteArray
from PySide6.QtMultimedia import QAudioBuffer, QAudioFormat
from tabota.audio import MusicDirector, Audio, CUES, synthesize, SFX_PEAK, MUSIC_GAIN
from tabota.bridge import Bridge
from tabota.spectrum import spectrum, FREQUENCIES


class AudioVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QCoreApplication.instance() or QCoreApplication([])

    def test_silence_and_frequency_separation(self):
        self.assertEqual(spectrum([0.0] * 1024, 22050), [0.0] * 24)
        for index in (6, 12, 20):
            samples = [.3 * math.sin(2 * math.pi * FREQUENCIES[index] * i / 22050) for i in range(1024)]
            bands = spectrum(samples, 22050)
            self.assertEqual(max(range(24), key=bands.__getitem__), index)
            self.assertTrue(all(0 <= x <= 1 for x in bands))

    def test_pcm_formats_stereo_crossfade_and_mute(self):
        # Hardware playback is covered by the opt-in smoke check; unit tests
        # must run without a PulseAudio socket or an attached sound device.
        with patch("tabota.audio.QMediaPlayer"), patch("tabota.audio.QAudioOutput"):
            director = MusicDirector(dict(music=True, musicVolume=.5, reduced=False))
        received = []
        director.spectrumChanged.connect(received.append)
        for form, code, scale, offset in [(QAudioFormat.UInt8, "B", 100, 128),
                                          (QAudioFormat.Int16, "h", 20000, 0),
                                          (QAudioFormat.Int32, "i", 1000000000, 0),
                                          (QAudioFormat.Float, "f", .6, 0)]:
            fmt = QAudioFormat()
            fmt.setSampleRate(22050)
            fmt.setChannelCount(2)
            fmt.setSampleFormat(form)
            values = []
            for i in range(1024):
                value = scale * math.sin(2 * math.pi * FREQUENCIES[12] * i / 22050)
                values.extend([offset+value, offset-value])
            if code != "f": values = [int(x) for x in values]
            buffer = QAudioBuffer(QByteArray(struct.pack("=" + code*len(values), *values)), fmt)
            director.sample_times = [0, 0]
            director.analyse(0, buffer)
            self.assertEqual(max(range(24), key=director.bands[0].__getitem__), 12)
        director.levels = [.6, .4]
        director.publish_spectrum()
        self.assertGreater(received[-1][12], 0)
        director.settings["music"] = False
        director.apply_volume()
        self.assertEqual(received[-1], [0.0]*24)
        self.assertFalse(director.visual_timer.isActive())
        director.settings.update(music=True, reduced=True)
        director.apply_volume()
        self.assertEqual(received[-1], [0.0]*24)
        director.settings.update(reduced=False, musicVolume=0)
        director.apply_volume()
        self.assertFalse(director.visual_timer.isActive())

    def test_sfx_are_cached_pcm_and_hover_never_cuts_placement(self):
        for kind in CUES:
            data = synthesize(kind)
            samples = struct.unpack("<" + "h"*(len(data)//2), data)
            self.assertGreater(max(samples), 0)
            self.assertLessEqual(max(abs(v) for v in samples), SFX_PEAK)
            self.assertEqual(samples[0], 0)
        audio = Audio.__new__(Audio)
        audio.settings = dict(sound=True, volume=.4)
        audio.cues = {k: synthesize(k) for k in CUES}
        audio.sink = Mock()
        audio.last_sound = audio.hover_until = 0
        audio.last_kind = ""
        audio.play("card")
        audio.play("hover")
        audio.play("click")
        self.assertEqual(audio.sink.start.call_count, 1)
        audio.settings["sound"] = False
        audio.play("ritual")
        self.assertEqual(audio.sink.start.call_count, 1)

    def test_sfx_music_mix_has_headroom_and_independent_sliders(self):
        director = MusicDirector.__new__(MusicDirector)
        director.settings = dict(music=True, musicVolume=.2, volume=1.0)
        director.duck = 1.0
        self.assertAlmostEqual(director.gain(), .2 * MUSIC_GAIN)
        pcm = synthesize('card')
        values = struct.unpack('<' + 'h' * (len(pcm)//2), pcm)
        peak = max(abs(x) for x in values) / 32768
        self.assertGreater(peak, director.gain() * 4)
        self.assertLess(peak, 1)
        director.settings['volume'] = 0
        self.assertAlmostEqual(director.gain(), .2 * MUSIC_GAIN)
        director.settings['musicVolume'] = 0
        self.assertEqual(director.gain(), 0)

    def test_spectrum_does_not_refresh_game_or_save(self):
        with tempfile.TemporaryDirectory() as directory:
            api = Bridge(directory)
            api.changed.connect(lambda: self.fail("Music refreshed game state"))
            api.boardChanged.connect(lambda: self.fail("Music refreshed board"))
            api.store.write = Mock(side_effect=AssertionError("Music wrote a save"))
            api.updateSpectrum([.2]*24)
            self.assertEqual(api.musicSpectrum, [.2]*24)


if __name__ == "__main__": unittest.main()
