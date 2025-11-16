# 🌈 Reactive Multi-Monitor Light Show

An immersive, audio-reactive visualization system that spans multiple monitors with organic fractals, glowing orbs, and atmospheric effects. Built with Python, pygame, and real-time audio analysis.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Security](https://img.shields.io/badge/security-scanned-brightgreen)
![Bandit](https://img.shields.io/badge/bandit-passing-success)
![CodeQL](https://github.com/ebman/reactive-screen/workflows/Security%20Scan/badge.svg)

## ✨ Features

- **🎵 Real-time Audio Reactivity** - Responds to microphone input with FFT analysis
- **🖥️ Flexible Multi-Monitor Spanning** - Auto-detects and spans any number of monitors
- **🎨 Three Unique Versions** - Choose your visual aesthetic
- **🔮 Organic Visuals** - Fractals, kaleidoscopes, and flowing particles
- **💫 Beat-Synchronized** - Pulsing effects that follow the music
- **🌫️ Atmospheric Effects** - Optional fog and cloud-like rendering
- **⚡ 60 FPS Performance** - Smooth, hardware-accelerated graphics

## 🔒 Security

This project takes security seriously and uses automated scanning to ensure code safety:

- **🛡️ Bandit** - Python security linter (scans for common vulnerabilities)
- **🔍 CodeQL** - GitHub's semantic code analysis engine
- **📦 Safety** - Dependency vulnerability scanner
- **🐚 ShellCheck** - Bash script security analysis

All security scans run automatically on every commit and weekly. View the [Security Policy](SECURITY.md) for details.

**No hardcoded secrets** • **No malicious code** • **Safe dependencies** • **Open source & auditable**

## 🎭 Available Versions

### 1️⃣ Regular - Clean & Vibrant
Clean organic fractals with glowing orbs. Perfect for sharp, colorful visuals.

**Features:**
- Kaleidoscope spirals with 8-way symmetry
- Organic particle clouds
- Fractal branching tendrils (3 levels deep)
- Frequency-reactive tunneling rings
- Floating glowing orbs (15-55 based on treble)
- Beat-pulsing energy rings
- Subtle waveforms spanning all monitors

### 2️⃣ Smokey - Atmospheric & Dreamy
Adds dense fog layers that blend all visual elements into a dreamy atmosphere.

**Features:**
- Everything from Regular version PLUS:
- **500 smoke particles** drifting organically
- **12-layer gradient smoke** for ultra-smooth fog
- **5-20 particles/frame** spawn rate
- Particles drift from edges with organic turbulence
- 3.3-5.8 second particle lifetime
- Thicker, smoother lines (2-14px)
- Enhanced prominence and blending

### 3️⃣ Fluffy - Ultra-Smooth Cloud-Like
Like Regular but with no harsh edges - everything soft and cloud-like.

**Features:**
- All Regular effects with **3x thicker lines**
- **Multi-layer particle glow** (4 gradient layers)
- **10-segment curves** for ultra-smooth fractals
- No sharp points or thin lines anywhere
- Softer colors and diffused edges
- Perfect for gentle, dreamy vibes

## 📋 Requirements

### System Requirements
- **OS**: Linux with X11 (works on Ubuntu, Fedora, Arch, openSUSE, Mint, etc.)
  - ✅ X11 display server (required)
  - ❌ Wayland not supported (use X11 session instead)
- **Display**: Any number of monitors (auto-detected via xrandr)
- **Audio**: Microphone input
- **Python**: 3.8 or higher

### Dependencies
- `pygame` - Graphics and rendering
- `pyaudio` - Audio capture
- `numpy` - Numerical processing
- `xdotool` - Window management
- `wmctrl` - Window control
- `portaudio19-dev` - Audio backend

## 🚀 Installation

### Quick Install (Recommended)

**One command to install everything:**
```bash
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen
./install.sh
```

The install script will:
- ✅ Auto-detect your Linux distro
- ✅ Install all system dependencies
- ✅ Install Python packages
- ✅ Set up permissions
- ✅ Verify X11 compatibility

Supports: Ubuntu, Debian, Mint, Fedora, RHEL, CentOS, Arch, Manjaro, openSUSE

---

### Manual Installation

If you prefer to install manually or the auto-installer doesn't work:

#### Requirements
- **X11 display server** (not Wayland)
- **Python 3.8+**
- **xrandr, xdotool, wmctrl** (X11 tools)
- **PortAudio** (audio backend)

#### 1. Install System Dependencies

#### Ubuntu/Debian/Mint
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip portaudio19-dev xdotool wmctrl
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install python3 python3-pip portaudio-devel xdotool wmctrl
```

#### Arch/Manjaro
```bash
sudo pacman -S python python-pip portaudio xdotool wmctrl
```

#### openSUSE
```bash
sudo zypper install python3 python3-pip portaudio-devel xdotool wmctrl
```

### 2. Install Python Packages
```bash
# All distros - install via pip
pip3 install --user pygame numpy pyaudio
```

### 3. Clone/Download Project
```bash
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen
chmod +x start-light-show.sh monitor_config.py
```

### 4. Verify X11 (Not Wayland)
```bash
echo $XDG_SESSION_TYPE
# Should output: x11
# If it says "wayland", you need to switch to X11 session at login
```

## 🎮 Usage

### Quick Start
```bash
./start-light-show.sh
```

You'll see a menu:
```
=========================================
  REACTIVE LIGHT SHOW LAUNCHER
=========================================

Choose your version:
  1) Regular - Clean organic fractals with glowing orbs
  2) Smokey - Adds atmospheric fog layers for dreamy blending
  3) Fluffy - Ultra-smooth, cloud-like (no harsh edges)

