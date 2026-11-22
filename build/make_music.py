#!/usr/bin/env python3
"""Generate the ad's music bed: a bright, simple pluck loop, pure stdlib.

Chord loop C - G - Am - F at 112 BPM: an arpeggiated pluck on every beat,
a soft bass on beats 1 and 3 of each bar, and a quiet pad under each chord.
Deterministic, no samples, modest level so it sits under the message.
Output: build/assets/music.wav, 34.0 s, 44.1 kHz stereo.
"""
import math
import struct
import wave
from pathlib import Path

SR = 44100
DURATION = 34.0
N = int(SR * DURATION)
BPM = 112.0
BEAT = 60.0 / BPM  # seconds per beat

# Chord tones (Hz): root, third, fifth, and the octave for the arpeggio.
CHORDS = [
    (130.81, [261.63, 329.63, 392.00, 523.25]),  # C
    (98.00, [246.94, 293.66, 392.00, 493.88]),   # G
    (110.00, [220.00, 261.63, 329.63, 440.00]),  # Am
    (87.31, [174.61, 220.00, 261.63, 349.23]),   # F
]
BAR_BEATS = 4
BAR = BAR_BEATS * BEAT

buf = [0.0] * N


def add_tone(freq, start, length, gain, decay, harmonic=0.35):
    """Add one plucked sine (fundamental + a little 2nd harmonic)."""
    i0 = int(start * SR)
    i1 = min(N, int((start + length) * SR))
    for i in range(i0, i1):
        t = (i - i0) / SR
        env = math.exp(-t / decay)
        s = math.sin(2 * math.pi * freq * t) + harmonic * math.sin(4 * math.pi * freq * t)
        buf[i] += gain * env * s


def add_pad(freq, start, length, gain):
    """Add one soft sustained tone with slow attack/release."""
    i0 = int(start * SR)
    i1 = min(N, int((start + length) * SR))
    for i in range(i0, i1):
        t = (i - i0) / SR
        attack = min(1.0, t / 0.4)
        release = min(1.0, (length - t) / 0.4)
        buf[i] += gain * attack * release * math.sin(2 * math.pi * freq * t)


bar = 0
while bar * BAR < DURATION:
    root, tones = CHORDS[bar % len(CHORDS)]
    t0 = bar * BAR
    # Pad: root + fifth, very quiet.
    add_pad(root * 2, t0, BAR, 0.045)
    add_pad(tones[2], t0, BAR, 0.035)
    # Bass on beats 1 and 3.
    add_tone(root, t0, BEAT * 1.8, 0.30, 0.55, harmonic=0.15)
    add_tone(root, t0 + 2 * BEAT, BEAT * 1.8, 0.26, 0.55, harmonic=0.15)
    # Arpeggio pluck, one note per beat, walking up then back down.
    pattern = [0, 1, 2, 3, 2, 1]
    for b in range(BAR_BEATS * 2):
        note = tones[pattern[b % len(pattern)] % len(tones)]
        add_tone(note, t0 + b * (BEAT / 2), BEAT * 0.9, 0.16, 0.30)
    bar += 1

# Gentle overall fade in/out, then normalise to a modest peak.
fade_in = int(0.3 * SR)
fade_out = int(2.0 * SR)
for i in range(N):
    if i < fade_in:
        buf[i] *= i / fade_in
    if i > N - fade_out:
        buf[i] *= (N - i) / fade_out
peak = max(abs(x) for x in buf) or 1.0
scale = 0.5 / peak
frames = b"".join(
    struct.pack("<hh", int(max(-1.0, min(1.0, x * scale)) * 32767),
                int(max(-1.0, min(1.0, x * scale)) * 32767))
    for x in buf
)
out = Path(__file__).parent / "assets" / "music.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(frames)
print(f"wrote {out} ({DURATION:.1f}s, peak {peak * scale:.2f})")
