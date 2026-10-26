"""Small, bounded PCM analyser; no extra decoder, microphone or dependencies."""
import math

BAND_COUNT = 24
FREQUENCIES = tuple(70 * (9000 / 70) ** (i / (BAND_COUNT - 1)) for i in range(BAND_COUNT))


def spectrum(samples, rate):
    """Hann-windowed Goertzel magnitudes on logarithmic frequency centres."""
    count = min(1024, len(samples))
    if count < 32 or rate <= 0:
        return [0.0] * BAND_COUNT
    window = [samples[i] * (.5 - .5 * math.cos(2 * math.pi * i / (count - 1))) for i in range(count)]
    bands = []
    for frequency in FREQUENCIES:
        if frequency >= rate / 2:
            bands.append(0.0)
            continue
        coefficient = 2 * math.cos(2 * math.pi * frequency / rate)
        a = b = 0.0
        for sample in window:
            value = sample + coefficient * a - b
            b, a = a, value
        amplitude = 4 * math.sqrt(max(0, a*a + b*b - coefficient*a*b)) / count
        bands.append(max(0.0, min(1.0, (20 * math.log10(max(1e-6, amplitude)) + 65) / 65)))
    return bands
