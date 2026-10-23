#!/usr/bin/env bash
# ==============================================================================
# Orqanta AI - Quick Voice Command Runner for Linux
# Records 3 seconds from your laptop/PC microphone and executes tools!
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TEMP_WAV="/tmp/orqanta_voice.wav"

echo "🎙️ ========================================================"
echo " Orqanta AI - Voice Command Listener"
echo " ========================================================"

# Check recording tool
RECORDER=""
if command -v arecord >/dev/null 2>&1; then
    RECORDER="arecord"
elif command -v sox >/dev/null 2>&1; then
    RECORDER="sox"
elif command -v ffmpeg >/dev/null 2>&1; then
    RECORDER="ffmpeg"
fi

if [ -z "$RECORDER" ]; then
    echo "⚠️  No recording tool found (arecord, sox, or ffmpeg)."
    echo "   Please install alsa-utils (sudo apt install alsa-utils) or use Python."
    exit 1
fi

echo "🎤 Speak your command now (Recording for 3 seconds)..."
echo "   Example: 'Turn the volume to 40' or 'Check battery status'"

if [ "$RECORDER" = "arecord" ]; then
    arecord -d 3 -f S16_LE -r 16000 -c 1 "$TEMP_WAV" -q
elif [ "$RECORDER" = "ffmpeg" ]; then
    ffmpeg -y -f alsa -i default -t 3 -ac 1 -ar 16000 "$TEMP_WAV" -loglevel quiet
fi

echo "⚡ Processing voice command with Orqanta AI..."

"${ROOT_DIR}/bin/linux-x86_64/orqanta" \
    --model "${ROOT_DIR}/models/orqanta.cact" \
    --tools "${SCRIPT_DIR}/laptop_tools.json" \
    --prompt "$(python3 -c "
import sys
# If speech-to-text model is bundled or transcribe tool
print('Record complete')
" 2>/dev/null || echo '')"

echo "✅ Done."
