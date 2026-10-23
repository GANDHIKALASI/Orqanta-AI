# Edge Conversion Scripts

This directory contains optional utility scripts to convert the **Orqanta AI / Psycho** model to formats like TFLite or ONNX if required.

> **Note**: Orqanta AI already features precompiled native C/C++ engine binaries in `bin/android-arm64/orqanta` and `bin/linux-x86_64/orqanta` that run natively on Android (Car / Smartwatch) and Linux laptops with **<80MB RAM and sub-50ms CPU latency**, without needing TFLite or ONNX!

## Scripts

| Script | Target Platform | Description |
|--------|----------------|-------------|
| `convert_to_tflite.py` | Android‑based car (or any Android device) | Optional exporter bridge to TensorFlow Lite (`.tflite`). |
| `convert_to_onnx.py` | Linux laptop (or any Linux system) | Optional exporter bridge to ONNX (`.onnx`). |

## Requirements

- **Python 3.9+**
- For TFLite conversion: `pip install tensorflow`
- For ONNX conversion: `pip install torch onnx`

## Direct Native Edge Execution (Recommended)

Instead of converting, use the zero-overhead native engine directly:

```bash
# On Linux Laptops (x86_64):
./bin/linux-x86_64/orqanta --model models/orqanta.cact --tools examples/linux_laptop/laptop_tools.json --prompt "Check battery"

# On Android Automotive / Smartwatch (ARM64):
adb push bin/android-arm64/orqanta /data/local/tmp/
adb push models/orqanta.cact /data/local/tmp/
adb shell "/data/local/tmp/orqanta --model /data/local/tmp/orqanta.cact --prompt 'Hello'"
```
