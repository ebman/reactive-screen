#!/bin/bash
# Light Show Launcher - Choose between regular or smokey version

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/monitor_config.json"

echo "========================================="
echo "  REACTIVE LIGHT SHOW LAUNCHER"
echo "========================================="
echo ""

# Check for monitor configuration
if [ ! -f "$CONFIG_FILE" ]; then
    echo "No monitor configuration found. Running auto-detection..."
    python3 "$SCRIPT_DIR/monitor_config.py" || {
        echo "Failed to detect monitors. Using default: 3 monitors at 1920x1080"
        TOTAL_WIDTH=5760
        TOTAL_HEIGHT=1080
    }
fi

# Read monitor configuration from JSON
if [ -f "$CONFIG_FILE" ]; then
    TOTAL_WIDTH=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['total_width'])")
    TOTAL_HEIGHT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['total_height'])")
    NUM_MONITORS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['num_monitors'])")
    echo "Detected configuration: $NUM_MONITORS monitor(s), ${TOTAL_WIDTH}x${TOTAL_HEIGHT}"
else
    TOTAL_WIDTH=5760
    TOTAL_HEIGHT=1080
    NUM_MONITORS=3
    echo "Using default configuration: $NUM_MONITORS monitor(s), ${TOTAL_WIDTH}x${TOTAL_HEIGHT}"
fi

echo ""
echo "Choose your version:"
echo "  1) Regular - Clean organic fractals with glowing orbs"
echo "  2) Smokey - Adds atmospheric fog layers for dreamy blending"
echo "  3) Fluffy - Ultra-smooth, cloud-like (no harsh edges)"
echo ""
read -p "Enter choice (1, 2, or 3): " choice

if [ "$choice" == "2" ]; then
    SCRIPT="light-show-smokey.py"
    echo ""
    echo "Loading SMOKEY version..."
elif [ "$choice" == "3" ]; then
    SCRIPT="light-show-fluffy.py"
    echo ""
    echo "Loading FLUFFY version..."
else
    SCRIPT="light-show-triple.py"
    echo ""
    echo "Loading REGULAR version..."
fi

echo "Spanning ${TOTAL_WIDTH}x${TOTAL_HEIGHT} across all monitors"
echo "Press ESC or Q to exit"
echo ""

# Hide all panels/taskbars temporarily
echo "Hiding panels..."
PANELS=$(xdotool search --class "Xfce4-panel|gnome-panel|plasma-desktop|lxpanel|mate-panel|tint2" 2>/dev/null)
for panel in $PANELS; do
    xdotool windowunmap $panel 2>/dev/null
done

# Set SDL to span all monitors
export SDL_VIDEO_WINDOW_POS="0,0"
export SDL_VIDEO_CENTERED=0

# Run the Python light show in background
python3 "$SCRIPT_DIR/$SCRIPT" &
PID=$!

# Give it a moment to create the window
sleep 1

# Force window to span all monitors and cover everything including taskbar
WID=$(xdotool search --pid $PID | head -1)
if [ ! -z "$WID" ]; then
    echo "Forcing window $WID to span all monitors and cover taskbar..."
    # Add fullscreen and above states
    wmctrl -i -r $WID -b add,fullscreen,above
    wmctrl -i -r $WID -b remove,maximized_vert,maximized_horz
    # Position at absolute 0,0
    xdotool windowmove $WID 0 0
    xdotool windowsize $WID $TOTAL_WIDTH $TOTAL_HEIGHT
    # Raise to top
    xdotool windowraise $WID
    xdotool windowfocus $WID
    echo "Window positioned to cover entire screen"
fi

# Wait for the process to finish
wait $PID

# Restore panels after exit
echo "Restoring panels..."
for panel in $PANELS; do
    xdotool windowmap $panel 2>/dev/null
done

echo "Goodbye!"
