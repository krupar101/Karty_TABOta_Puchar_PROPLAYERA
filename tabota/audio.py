"""Crossfading OST with independent synth SFX and supplied result stingers."""
import math
import struct
from time import monotonic
from PySide6.QtCore import QByteArray, QBuffer, QIODevice, QTimer, QUrl, QObject, Signal
from .music import MUSIC_DIR, soundtrack_for
from .spectrum import spectrum, BAND_COUNT
from PySide6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices, QAudioOutput, QMediaPlayer, QAudioBufferOutput


SFX_PEAK = 24000  # Headroom below signed 16-bit clipping, +13.6 dB vs the old mix.
MUSIC_GAIN = .35  # Master trim; independent of the user music slider.

CUES = {"hover": ([920], .035, .22), "click": ([720], .055, .55),
        "card": ([210, 330], .13, .8), "select": ([540, 660], .075, .45),
        "undo": ([520, 350], .10, .5), "shuffle": ([240, 380, 290], .20, .6),
        "turn": ([330, 495], .18, .55), "error": ([190, 160], .14, .45),
        "ritual": ([330, 495, 660, 990], .38, .7),
        "reveal": ([330, 495, 660], .32, .7), "start": ([220, 330, 440], .35, .7),
        "draw": ([440, 550, 440], .4, .65),
        "win": ([440, 550, 660, 880], .65, .8), "lose": ([330, 294, 220], .4, .7)}


def synthesize(kind):
    frequencies, duration, gain = CUES[kind]
    samples = []
    for i in range(int(22050 * duration)):
        t = i / 22050
        part = min(len(frequencies)-1, int(t/duration*len(frequencies)))
        f = frequencies[part]
        envelope = min(1, t/.008) * (1-t/duration)**1.8
        value = (.8*math.sin(2*math.pi*f*t) + .2*math.sin(2*math.pi*2*f*t)) * envelope
        samples.append(struct.pack("<h", int(value*SFX_PEAK*gain)))
    return b"".join(samples)


class Audio:
    def __init__(self, settings):
        self.settings = settings
        self.sink = None
        self.buffer = None
        self.cues = {kind: synthesize(kind) for kind in CUES}
        self.last_sound = 0.0
        self.last_kind = ""
        self.hover_until = 0.0
        self.music = MusicDirector(self.settings)
        self.sting = QMediaPlayer()
        self.sting_output = QAudioOutput()
        self.sting.setAudioOutput(self.sting_output)
        self.sting.playbackStateChanged.connect(
            lambda state: self.music.set_duck(state == QMediaPlayer.PlayingState)
        )
        device = QMediaDevices.defaultAudioOutput()
        if device.isNull(): return
        fmt = QAudioFormat()
        fmt.setSampleRate(22050)
        fmt.setChannelCount(1)
        fmt.setSampleFormat(QAudioFormat.Int16)
        if device.isFormatSupported(fmt): self.sink = QAudioSink(device, fmt)

    def sync(self, screen, mission):
        self.music.change(screen, mission)

    def play(self, kind):
        if not self.settings.get("sound", True): return
        if kind not in CUES: return
        now = monotonic()
        # Hover never interrupts a card/ritual, and a button's generic click
        # cannot replace the more specific sound emitted by its action.
        if kind == "hover" and now < self.hover_until: return
        if kind == "click" and self.last_kind != "hover" and now - self.last_sound < .08: return
        self.last_sound = now
        self.last_kind = kind
        self.hover_until = now + max(.10, CUES[kind][1])
        stings = {"win": "X02.mp3", "lose": "X03.mp3"}
        if kind in stings and (MUSIC_DIR/stings[kind]).is_file():
            self.sting.stop()
            self.sting.setSource(QUrl.fromLocalFile(str(MUSIC_DIR/stings[kind])))
            self.sting_output.setVolume(float(self.settings.get("volume", .4)))
            self.sting.play()
            return
        if not self.sink: return
        self.sink.stop()
        self.buffer = QBuffer()
        self.buffer.setData(QByteArray(self.cues[kind]))
        self.buffer.open(QIODevice.ReadOnly)
        self.sink.setVolume(float(self.settings.get("volume", .4)))
        self.sink.start(self.buffer)


