# Generate the cinematic cut's audio bed: a low sub-drone with a slow swell and
# pitch-drop thumps on the cuts and slams. Replaces the bundled music track.
# Deterministic (seeded noise). Output: assets/drone.wav, mono 44.1 kHz.
import numpy as np, wave
SR = 44100
DUR = 35.0
t = np.arange(int(SR * DUR)) / SR
rng = np.random.default_rng(7)

def env(points):
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)

# drone: detuned sub pair + soft octave, slow amplitude LFO
drone = (np.sin(2*np.pi*55.0*t) + np.sin(2*np.pi*55.35*t)) * 0.5
drone += 0.35 * np.sin(2*np.pi*110.0*t + 0.4) * (0.6 + 0.4*np.sin(2*np.pi*0.09*t))
drone *= 0.85 + 0.15*np.sin(2*np.pi*0.13*t)
# air: brown noise, low-passed by cumulative sum, very quiet
white = rng.standard_normal(len(t))
brown = np.cumsum(white); brown -= np.convolve(brown, np.ones(2000)/2000, mode="same")
brown /= np.max(np.abs(brown))
# swell through the run scene (9.0 → 16.5), drop on the cut, quiet under the outro
swell = env([(0,0.0),(5.5,0.0),(17.4,1.0),(17.5,0.0),(35.0,0.0)])
master = env([(0,0.0),(1.5,1.0),(33.9,1.0),(35.0,0.0)])
bed = drone * (0.16 + 0.10*swell) + brown * (0.03 + 0.05*swell)

# thumps: pitch-drop sine 90 → 38 Hz over 0.45 s with a fast attack
def thump(at, gain):
    n = int(0.55 * SR)
    tt = np.arange(n) / SR
    f = 38 + (90 - 38) * np.exp(-tt * 9)
    phase = 2*np.pi*np.cumsum(f)/SR
    e = np.exp(-tt * 6.5) * (1 - np.exp(-tt * 400))
    s = np.sin(phase) * e * gain
    i = int(at * SR)
    bed[i:i+n] += s[:len(bed)-i]

for at, g in [(0.25,0.6),(1.15,0.45),(2.7,0.7),(5.5,0.7),(8.0,0.35),(10.5,0.7),(14.0,0.7),
              (17.5,0.7),(17.9,0.9),(21.0,0.8),(24.5,0.8),(27.5,0.75),(28.0,0.4),(28.5,0.4),(29.0,0.4),(29.5,0.45),
              (31.5,0.8),(31.9,0.9),(32.9,0.8),(33.5,0.7)]:
    thump(at, g)

out = bed * master
out = out / max(1.0, np.max(np.abs(out)) / 0.85)
with wave.open("assets/drone.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("wrote assets/drone.wav", len(out)/SR, "s; peak", round(float(np.max(np.abs(out))),3), "rms", round(float(np.sqrt(np.mean(out**2))),4))
