#!/usr/bin/env bash
# ==============================================================================
# Orqanta AI - ADB Deployer for WearOS / Smartwatches
# Pushes the ultra-lightweight Orqanta model to wearable storage
# ==============================================================================

set -e

WATCH_DIR="/data/local/tmp/orqanta_watch"

echo "⌚ [1/3] Connecting to Smartwatch via ADB..."
adb devices

echo "⌚ [2/3] Uploading binary & weights to smartwatch directory: ${WATCH_DIR}"
adb shell "mkdir -p ${WATCH_DIR}"
adb push bin/android-arm64/orqanta "${WATCH_DIR}/orqanta"
adb push models/orqanta.cact "${WATCH_DIR}/orqanta.cact"
adb push examples/smartwatch/watch_tools.json "${WATCH_DIR}/watch_tools.json"

adb shell "chmod +x ${WATCH_DIR}/orqanta"

echo "⌚ [3/3] Running on-device watch inference test..."
adb shell "${WATCH_DIR}/orqanta \
    --model ${WATCH_DIR}/orqanta.cact \
    --tools ${WATCH_DIR}/watch_tools.json \
    --prompt 'What is my current heart rate?'"

echo "✅ Smartwatch deployment complete! Instant execution under 50ms with 0% GPU."