class MusicDirector(QObject):
    """Two decoders allow actual overlapping fades, not stop-and-restart gaps.

    Uses one frame timer for the entire soundtrack. Consecutive navigation during
    a fade starts from the current levels, preventing jumps and leaked players.
    """
    spectrumChanged = Signal(list)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.players = [QMediaPlayer(), QMediaPlayer()]
        self.outputs = [QAudioOutput(), QAudioOutput()]
        for player, output in zip(self.players, self.outputs):
            player.setAudioOutput(output)
            player.setLoops(QMediaPlayer.Infinite)
            output.setVolume(0.0)
        self.active = -1
        self.track = None
        self.fade_ms = 0
        self.elapsed_ms = 0
        self.starts = [0.0, 0.0]
        self.targets = [0.0, 0.0]
        self.levels = [0.0, 0.0]
        self.timer = QTimer()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.step)
        self.duck = 1.0
        self.duck_target = 1.0
        self.duck_timer = QTimer()
        self.duck_timer.setInterval(40)
        self.duck_timer.timeout.connect(self.step_duck)
        self.bands = [[0.0] * BAND_COUNT for _ in range(2)]
        self.sample_times = [0.0, 0.0]
        self.taps = [QAudioBufferOutput(self), QAudioBufferOutput(self)]
        for i, (player, tap) in enumerate(zip(self.players, self.taps)):
            player.setAudioBufferOutput(tap)
            tap.audioBufferReceived.connect(lambda buffer, i=i: self.analyse(i, buffer))
        self.visual_timer = QTimer(self)
        self.visual_timer.setInterval(50)
        self.visual_timer.timeout.connect(self.publish_spectrum)

    def visual_enabled(self):
        return self.gain() > 0 and not self.settings.get("reduced", False)

    def analyse(self, index, buffer):
        now = monotonic()
        if not self.visual_enabled() or now - self.sample_times[index] < .045:
            return
        if not buffer.isValid():
            self.bands[index] = [0.0] * BAND_COUNT
            return
        fmt = buffer.format()
        formats = {QAudioFormat.UInt8: ("B", 128, 128), QAudioFormat.Int16: ("h", 32768, 0),
                   QAudioFormat.Int32: ("i", 2147483648, 0), QAudioFormat.Float: ("f", 1, 0)}
        if fmt.sampleFormat() not in formats or fmt.channelCount() < 1:
            return
        code, scale, offset = formats[fmt.sampleFormat()]
        data = buffer.constData().cast(code)
        channels = fmt.channelCount()
        count = min(1024, buffer.frameCount())
        # Analyse the loudest channel in this block; averaging antiphase stereo
        # can cancel the music, while switching channels per sample adds noise.
        channel = max(range(channels), key=lambda c: sum(abs(data[i*channels+c]-offset) for i in range(0, count, 8)))
        samples = [data[i*channels+channel] for i in range(count)]
        self.bands[index] = spectrum([(v-offset)/scale for v in samples], fmt.sampleRate())
        self.sample_times[index] = now

    def publish_spectrum(self):
        now = monotonic()
        # Master audio trim must not reduce the existing visual motion.
        weights = [self.levels[i] * (self.gain() / MUSIC_GAIN) if now-self.sample_times[i] < .25 else 0 for i in range(2)]
        self.spectrumChanged.emit([min(1.0, sum(self.bands[i][b]*weights[i] for i in range(2))) for b in range(BAND_COUNT)])

    def set_duck(self, active):
        """Let one-shot win/lose audio take precedence over the campaign bed."""
        self.duck_target = .24 if active else 1.0
        if not self.duck_timer.isActive():
            self.duck_timer.start()

    def step_duck(self):
        self.duck += (self.duck_target-self.duck) * .2
        if abs(self.duck-self.duck_target) < .01:
            self.duck = self.duck_target
            self.duck_timer.stop()
        self.apply_volume()

    def gain(self):
        if not self.settings.get("music", True):
            return 0.0
        return min(1.0, max(0.0, float(self.settings.get("musicVolume", .35)))) * MUSIC_GAIN * self.duck

    def change(self, screen, mission):
        desired = soundtrack_for(screen, mission)
        if desired != self.track:
            path = MUSIC_DIR / desired
            if not path.is_file():
                return  # Missing optional asset must never prevent the game starting.
            if self.active < 0:
                incoming = 0
            else:
                # Preserve the louder outgoing stream on rapid screen changes.
                incoming = min(range(2), key=lambda i: self.levels[i])
                self.players[incoming].stop()
            self.players[incoming].setSource(QUrl.fromLocalFile(str(path)))
            self.players[incoming].play()
            self.track = desired
            self.active = incoming
            self.starts = self.levels[:]
            self.targets = [0.0, 0.0]
            self.targets[incoming] = 1.0
            self.elapsed_ms = 0
            self.fade_ms = 320 if screen == "result" else 1400
            self.timer.start()
        # Updates from Settings reach a running track immediately, even mid-fade.
        self.apply_volume()

    def apply_volume(self):
        gain = self.gain()
        for i, out in enumerate(self.outputs):
            out.setVolume(gain * self.levels[i])
        if self.visual_enabled():
            if not self.visual_timer.isActive(): self.visual_timer.start()
        else:
            self.visual_timer.stop()
            self.spectrumChanged.emit([0.0] * BAND_COUNT)

    def step(self):
        self.elapsed_ms += self.timer.interval()
        t = min(1.0, self.elapsed_ms / max(1, self.fade_ms))
        # Cosine ease keeps audio levels free of abrupt slope changes.
        import math
        eased = (1-math.cos(math.pi*t))/2
        self.levels = [a+(b-a)*eased for a,b in zip(self.starts,self.targets)]
        self.apply_volume()
        if t >= 1.0:
            self.timer.stop()
            for i, player in enumerate(self.players):
                if i != self.active:
                    player.stop()
                    self.levels[i] = 0.0
            self.apply_volume()
