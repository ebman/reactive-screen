# Quick Start Guide

Get the Reactive Light Show running in 5 minutes!

## Prerequisites

- Linux with X11 (not Wayland)
- Python 3.8 or higher
- Microphone access
- One or more monitors

## Installation (One Command)

```bash
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen
./install.sh
```

The installer will:
- ✅ Auto-detect your Linux distro
- ✅ Install all system dependencies
- ✅ Install Python packages
- ✅ Set up permissions
- ✅ Verify X11 compatibility

## First Run

1. **Launch the light show:**
   ```bash
   ./start-light-show.sh
   ```

2. **Choose your visual style:**
   ```
   1) Regular - Clean organic fractals with glowing orbs
   2) Smokey - Adds atmospheric fog layers
   3) Fluffy - Ultra-smooth, cloud-like visuals
   ```

3. **Allow microphone access** when prompted

4. **Play some music** and watch the magic! 🎵

## Controls

- **ESC** or **Q** - Exit the light show
- The light show automatically:
  - Hides taskbars/panels
  - Spans all monitors
  - Restores panels on exit

## What You'll See

### Regular Version
- Kaleidoscope spirals with 8-way symmetry
- Organic fractal tendrils
- Floating glowing orbs (more with high notes)
- Pulsing energy rings (on bass drops)
- Tunneling concentric rings

### Smokey Version
- Everything from Regular PLUS:
- 500 drifting smoke particles
- Ultra-smooth 12-layer fog gradients
- Atmospheric blending of all effects

### Fluffy Version
- Like Regular but with:
- 3x thicker lines
- No harsh edges anywhere
- Cloud-like soft rendering
- Perfect for dreamy vibes

## Monitor Configuration

The light show auto-detects your monitors on first run.

**To reconfigure:**
```bash
rm monitor_config.json
./start-light-show.sh
```

**Manual configuration:**
```bash
python3 monitor_config.py
```

## Troubleshooting

### Light show only on one monitor?
```bash
# Force re-detection
rm monitor_config.json
./start-light-show.sh
```

### No audio detected?
- Check microphone is connected
- Allow microphone permission when prompted
- Test: `arecord -d 5 test.wav`

### Window doesn't span?
```bash
# Check if running X11 (not Wayland)
echo $XDG_SESSION_TYPE
# Should output: x11
```

If it says "wayland":
1. Log out
2. At login screen, click gear icon
3. Select "Ubuntu on Xorg" or "GNOME on Xorg"
4. Log back in

## Next Steps

- Read the [Visual Styles Guide](Visual-Styles-Guide) for details on each version
- Check out [Customization Guide](Customization-Guide) to modify effects
- See [Performance Tuning](Performance-Tuning) if experiencing lag

---

**Enjoy your light show!** 🎉
