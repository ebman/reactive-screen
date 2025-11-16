# Installation Guide

Complete installation instructions for all supported Linux distributions.

## System Requirements

| Requirement | Details |
|------------|---------|
| **OS** | Linux with X11 display server |
| **Display** | Any number of monitors (auto-detected) |
| **Audio** | Microphone input |
| **Python** | 3.8 or higher |
| **RAM** | 2GB minimum, 4GB recommended |
| **GPU** | Any with OpenGL support |

## Supported Distributions

✅ Ubuntu / Debian / Linux Mint
✅ Fedora / RHEL / CentOS
✅ Arch / Manjaro
✅ openSUSE
✅ Most other Linux distros with X11

❌ Wayland (use X11 session instead)
❌ macOS (different window management)
❌ Windows (different window management)

## Quick Install (Recommended)

### One-Command Installation

```bash
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen
./install.sh
```

The installer will:
1. Auto-detect your Linux distribution
2. Install all system dependencies
3. Install Python packages
4. Set up file permissions
5. Verify X11 compatibility

**That's it!** Skip to [Verification](#verification).

---

## Manual Installation

If the auto-installer doesn't work, install manually for your distribution:

### Ubuntu / Debian / Mint

```bash
# Update package list
sudo apt-get update

# Install system dependencies
sudo apt-get install -y python3 python3-pip portaudio19-dev xdotool wmctrl

# Install Python packages
pip3 install --user pygame numpy pyaudio

# Clone repository
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen

# Set permissions
chmod +x start-light-show.sh monitor_config.py
```

### Fedora / RHEL / CentOS

```bash
# Install system dependencies
sudo dnf install python3 python3-pip portaudio-devel xdotool wmctrl

# Install Python packages
pip3 install --user pygame numpy pyaudio

# Clone repository
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen

# Set permissions
chmod +x start-light-show.sh monitor_config.py
```

### Arch / Manjaro

```bash
# Install system dependencies
sudo pacman -S python python-pip portaudio xdotool wmctrl

# Install Python packages
pip3 install --user pygame numpy pyaudio

# Clone repository
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen

# Set permissions
chmod +x start-light-show.sh monitor_config.py
```

### openSUSE

```bash
# Install system dependencies
sudo zypper install python3 python3-pip portaudio-devel xdotool wmctrl

# Install Python packages
pip3 install --user pygame numpy pyaudio

# Clone repository
git clone https://github.com/ebman/reactive-screen.git
cd reactive-screen

# Set permissions
chmod +x start-light-show.sh monitor_config.py
```

## Verification

### 1. Check Python Version

```bash
python3 --version
# Should be 3.8 or higher
```

### 2. Verify Python Packages

```bash
python3 -c "import pygame, numpy, pyaudio"
# Should return nothing (no errors)
```

### 3. Check System Tools

```bash
which xrandr xdotool wmctrl
# Should show paths to all three tools
```

### 4. Verify X11 (Not Wayland)

```bash
echo $XDG_SESSION_TYPE
# Should output: x11
```

If it says "wayland", see [Switching to X11](#switching-from-wayland-to-x11).

## Switching from Wayland to X11

Many modern distros use Wayland by default, but this light show requires X11.

### Ubuntu / GNOME

1. Log out of your session
2. At the login screen, click your username
3. Click the gear icon ⚙️ (bottom right)
4. Select **"Ubuntu on Xorg"** or **"GNOME on Xorg"**
5. Enter password and log in

### Fedora

1. Log out
2. Click your username at login
3. Click gear icon
4. Select **"GNOME on Xorg"**
5. Log in

### Other Desktop Environments

Look for session options at login screen to select X11/Xorg instead of Wayland.

## Troubleshooting Installation

### Issue: "pip: command not found"

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pip
```

**Fedora:**
```bash
sudo dnf install python3-pip
```

### Issue: "pyaudio installation failed"

You need portaudio development headers.

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev
```

**Fedora:**
```bash
sudo dnf install portaudio-devel
```

**Arch:**
```bash
sudo pacman -S portaudio
```

### Issue: "Permission denied" when running scripts

```bash
chmod +x start-light-show.sh monitor_config.py
```

### Issue: "xrandr: command not found"

Install X11 utilities:

**Ubuntu/Debian:**
```bash
sudo apt-get install x11-xserver-utils
```

**Fedora:**
```bash
sudo dnf install xorg-x11-server-utils
```

## Post-Installation

After installation, proceed to:
- [Quick Start](Quick-Start) - Launch your first light show
- [Monitor Configuration](Monitor-Configuration) - Configure your displays
- [Visual Styles Guide](Visual-Styles-Guide) - Choose your visual style

---

**Need more help?** Check the [Troubleshooting](Troubleshooting) page or [open an issue](https://github.com/ebman/reactive-screen/issues/new).