Enter choice (1, 2, or 3):
```

### Direct Launch (Advanced)
```bash
# Launch Regular version
python3 light-show-triple.py

# Launch Smokey version
python3 light-show-smokey.py

# Launch Fluffy version
python3 light-show-fluffy.py

# Or use the native launcher (manages panels automatically)
./start-native-show.sh
```

### Keyboard Controls
- **ESC** or **Q** - Exit the light show
- The show will automatically restore your taskbar/panels on exit

## 🖥️ Monitor Configuration

The light show automatically detects your monitor setup using xrandr and adapts to any configuration.

### Auto-Detection
On first run, the system will:
1. Detect all connected monitors and their positions
2. Calculate total screen dimensions
3. Save configuration to `monitor_config.json`
4. Use this config for all subsequent launches

```bash
# Force re-detection (deletes saved config)
rm monitor_config.json
./start-light-show.sh

# Or manually run detection
python3 monitor_config.py
```

### Supported Layouts
- **Horizontal**: Monitors side-by-side (most common)
- **Vertical**: Monitors stacked
- **Mixed**: Any combination detected by xrandr
- **Any count**: 1, 2, 3, 4+ monitors supported

### Manual Configuration
If auto-detection fails, you can manually configure:

```bash
python3 monitor_config.py
# Follow prompts to enter:
# - Number of monitors
# - Resolution per monitor
# - Layout (horizontal/vertical)
```

### Viewing Current Config
```bash
cat monitor_config.json
# Shows:
# - Number of monitors
# - Each monitor's position and size
# - Total dimensions
# - Center points for visualization
```

## 🎨 Visual Effects Breakdown

### Core Effects (All Versions)

#### Kaleidoscope Spirals
- 4 rotating layers with different speeds
- 8-way radial symmetry
- Bass-reactive line thickness
- Blend modes: screen, lighten, color-dodge, overlay

#### Organic Particle Clouds
- Position varies with organic sine/cosine offsets
- Multiple concentric rings
- Golden ratio distribution (Regular/Fluffy) or random (Smokey)

#### Fractal Tendrils
- Recursive branching (3 levels deep)
- Organic curved segments
- Left/right branching with golden angle
- Audio-reactive length and intensity

#### Tunneling Rings
- 15 expanding concentric rings
- Frequency-mapped colors
- Bass-reactive radius

#### Waveforms
- Horizontal oscilloscope waves (top/bottom)
- Organic flowing multi-sine curves
- Edge tendrils (16 radial wisps)

### High Note Effects (Treble > 100)

#### Floating Glowing Orbs
- 15-55 orbs depending on treble intensity
- **Regular/Fluffy**: Golden ratio distribution
- **Smokey**: Completely random positions
- Multi-layer glow (3-4 layers)
- Size pulses with beat

#### Pulsing Energy Rings (Bass > 150)
- 3-8 expanding rings from monitor centers
- Synchronized to beat
- Fade over lifetime

#### Beat Impact Orbs (Bass > 200)
- 4-12 explosive orbs on heavy beats
- Triple-layer rendering (explosion/ring/core)
- Random positions

#### Screen Pulse Glow (Bass > 180)
- Full-screen color wash
- Warm, cycling hues
- Beat-synchronized opacity

### Smokey-Exclusive Effects

#### Atmospheric Smoke System
- **SmokeParticle class** with physics simulation
- Spawn locations: 40% bottom, 30% left, 30% right
- Organic turbulence using Perlin-like noise
- Alpha blending with 12-layer gradients
- Size: 60-180px, Opacity: 40-120
- Grows and fades over 3.3-5.8 second lifetime

## 🔧 Technical Details

### Architecture
```
┌─────────────────────────────────────┐
│   Audio Input (Microphone)          │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   PyAudio (44.1kHz, 1024 samples)   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   FFT Analysis (128 frequency bins) │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Bass/Mid/Treble Separation        │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Pygame Rendering (60 FPS)         │
│   - NOFRAME window (5760x1080)      │
│   - HWSURFACE (hardware accel)      │
│   - DOUBLEBUF (double buffering)    │
└─────────────────────────────────────┘
```

### Performance Optimizations
- Hardware surface rendering (`HWSURFACE`)
- Double buffering (`DOUBLEBUF`)
- 60 FPS cap with pygame clock
- Efficient particle culling (lifetime-based)
- Alpha blending with `BLEND_ALPHA_SDL2`
- Minimal CPU overhead (~15-25% on modern hardware)

### Audio Analysis
- **Sample Rate**: 44,100 Hz
- **Chunk Size**: 1024 samples
- **FFT Size**: Full chunk (1024)
- **Frequency Bins**: 128 (downsampled from 512)
- **Bass**: 0-42 bins (0-5.5 kHz)
- **Mid**: 43-85 bins (5.5-11 kHz)
- **Treble**: 86-128 bins (11-22 kHz)

### Window Management
The launcher script handles:
1. **Panel hiding** - Temporarily unmaps system panels
2. **Window positioning** - Forces absolute 0,0 position
3. **Fullscreen state** - Adds fullscreen window hints
4. **Above state** - Keeps window on top
5. **Panel restoration** - Remaps panels on exit

## 🐛 Troubleshooting

### Issue: "xrandr: command not found" or window doesn't span
**Cause**: Running on Wayland instead of X11

**Solution**:
```bash
# Check your display server
echo $XDG_SESSION_TYPE

