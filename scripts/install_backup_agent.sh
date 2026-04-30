#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_SRC="${PROJECT_ROOT}/scripts/com.novator.backup.plist"
PLIST_DST="${LAUNCH_AGENTS_DIR}/com.novator.backup.plist"

mkdir -p "$LAUNCH_AGENTS_DIR"
cp "$PLIST_SRC" "$PLIST_DST"

if launchctl print "gui/$(id -u)/com.novator.backup" >/dev/null 2>&1; then
    launchctl bootout "gui/$(id -u)" "$PLIST_DST" || true
fi

launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
"${PROJECT_ROOT}/scripts/daily_backup.sh"

echo "Backup agent installed: $PLIST_DST"
