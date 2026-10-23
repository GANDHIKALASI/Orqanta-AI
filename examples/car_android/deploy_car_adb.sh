#!/usr/bin/env bash
# ==============================================================================
# Orqanta AI - ADB Deployer for Android Automotive / Car Head Units
# Pushes Orqanta AI to /data/local/tmp and tests native inference (<80MB RAM)
# ==============================================================================

set -e

DEVICE_DIR="/data/local/tmp/orqanta_ai"

echo "🚗 [1/4] Checking connected Android Car / ADB devices..."
if ! command -v adb >/dev/null 2>&1; then
    echo "Error: adb command not found. Please install Android Platform Tools."
    exit 1
fi

adb devices

echo "🚗 [2/4] Creating device directory: ${DEVICE_DIR}"
adb shell "mkdir -p ${DEVICE_DIR}"

echo "🚗 [3/4] Pushing ARM64 binary and model weights..."
adb push bin/android-arm64/orqanta "${DEVICE_DIR}/orqanta"
adb push models/orqanta.cact "${DEVICE_DIR}/orqanta.cact"
adb push examples/car_android/car_tools.json "${DEVICE_DIR}/car_tools.json"

adb shell "chmod +x ${DEVICE_DIR}/orqanta"

echo "🚗 [4/4] Executing test in-car command via ADB..."
adb shell "${DEVICE_DIR}/orqanta \
    --model ${DEVICE_DIR}/orqanta.cact \
    --tools ${DEVICE_DIR}/car_tools.json \
    --prompt 'Hey car, turn the AC to 22 degrees and set fan speed to 4'"

echo "✅ Deployment successful! You can also run Orqanta AI as a local daemon:"
echo "   adb shell '${DEVICE_DIR}/orqanta --model ${DEVICE_DIR}/orqanta.cact --tools ${DEVICE_DIR}/car_tools.json --serve --port 8080 &'"
