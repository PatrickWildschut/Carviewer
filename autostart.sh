#!/bin/bash
#
# Launch Carviewer fullscreen when the desktop session starts.
# Started by ~/.config/autostart/carviewer.desktop (the labwc session runs
# lxsession-xdg-autostart), so no terminal window is opened.

LOG="$HOME/Carviewer/carviewer.log"

# Let the compositor, panel and output configuration settle first.
sleep 3

cd "$HOME/Carviewer" || exit 1

# Keep the log from growing forever across reboots.
if [ -f "$LOG" ] && [ "$(stat -c %s "$LOG")" -gt 1048576 ]; then
    : > "$LOG"
fi

echo "=== $(date '+%Y-%m-%d %H:%M:%S') starting: ./main.py fullscreen ===" >> "$LOG"

exec ./main.py fullscreen >> "$LOG" 2>&1
