# Visual Effects Reference

Complete reference of all visual effects in the Reactive Light Show.

## Core Effects (All Versions)

### 🌀 Kaleidoscope Spirals

**What it is:** Rotating spiral patterns with 8-way radial symmetry

**How it works:**
- 4 rotating layers at different speeds
- Each layer rotates independently (some clockwise, some counter-clockwise)
- Line thickness responds to bass intensity
- Colors cycle through HSV spectrum

**Audio reactivity:**
- Bass → Line thickness (3-11px)
- Average volume → Global pulse multiplier
- Time → Rotation speed and color cycling

**Code location:** `draw_on_monitor()` lines 133-170

---

### ✨ Organic Particle Clouds

**What it is:** Concentric rings of glowing particles with organic movement

**How it works:**
- 3 concentric rings at different radii
- Each particle has organic sine/cosine offset
- Multi-layer glow rendering for soft appearance

**Audio reactivity:**
- Frequency data → Particle positions radially
- Bass → Radius expansion
- Average → Glow intensity

**Positioning:**
- Regular/Fluffy: Golden ratio distribution
- Smokey: Completely random positions

**Code location:** `draw_on_monitor()` lines 172-198

---

### 🌿 Fractal Tendrils

**What it is:** Recursive branching structures with organic curves

**How it works:**
- 8 main tendrils around each monitor center
- Each branches recursively (3 levels deep)
- Branches curve organically using sine waves
- Left/right splits at each level

**Audio reactivity:**
- Bass/Mid/Treble → Different tendril lengths
- Global pulse → Overall size
- Time → Organic curve animation

**Recursion:**
- Depth 3: Main branch
- Depth 2: 2 sub-branches
- Depth 1: 4 leaf branches
- Each branch 65% length of parent

**Code location:** `draw_fractal_tendril()` lines 236-301

---

### ⭕ Tunneling Rings

**What it is:** 15 expanding concentric rings creating tunnel effect

**How it works:**
- Rings expand from center outward
- Wraps around (ring 15 becomes ring 1)
- Each ring mapped to different frequency

**Audio reactivity:**
- Per-ring frequency → Color and line thickness
- Bass → Global radius multiplier
- Time → Animation speed

**Size:** Can extend 1.2x beyond monitor boundaries for overlap

**Code location:** `draw_on_monitor()` lines 224-240

---

## High Note Effects (Treble > 100)

### 💫 Floating Glowing Orbs

**Trigger:** Treble frequency > 100

**What it is:** 15-55 glowing orbs that pulse and float

**How it works:**
- Number of orbs scales with treble intensity
- 3-layer rendering (outer glow, middle, core)
- Floating motion using sine/cosine

**Audio reactivity:**
- Treble intensity → Number of orbs (15-55)
- Bass → Orb size pulsing
- Time → Floating movement

**Rendering:**
- Outer layer: 30-80 alpha, 2x orb size
- Middle layer: 80-180 alpha, 1.2x orb size
- Core: 150-255 alpha, 1x orb size

**Code location:** `draw_high_note_effects()` lines 384-426

---

### 💥 Pulsing Energy Rings

**Trigger:** Bass > 150

**What it is:** 3-8 expanding rings emanating from monitor centers

**How it works:**
- Rings expand and fade over time
- Emit from each monitor center cyclically
- Transparent rendering with alpha fade

**Audio reactivity:**
- Bass intensity → Number of rings (3-8)
- Bass → Expansion speed
- Phase → Alpha fade (bright to transparent)

**Code location:** `draw_high_note_effects()` lines 436-453

---

### 🎆 Beat Impact Orbs

**Trigger:** Bass > 200

**What it is:** 4-12 explosive orbs on heavy beats

**How it works:**
- Random positions across all screens
- 3-layer explosive rendering
- Large pulsing size

**Audio reactivity:**
- Bass intensity → Number of orbs (4-12)
- Beat pulse → Size multiplier
- Time → Color cycling

**Rendering:**
- Outer explosion: 40 alpha, 2x size
- Middle ring: 120 alpha, 1.3x size
- Bright core: 200 alpha, 1x size

**Code location:** `draw_high_note_effects()` lines 456-482

---

### 🌟 Screen Pulse Glow

