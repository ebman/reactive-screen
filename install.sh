#!/bin/bash
# Automatic dependency installer for Reactive Multi-Monitor Light Show
# Detects Linux distro and installs required packages

set -e  # Exit on error

echo "========================================="
echo "  REACTIVE LIGHT SHOW - INSTALLER"
echo "========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This script only works on Linux"
    exit 1
fi

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "❌ Error: Cannot detect Linux distribution"
    exit 1
fi

echo "📦 Detected distro: $DISTRO"
echo ""

# Check for X11 (not Wayland)
echo "🖥️  Checking display server..."
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "⚠️  WARNING: You are running Wayland, but this app requires X11"
    echo "   Please log out and select 'X11' or 'Xorg' session at login"
    echo ""
    read -p "Continue anyway? (y/n): " continue
    if [[ ! "$continue" =~ ^[Yy]$ ]]; then
        exit 1
    fi
elif [ "$XDG_SESSION_TYPE" = "x11" ]; then
    echo "✅ X11 detected - good!"
else
    echo "⚠️  Display server type unknown (not Wayland or X11)"
fi
echo ""

# Install system dependencies based on distro
echo "📦 Installing system dependencies..."
echo ""

case "$DISTRO" in
    ubuntu|debian|linuxmint|pop)
        echo "Using apt-get for Ubuntu/Debian/Mint..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip portaudio19-dev xdotool wmctrl
        ;;

    fedora|rhel|centos)
        echo "Using dnf for Fedora/RHEL/CentOS..."
        sudo dnf install -y python3 python3-pip portaudio-devel xdotool wmctrl
        ;;

    arch|manjaro)
        echo "Using pacman for Arch/Manjaro..."
        sudo pacman -S --noconfirm python python-pip portaudio xdotool wmctrl
        ;;

    opensuse*)
        echo "Using zypper for openSUSE..."
        sudo zypper install -y python3 python3-pip portaudio-devel xdotool wmctrl
        ;;

    *)
        # Try to detect based on package manager
        if command -v apt-get &> /dev/null; then
            echo "Using apt-get (Debian-based)..."
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip portaudio19-dev xdotool wmctrl
        elif command -v dnf &> /dev/null; then
            echo "Using dnf (Fedora-based)..."
            sudo dnf install -y python3 python3-pip portaudio-devel xdotool wmctrl
        elif command -v pacman &> /dev/null; then
            echo "Using pacman (Arch-based)..."
            sudo pacman -S --noconfirm python python-pip portaudio xdotool wmctrl
        elif command -v zypper &> /dev/null; then
            echo "Using zypper (openSUSE)..."
            sudo zypper install -y python3 python3-pip portaudio-devel xdotool wmctrl
        else
            echo "❌ Error: Could not detect package manager"
            echo "   Please install manually: python3, python3-pip, portaudio-dev, xdotool, wmctrl"
            exit 1
        fi
        ;;
esac

echo ""
echo "✅ System dependencies installed"
echo ""

# Install Python packages
echo "🐍 Installing Python packages..."
pip3 install --user pygame numpy pyaudio

echo ""
echo "✅ Python packages installed"
echo ""

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x start-light-show.sh
chmod +x monitor_config.py

echo "✅ Permissions set"
echo ""

# Test installations
echo "🧪 Verifying installations..."
echo ""

# Check Python packages
python3 -c "import pygame, numpy, pyaudio" 2>/dev/null && echo "✅ Python packages: OK" || echo "❌ Python packages: FAILED"

# Check system tools
command -v xrandr &> /dev/null && echo "✅ xrandr: OK" || echo "❌ xrandr: MISSING"
command -v xdotool &> /dev/null && echo "✅ xdotool: OK" || echo "❌ xdotool: MISSING"
command -v wmctrl &> /dev/null && echo "✅ wmctrl: OK" || echo "❌ wmctrl: MISSING"

echo ""
echo "========================================="
echo "  ✅ INSTALLATION COMPLETE!"
echo "========================================="
echo ""
echo "🚀 To start the light show:"
echo "   ./start-light-show.sh"
echo ""
echo "📖 For more info, see README.md"
echo ""
