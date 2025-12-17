from __future__ import annotations
import math, random, wave, struct
from utils.paths import project_root
from config.settings import SFX_DIR

def _write_wav(path, samples, sr=44100):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        for s in samples:
            v = max(-1.0, min(1.0, s))
            wf.writeframesraw(struct.pack("<h", int(v * 32767)))

def ensure_music_files() -> None:
    base = project_root() / SFX_DIR
    base.mkdir(parents=True, exist_ok=True)

    def make_track(seed, seconds=18, tempo=120):
        rng = random.Random(seed)
        sr = 44100
        total = int(seconds * sr)
        notes = [220, 247, 262, 294, 330, 349, 392, 440]
        beat = 60.0 / tempo
        step = beat / 2
        samples = [0.0] * total
        i = 0
        while i < total:
            f = rng.choice(notes) * rng.choice([0.5, 1, 1, 2])
            dur = rng.choice([step, step*2, step*4])
            n = int(dur * sr)
            for k in range(n):
                idx = i + k
                if idx >= total:
                    break
                tt = idx / sr
                phase = 2 * math.pi * f * tt
                sq = 1.0 if math.sin(phase) >= 0 else -1.0
                s = 0.55 * sq + 0.20 * math.sin(phase * 0.5)
                env = math.exp(-k / (0.18 * sr))
                samples[idx] += 0.28 * s * env
            i += n
        m = max(1e-6, max(abs(x) for x in samples))
        if m > 0.95:
            samples = [x * (0.95 / m) for x in samples]
        return samples

    tracks = [
        ("menu_0.wav", 123, 12, 118),
        ("menu_1.wav", 124, 12, 118),
        ("game_0.wav", 223, 14, 132),
        ("game_1.wav", 224, 14, 132),
    ]
    for name, seed, secs, tempo in tracks:
        p = base / name
        if not p.exists():
            _write_wav(p, make_track(seed, seconds=secs, tempo=tempo))