**Trigger:** Bass > 180

**What it is:** Full-screen warm color wash on beats

**How it works:**
- Semi-transparent colored overlay
- Pulsesynchronized with bass

**Audio reactivity:**
- Bass intensity → Opacity (0-40%)
- Beat pulse → Brightness multiplier
- Time → Hue cycling

**Code location:** `draw_high_note_effects()` lines 485-494

---

## Smokey-Exclusive Effects

### 🌫️ Atmospheric Fog

**What it is:** 500 drifting smoke particles with organic movement

**Particle properties:**
- Size: 60-180px
- Opacity: 40-120 (fades over lifetime)
- Lifetime: 3.3-5.8 seconds
- Velocity: Slow drift with turbulence

**Rendering:**
- 12-layer gradient for ultra-smooth fog
- Each layer progressively darker/smaller
- Alpha blending for transparency

**Spawn rate:**
- Base: 5 particles/frame
- Audio-reactive: Up to 20 particles/frame
- Spawns from screen edges

**Physics:**
- Organic turbulence using sine/cosine
- Velocity affected by time
- Particles grow and fade over life

**Code location:**
- Particle class: lines 21-63
- Rendering: `draw_smoke_particles()` lines 495-570

---

## Fluffy-Exclusive Modifications

### ☁️ Ultra-Smooth Rendering

**What it is:** All Regular effects with enhanced smoothness

**Modifications:**
- **All lines 3x thicker** (prevents any thin/sharp edges)
- **Particle glow** uses 4 gradient layers instead of 3
- **Fractal curves** use 10 segments instead of 5
- **No sharp points** anywhere in rendering

**Code differences:**
- Line widths: `max(3, ...)` instead of `max(1, ...)`
- Curve segments: `num_segments = 10`
- Multi-layer glow on all particles

---

## Global Effects (All Versions)

### 🌫️ Trailing Effect

**What it is:** Fade overlay creating motion blur trails

**How it works:**
- Semi-transparent black overlay each frame
- Fade amount adjusts with bass

**Audio reactivity:**
- Bass → Less fade (longer trails on bass)
- Standard: 15% fade per frame
- Bass active: 5-15% fade (preserves trails longer)

**Code location:** Main loop, lines 519-523

---

### ⚡ Bass Flash

**Trigger:** Bass > 230

**What it is:** Brief white flash on massive bass hits

**How it works:**
- Full-screen white overlay
- Opacity scales with bass intensity above 230
- Maximum 76 alpha (30%)

**Code location:** Main loop, lines 526-530

---

## Audio Analysis

### Frequency Bands

| Band | Range | Use |
|------|-------|-----|
| **Bass** | 0-5.5 kHz (bins 0-42) | Size, pulse, impacts |
| **Mid** | 5.5-11 kHz (bins 43-85) | Moderate effects |
| **Treble** | 11-22 kHz (bins 86-128) | High notes, orbs |
| **Average** | All frequencies | Global intensity |

### FFT Configuration

- Sample rate: 44,100 Hz
- Chunk size: 1024 samples
- FFT bins: 128 (downsampled from 512)
- Update rate: 60 FPS

---

## Color System

### HSV Color Cycling

All effects use HSV color space for smooth color transitions:

```python
hue = (base_hue + time * speed + offset) % 360
color = hsv_to_rgb(hue, saturation, value)
```

**Typical values:**
- Hue: 0-360 (cycles through spectrum)
- Saturation: 0.4-1.0 (varies by effect)
- Value: 0.2-0.8 (varies by intensity)

---

## Performance Characteristics

| Effect | CPU Impact | GPU Impact |
|--------|-----------|-----------|
| Kaleidoscope | Low | Medium |
| Particles | Low | Low |
| Fractals | Medium | Low |
| Tunneling Rings | Low | Low |
| Orbs (high notes) | Medium | Medium |
| Smoke (500 particles) | High | Medium |

**Overall:** 15-25% CPU on modern hardware at 60 FPS

---

**See also:**
- [Audio Analysis](Audio-Analysis) - Deep dive into FFT and frequency detection
- [Customization Guide](Customization-Guide) - Modify these effects
- [Performance Tuning](Performance-Tuning) - Optimize for your system
