# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q: What Linux distributions are supported?

**A:** Any Linux distro with X11 display server:
- ✅ Ubuntu, Debian, Linux Mint
- ✅ Fedora, RHEL, CentOS
- ✅ Arch, Manjaro
- ✅ openSUSE
- ✅ Most others with X11

The auto-installer (`install.sh`) detects your distro and installs the correct packages.

---

### Q: Does this work on Wayland?

**A:** No, this requires X11. Wayland has different window management that doesn't support the multi-monitor spanning we need.

**Solution:** Switch to X11 session at login (select "Xorg" option at login screen).

---

### Q: Can I run this on Windows or macOS?

**A:** No, this is Linux-only. The window management and display detection rely on X11 tools (xrandr, xdotool, wmctrl) that don't exist on Windows/macOS.

---

### Q: How do I check if I'm running X11 or Wayland?

**A:** Run this command:
```bash
echo $XDG_SESSION_TYPE
```
Should output `x11`. If it says `wayland`, switch to X11 session.

---

## Monitor Configuration

### Q: How many monitors can I use?

**A:** Any number! The system auto-detects your setup:
- 1 monitor: Works great
- 2 monitors: Spans both
- 3 monitors: Tested and working
- 4+ monitors: Should work (tested up to 3)

---

### Q: Does it work with different sized monitors?

**A:** Yes! The auto-detection finds each monitor's size and position. Works with:
- Mixed resolutions (1080p + 1440p + 4K)
- Vertical monitor arrangements
- Mixed horizontal/vertical setups

---

### Q: How do I reconfigure after changing monitors?

**A:** Delete the config and re-detect:
```bash
rm monitor_config.json
./start-light-show.sh
```

---

### Q: Can I manually configure monitors?

**A:** Yes:
```bash
python3 monitor_config.py
```
Follow the prompts to enter number of monitors, resolution, and layout.

---

## Performance

### Q: What FPS should I expect?

**A:** 60 FPS on most systems:
- Modern CPU (Intel i5/Ryzen 5 or better): 60 FPS stable
- Older hardware: 30-45 FPS
- Integrated graphics: 45-60 FPS

---

### Q: The Regular version runs fine but Smokey is laggy. Why?

**A:** Smokey renders 500 smoke particles with 12-layer gradients - much more intensive.

**Solutions:**
- Use Regular or Fluffy version instead
- Reduce `max_smoke_particles` in `light-show-smokey.py`
- Close other GPU-intensive applications

---

### Q: Can I run this on a Raspberry Pi?

**A:** Possibly on Pi 4 with reduced settings:
- Use Regular version (not Smokey)
- Reduce particle counts
- May need to lower resolution
- Expect 20-30 FPS

---

## Audio

### Q: No sound is being detected. Why?

**A:** Check these:

1. **Microphone connected?**
   ```bash
   arecord -l  # List recording devices
   ```

2. **Permission granted?**
   - Allow microphone access when prompted
   - Check system audio permissions

3. **Test recording:**
   ```bash
   arecord -d 5 test.wav
   aplay test.wav
   ```

---

### Q: The visualization doesn't react to my music player

**A:** You need to enable microphone to pick up system audio, OR:

**Better solution:** Route audio through virtual cable:
```bash
# Install PulseAudio volume control
sudo apt-get install pavucontrol

# Run pavucontrol
# Set light show to record from "Monitor of [your audio output]"
```

---

### Q: Can I use a line-in instead of microphone?

**A:** Yes! Any audio input works. Set it in your system audio settings.

---

## Visual Effects

### Q: What's the difference between Regular, Smokey, and Fluffy?

**A:**

**Regular:**
- Clean, vibrant fractals and orbs
- Sharp, defined edges
- Best performance

**Smokey:**
- Everything from Regular PLUS
- 500 atmospheric fog particles
- Ultra-smooth blending
- Higher GPU/CPU usage

**Fluffy:**
- Like Regular but ultra-smooth
- 3x thicker lines
- No harsh edges
- Cloud-like appearance
- Similar performance to Regular

---

### Q: Can I customize the colors?

**A:** Yes! Edit the Python files:
- Colors use HSV system
- Modify `hue` values to change color spectrum
- See [Customization Guide](Customization-Guide)

---

### Q: Can I add my own visual effects?

**A:** Absolutely! The code is open source and well-documented.
- See [Architecture](Architecture) for code structure
- Effects are in `draw_on_monitor()` and related methods
- Check [Contributing](Contributing) for guidelines

---

## Troubleshooting

### Q: Light show only appears on one monitor

**A:** Try these:

1. **Re-detect monitors:**
   ```bash
   rm monitor_config.json
   ./start-light-show.sh
   ```

2. **Check xrandr:**
   ```bash
   xrandr --query
   ```
   All monitors should show as "connected"

3. **Verify config:**
   ```bash
   cat monitor_config.json
   ```
   Should list all your monitors

---

### Q: Taskbar/panels still visible

**A:** The launcher should hide these automatically, but if not:

```bash
# Find panel IDs
xdotool search --class "panel"

# Hide manually (replace WINDOW_ID)
xdotool windowunmap WINDOW_ID
```

---

### Q: Window doesn't go fullscreen

**A:** Likely running on Wayland. Switch to X11:
1. Log out
2. At login, click gear icon
3. Select "X11" or "Xorg" session
4. Log in

---

### Q: Getting "ModuleNotFoundError: No module named 'pygame'"

**A:** Install Python packages:
```bash
pip3 install --user pygame numpy pyaudio
```

---

### Q: Error: "portaudio.h: No such file or directory"

**A:** Install PortAudio development headers:

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev
```

**Fedora:**
```bash
sudo dnf install portaudio-devel
```

---

## Security & Privacy

### Q: Is this safe to run?

**A:** Yes! The code is:
- ✅ Open source and auditable
- ✅ Automatically security scanned (Bandit, Safety, CodeQL)
- ✅ No network connections
- ✅ No data collection
- ✅ No hardcoded secrets

See [Security Policy](https://github.com/ebman/reactive-screen/blob/master/SECURITY.md)

---

### Q: Why does it need microphone access?

**A:** To analyze audio in real-time for the reactive visualizations. No audio is recorded or transmitted - it's only analyzed locally.

---

### Q: Does it send any data to the internet?

**A:** No. Zero network activity. Everything runs 100% locally on your machine.

---

## Advanced

### Q: Can I run multiple instances on different monitor sets?

**A:** Not recommended - they'll conflict for audio input and window management.

---

### Q: Can I record the output?

**A:** Yes! Use screen recording software like:
- OBS Studio
- SimpleScreenRecorder
- FFmpeg

Example with FFmpeg:
```bash
ffmpeg -f x11grab -s 5760x1080 -i :0.0 output.mp4
```

---

### Q: Can I use this for live performances/VJing?

**A:** Yes! It's perfect for:
- Live music visualization
- DJ sets
- Parties and events
- Art installations

Make sure to test your setup beforehand!

---

### Q: How do I contribute?

**A:** See the [Contributing](Contributing) guide. We welcome:
- Bug reports
- Feature requests
- Code contributions
- Documentation improvements

---

## Still Have Questions?

- Check other [Wiki pages](Home)
- Search [existing issues](https://github.com/ebman/reactive-screen/issues)
- [Open a new issue](https://github.com/ebman/reactive-screen/issues/new)

---

**Last Updated**: 2025-11-16
