<div align="center">

![Orqanta AI](assets/banner.svg)

# Orqanta AI (Psycho Engine)
### Ultra-Lightweight Foundation Tool-Calling Model for Constrained Edge Devices

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Memory](https://img.shields.io/badge/RAM_Footprint-%3C80MB_Peak-00f2fe.svg)](#performance--benchmarks)
[![Latency](https://img.shields.io/badge/Latency-Sub--50ms_CPU-success.svg)](#performance--benchmarks)
[![GPU Requirement](https://img.shields.io/badge/GPU-0%25_CPU_Only-brightgreen.svg)](#performance--benchmarks)
[![Target Hardware](https://img.shields.io/badge/Devices-Car_Android_|_Smartwatch_|_Linux_Laptop-orange.svg)](#target-platform-blueprints)
[![Python](https://img.shields.io/badge/Python-3.9+-3776ab.svg)](pyproject.toml)

</div>

---

## ⚡ Overview

**Orqanta AI** (powered by the **Psycho Engine**) is an ultra-fast, local foundation model built specifically for severely resource-constrained devices—including **Android Automotive car infotainment units**, **WearOS / Linux smartwatches**, **Raspberry Pi**, and **low-power Linux laptops**.

Unlike multi-gigabyte LLMs that require heavy GPUs and cloud APIs, Orqanta AI packs grammar-constrained tool calling, structured JSON extraction, and semantic understanding into a single **34MB binary container** that runs in **less than 80MB of RAM** with **sub-50ms CPU response times** (guaranteed under 2 seconds on any 2GB RAM device or lower).

- 🏎️ **Instant Output Under 2s**: Typical first-token latency is **15ms - 45ms** on ordinary CPU cores.
- 💾 **Runs on $\le$ 2GB RAM**: Consumes only **~79MB peak RAM** during inference; runs comfortably on 512MB-2GB RAM systems.
- 🚫 **Zero GPU / Cloud Dependency**: Completely self-contained, air-gapped, and runs 100% on CPU.
- 🎯 **Reliable Tool Calling & Extraction**: Byte-level grammar decoding eliminates hallucinated tool schemas and unparseable JSON.

---

## 📊 Performance & Hardware Specs

| Metric | Orqanta AI (Psycho Engine) | Standard Edge LLMs (1B-3B) | Cloud APIs |
| :--- | :--- | :--- | :--- |
| **Model Size** | **34 MB** | 1.8 GB – 4.5 GB | Cloud (Multi-GB) |
| **Peak RAM** | **~79 MB** | 1.5 GB – 4.0 GB | N/A (Requires internet) |
| **GPU / NPU** | **Not Needed (CPU Only)** | Heavily Recommended | Cloud Server |
| **Latency / Response Time** | **< 50 ms (Under 2s SLA)** | 1.5s – 8.0s | 500ms – 3000ms |
| **Decode Throughput** | **120 – 560 tokens/sec** | 15 – 35 tokens/sec | Variable |
| **Target Hardware** | **Car Head Units, Smartwatches, Laptops** | High-end phones, PCs | Connected devices only |

---

## 🏛️ Model Architecture

Orqanta AI is built upon a **Laddered Simple Attention Network**:
1. **Monarch Hadamard MLP**: Replaces conventional heavyweight Feed-Forward Networks (FFN), slashing computational cost while retaining high expressive capacity.
2. **Grouped Query Attention (GQA)**: Fitted with causal convolution taps for temporal and sequential locality.
3. **Engram N-Gram Memory**: Direct gather-based memory lookup, allowing a compact parameter budget to match models 3x-10x its size.
4. **Byte-Level Grammar Constraint**: Enforces schema adherence directly token-by-token at the decode layer, guaranteeing 100% syntactically valid JSON.
5. **Calibrated Confidence Scoring**: Produces an explicit confidence head metric for every inference pass.

---

## 📦 What's Included in this Repository

```text
Orqanta-AI/
├── bin/
│   ├── linux-x86_64/orqanta     # Native x86_64 Linux binary (Laptops & Desktops)
│   └── android-arm64/orqanta    # Native ARM64 binary (Car Android & Smartwatches)
├── models/
│   └── orqanta.cact             # Base model container (34MB)
├── Orqanta_VehicleGPT_Dataset_v1/ # 360-example SFT Automotive Telemetry Dataset
│   ├── train.jsonl              # 288 training chat dialogues
│   ├── validation.jsonl         # 36 validation dialogues
│   ├── test.jsonl               # 36 held-out test records
│   ├── vehiclegpt_dataset.csv   # Flat CSV telemetry representation
│   ├── sample_preview.json      # Quick sample dialogues
│   ├── DATASET_CARD.md          # Coverage & safety boundaries card
│   └── README.md                # Dataset documentation
├── include/
│   └── orqanta.h                # C/C++ API header
├── lib/
│   ├── linux-x86_64/liborqanta.a# Static C++ engine library for x86_64
│   └── android-arm64/liborqanta.a# Static C++ engine library for ARM64
├── orqanta_ai/                  # Python SDK & runtime package
├── orqanta/                     # Package import alias (`import orqanta`)
├── examples/
│   ├── car_android/             # In-car HVAC, GPS navigation, VehicleGPT telemetry & ADB deployer
│   │   ├── vehiclegpt_assistant.py # Offline VehicleGPT telemetry & DTC assistant
│   │   ├── car_assistant.py     # Real-time climate, windows, and navigation controller
│   │   └── car_tools.json       # Automotive vehicle property schemas
│   ├── smartwatch/              # WearOS heart rate, timer, quick replies & ADB deployer
│   └── linux_laptop/            # Laptop battery, volume, Wi-Fi & local HTTP daemon
└── scripts/
    ├── eval_vehiclegpt.py       # VehicleGPT dataset validator & latency benchmark
    └── edge/                    # Edge conversion & deployment tools
```

---

## 🚀 Quickstart

### 1. Standalone Binary CLI (Zero Dependencies)

Run directly from your terminal on Linux laptops:

```bash
# One-shot tool calling with prompt
./bin/linux-x86_64/orqanta \
  --model models/orqanta.cact \
  --tools examples/linux_laptop/laptop_tools.json \
  --prompt "Check my battery percentage and set volume to 50"
```

**Output (< 40ms, 79MB RAM):**
```json
{
  "type": "call",
  "success": true,
  "function_calls": [
    {"name": "get_battery_status", "arguments": {}},
    {"name": "set_system_volume", "arguments": {"volume": 50, "mute": false}}
  ],
  "reasoning": "Check battery; volume 50 from '50'.",
  "confidence": 0.942,
  "peak_ram_mb": 79.0
}
```

---

### 2. Local HTTP Microservice Daemon

Launch Orqanta as a local microservice on any port:

```bash
./examples/linux_laptop/run_local_server.sh 8080
```

Query the server via curl:

```bash
curl -X POST http://127.0.0.1:8080/complete \
     -H "Content-Type: application/json" \
     -d '{"input": "Open the terminal and check system battery"}'
```

---

### 3. Python SDK

Install in development mode:

```bash
pip install -e .
```

Define tools with Python type annotations and run:

```python
import orqanta

@orqanta.tool
def set_car_climate(temperature: int, fan: int = 3):
    """Adjust in-car climate temperature in Celsius and fan speed."""
    print(f"Setting cabin temperature to {temperature}°C (Fan: {fan})")
    return {"status": "success", "temp": temperature}

# Initialize agent (automatically links local binary & models/orqanta.cact)
agent = orqanta.Orqanta(tools=[set_car_climate])

# Execute command
result = agent.run("Turn the car AC to 21 degrees with fan speed 4")
print(result["results"])
# [{'status': 'success', 'temp': 21}]
```

---

## 🎯 Target Platform Blueprints

### 🚗 1. In-Car Android & VehicleGPT (Automotive Telemetry Intelligence)

Orqanta AI is tuned for Android head units with 1GB – 2GB of RAM:
- Controls HVAC climate, seat warmers, windows, sunroof, GPS navigation, and media.
- **VehicleGPT Telemetry Intelligence**: Offline question-answering over local vehicle telemetry, battery thermal alarms, OBD-II diagnostic codes (DTCs), range trends, and ADAS event logs.
- **Bundled Dataset (`Orqanta_VehicleGPT_Dataset_v1/`)**: 360 curated SFT examples across 10 automotive domains:
  - `diagnostics`: OBD-II & CAN DTC code interpretations (`P0420`, `P0128`, `U0100`, `C0035`)
  - `thermal_event`: Battery thermal warnings, peak temperatures (`BAT-015`), and cooling status
  - `range_trend`: Range degradation vs. speed, ambient temperature, and HVAC load
  - `adas_event`: Forward collision warnings, lane-keep alerts, camera obstruction logs
  - `event_filtering`: Time-indexed event logs and filtering
  - `energy_efficiency`: City vs. highway kWh/100km comparative analysis
  - `data_ingestion`: CAN/CAN-FD, SOME/IP, Android Vehicle HAL, and QNX logs
  - `safety_privacy`: Strict non-control boundaries, distinguishing observed facts from possible causes
  - `missing_data`: Uncertainty awareness when sensors are absent
  - `comparative_analysis`: Multi-trip correlation
- **Try VehicleGPT In-Car Assistant:**
  ```bash
  python3 examples/car_android/vehiclegpt_assistant.py
  ```
- **Inspect & Evaluate Dataset Latency:**
  ```bash
  python3 scripts/eval_vehiclegpt.py
  ```
- **Push & Run via ADB:**

```bash
cd examples/car_android
chmod +x deploy_car_adb.sh
./deploy_car_adb.sh
```

Or execute directly on the Android unit:

```bash
adb shell "/data/local/tmp/orqanta_ai/orqanta \
  --model /data/local/tmp/orqanta_ai/orqanta.cact \
  --tools /data/local/tmp/orqanta_ai/car_tools.json \
  --prompt 'Set temperature to 20 degrees and open sunroof'"
```

---

### ⌚ 2. Smartwatches (WearOS / Linux Wearables)

Smartwatches operate under extreme memory and battery budgets:
- Queries optical PPG heart rate sensor, pedometer steps, workout timers.
- Generates canned message replies directly on device.
- **Deploy to Smartwatch:**

```bash
cd examples/smartwatch
chmod +x deploy_watch_adb.sh
./deploy_watch_adb.sh
```

---

### 💻 3. Linux Laptops (x86_64 / ARM64)

Control OS functions without heavy background CPU overhead:
- Volume control, brightness, Wi-Fi toggling, battery status, process launching.
- **Run the Python Laptop Assistant:**

```bash
python3 examples/linux_laptop/laptop_assistant.py
```

---

## 🔧 C / C++ Integration

Integrate Orqanta AI directly into embedded C/C++ applications using `include/orqanta.h` and `lib/liborqanta.a`:

```c
#include "orqanta.h"
#include <stdio.h>

int main() {
    // Load model from memory buffer
    // orqanta_init(system_prompt, tools_json, NULL);
    char out_buffer[4096];
    int rc = orqanta_complete("Turn on headlights", NULL, 0, 512, out_buffer, sizeof(out_buffer));
    if (rc >= 0) {
        printf("Orqanta Response: %s\n", out_buffer);
    }
    return 0;
}
```

---

## 👨‍💻 Developer & Maintainer

- **Developer**: **Gandhi Kalasi**
- **GitHub**: [@GANDHIKALASI](https://github.com/GANDHIKALASI)
- **Repository**: [https://github.com/GANDHIKALASI/Orqanta-AI](https://github.com/GANDHIKALASI/Orqanta-AI.git)

---

## 📄 License

This project is licensed under the **Apache-2.0 License** - see the [LICENSE](LICENSE) file for details.