# If it says "wayland":
# 1. Log out
# 2. At login screen, click gear icon
# 3. Select "Ubuntu on Xorg" or "GNOME on Xorg"
# 4. Log back in
```

### Issue: Show only appears on one monitor
**Solution**:
```bash
# Check your monitor setup
xrandr --query

# Force re-detection
rm monitor_config.json
./start-light-show.sh

# Manual configuration if auto-detect fails
python3 monitor_config.py
```

### Issue: No sound detected / orbs not appearing
**Solution**:
```bash
# Test microphone
arecord -d 5 test.wav

# Check PulseAudio
pavucontrol

# Grant microphone permission when browser/app asks
```

### Issue: Taskbar still visible
**Solution**:
The script should handle this automatically, but you can manually hide panels:
```bash
# Find panel window IDs
xdotool search --class "panel"

# Hide manually
xdotool windowunmap <WINDOW_ID>
```

### Issue: Performance is slow / low FPS
**Solution**:
- Close other GPU-intensive applications
- Reduce particle count in smokey version (edit `max_smoke_particles`)
- Use Regular or Fluffy version (no smoke overhead)
- Check GPU drivers are installed

### Issue: "ModuleNotFoundError: No module named 'pygame'"
**Solution**:
```bash
pip3 install --user pygame
# or
sudo apt-get install python3-pygame
```

## 📁 Project Structure

```
reactive-screen/
├── README.md                    # This file
├── SECURITY.md                  # Security policy and practices
├── requirements.txt             # Python dependencies
├── install.sh                   # Auto-installer for all distros
├── monitor_config.py            # Monitor detection system
├── start-light-show.sh          # Main launcher (menu)
├── light-show-triple.py         # Regular version
├── light-show-smokey.py         # Smokey version
├── light-show-fluffy.py         # Fluffy version
├── monitor_config.json          # Generated monitor config (gitignored)
├── .github/
│   └── workflows/
│       └── security-scan.yml    # Automated security scanning
├── light-show.html              # Original HTML version (legacy)
└── light-show-v1.html           # HTML variant (legacy)
```

## 🎯 Customization

### Adjusting Monitor Configuration
Edit `start-light-show.sh`:
```bash
TOTAL_WIDTH=5760   # Change to your total width
TOTAL_HEIGHT=1080  # Change to your total height
```

Edit Python files (`__init__` method):
```python
self.monitor_width = 1920   # Single monitor width
self.monitor_height = 1080  # Single monitor height
self.num_monitors = 3       # Number of monitors
```

### Adjusting Smoke Density (Smokey Version)
Edit `light-show-smokey.py`:
```python
self.max_smoke_particles = 500  # Increase for more smoke
spawn_rate = int(5 + (average / 255) * 15)  # Adjust spawn rate
```

### Adjusting Visual Intensity
All versions have intensity multipliers you can adjust:
```python
# Particle sizes
base_size = 8 + intensity * 25  # Change multiplier

# Line widths
width = max(3, int(5 + (bass / 255) * 12))  # Adjust thickness

# Orb count
num_orbs = int(intensity * 40) + 15  # Change range
```

## 🤝 Contributing

Feel free to fork and customize! Some ideas:
- Add more visual effects
- Support for different monitor configurations
- MIDI input support
- Save/load presets
- Audio file input (instead of microphone)
- Additional blend modes

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Built with Python, Pygame, and PyAudio
- Inspired by classic music visualizers and VJ software
- Audio analysis using NumPy FFT
- Window management via xdotool and wmctrl

## 📧 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed
3. Ensure your monitor setup matches the configuration
4. Test microphone input separately

---

**Enjoy the show! 🎵✨🌈**

*Created with Claude Code*
