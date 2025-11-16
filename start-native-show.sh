#!/bin/bash
# Native Light Show Launcher - Uses SDL/pygame for proper multi-monitor spanning

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TOTAL_WIDTH=5760
TOTAL_HEIGHT=1080

echo "Starting native light show (SDL/pygame)..."
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

# Run the Python light show in background (triple monitor version)
python3 "$SCRIPT_DIR/light-show-triple.py" &
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
    echo "Window positioned to cover entire screen including taskbar"
fi

# Wait for the process to finish
wait $PID

# Restore panels after exit
echo "Restoring panels..."
for panel in $PANELS; do
    xdotool windowmap $panel 2>/dev/null
done
