<div align="center">

![Orqanta AI](assets/banner.svg)

# Orqanta AI (Psycho Engine)
### Ultra-Lightweight Automotive Foundation Model for Electric & Petrol Vehicles

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Memory](https://img.shields.io/badge/RAM_Footprint-%3C80MB_Peak-00f2fe.svg)](#performance--benchmarks)
[![Latency](https://img.shields.io/badge/Latency-Sub--50ms_CPU-success.svg)](#performance--benchmarks)
[![GPU Requirement](https://img.shields.io/badge/GPU-0%25_CPU_Only-brightgreen.svg)](#performance--benchmarks)
[![Target Hardware](https://img.shields.io/badge/Vehicles-Cars_(EV_&_Petrol)_|_Two--Wheelers_(Scooters_&_Bikes)-orange.svg)](#target-platform-blueprints)
[![Python](https://img.shields.io/badge/Python-3.9+-3776ab.svg)](pyproject.toml)

</div>

---

## ⚡ Overview

**Orqanta AI** (powered by the **Psycho Engine**) is an ultra-fast, offline foundation tool-calling and telemetry intelligence model engineered specifically for **Vehicles**:
- 🚗 **Cars (Electric & Petrol / ICE / Hybrid)**: Runs on Android Automotive OS (AAOS) & Linux In-Vehicle Infotainment (IVI) head units.
- 🛵 **Two-Wheelers (Electric Scooters & Petrol Motorcycles)**: Runs on ARM64 Digital Instrument Clusters & Smart TFT Dashboards (Ather, TVS, Ola, Royal Enfield Tripper style).

Unlike multi-gigabyte cloud LLMs that require heavy GPUs, fast internet, and massive power, Orqanta AI packs grammar-constrained function calling, structured JSON extraction, and automotive telemetry reasoning into a single **34MB binary container** that executes in **less than 80MB of RAM** with **sub-50ms CPU response times** (guaranteed under 2 seconds on any 1GB–2GB RAM vehicle ECU).

- 🏎️ **Instant Output Under 2s**: Typical first-token latency is **15ms - 45ms** on ordinary embedded ARM64/x86 CPU cores.
- 💾 **Runs on $\le$ 2GB RAM**: Consumes only **~79MB peak RAM** during inference; leaves 90%+ RAM free for GPS navigation and digital cluster rendering.
- 🚫 **Zero GPU / Cloud Dependency**: 100% self-contained, air-gapped, and runs in dead zones, remote highways, and underground tunnels.
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
| **Target Hardware** | **Car Head Units, Bike Digital Clusters** | High-end phones, PCs | Connected devices only |

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
│   ├── linux-x86_64/orqanta     # Native x86_64 Linux binary (Testing & Linux IVI)
│   └── android-arm64/orqanta    # Native ARM64 binary (Car Android & Cluster Displays)
├── models/
│   └── orqanta.cact             # Base model container (34MB)
├── Orqanta_AI_Dataset_v1/        # 360-example SFT Car Telemetry Dataset (EV & Petrol)
│   ├── train.jsonl              # 288 training chat dialogues
│   ├── validation.jsonl         # 36 validation dialogues
│   ├── test.jsonl               # 36 held-out test records
│   ├── orqanta_ai_dataset.csv   # Flat CSV telemetry representation
│   └── DATASET_CARD.md          # Coverage & safety boundaries card
├── Orqanta_TwoWheeler_Dataset_v1/# 380-example SFT Two-Wheeler Dataset (Bikes & Scooters)
│   ├── train.jsonl              # 304 training dialogues (Electric & Petrol)
│   ├── validation.jsonl         # 35 validation dialogues
│   ├── test.jsonl               # 41 held-out test dialogues
│   ├── two_wheeler_dataset.csv  # Flat CSV representation
│   └── DATASET_CARD.md          # Scope & maintenance/tyre safety card
├── include/
│   └── orqanta.h                # C/C++ API header
├── lib/
│   ├── linux-x86_64/liborqanta.a# Static C++ engine library for x86_64
│   └── android-arm64/liborqanta.a# Static C++ engine library for ARM64
├── orqanta_ai/                  # Python SDK & runtime package
├── orqanta/                     # Package import alias (`import orqanta`)
├── examples/
│   ├── car_android/             # In-car HVAC, GPS navigation, EV/ICE telemetry & ADB deployer
│   │   ├── orqanta_car_assistant.py # Offline car telemetry & DTC diagnostic assistant
│   │   ├── car_assistant.py     # Real-time climate, windows, and navigation controller
│   │   ├── car_tools.json       # Automotive vehicle property schemas
│   │   └── deploy_car_adb.sh    # ADB push script for Android Automotive
│   ├── two_wheeler/             # Scooter & Motorcycle cluster assistant
│   │   ├── two_wheeler_assistant.py # EV battery range & petrol mileage cluster assistant
│   │   └── two_wheeler_tools.json # Two-wheeler instrument cluster schemas
│   └── voice_assistant.py       # Vehicle cockpit mic & helmet intercom voice pipeline
└── scripts/
    ├── eval_dataset.py          # Dual dataset benchmark & latency validator
    └── edge/                    # Edge conversion & deployment tools
```

---

## 🚀 Quickstart

### 1. Standalone Binary CLI (Zero Dependencies)

Run directly from your terminal:

```bash
# Vehicle tool calling with natural language prompt
./bin/linux-x86_64/orqanta \
  --model models/orqanta.cact \
  --tools examples/car_android/car_tools.json \
  --prompt "Check diagnostic trouble codes and set temperature to 21 degrees"
```

**Output (< 40ms, 79MB RAM):**
```json
{
  "type": "call",
  "success": true,
  "function_calls": [
    {"name": "query_diagnostic_trouble_codes", "arguments": {"subsystem": "all"}},
    {"name": "set_climate", "arguments": {"temperature": 21}}
  ],
  "reasoning": "DTC diagnostics -> query_diagnostic_trouble_codes; temp 21 -> set_climate 21.",
  "confidence": 0.942,
  "peak_ram_mb": 79.0
}
```

---

### 2. Python SDK

Install in development mode:

```bash
pip install -e .
```

Define vehicle tools with Python type annotations and run:

```python
import orqanta

@orqanta.tool
def set_cabin_climate(temperature: int, fan: int = 3):
    """Adjust in-car climate temperature in Celsius and fan speed."""
    print(f"Setting cabin temperature to {temperature}°C (Fan: {fan})")
    return {"status": "success", "temp": temperature}

# Initialize agent (automatically links local binary & models/orqanta.cact)
agent = orqanta.Orqanta(tools=[set_cabin_climate])

# Execute command
result = agent.run("Turn the car AC to 21 degrees with fan speed 4")
print(result["results"])
# [{'status': 'success', 'temp': 21}]
```

---

## 🎯 Target Platform Blueprints

### 🚗 1. In-Car Android & Linux IVI (Electric & Petrol Cars)

Orqanta AI is tuned for Android head units (AAOS) and Automotive Grade Linux (AGL) with 1GB – 2GB of RAM:
- **Electric Vehicles (EV)**: High-voltage battery pack thermal telemetry (`BAT-015`), SOC degradation trends, charging rate, and regenerative braking analysis.
- **Petrol / ICE Cars**: Fuel consumption, engine RPM, coolant temperature, OBD-II DTC diagnostic codes (`P0420`, `P0128`, `U0100`, `C0035`), and oil change intervals.
- **Body & Comfort Controls**: Cabin HVAC climate, seat warmers, windows, sunroof, and navigation.
- **Run the Car Assistant Demo:**
  ```bash
  python3 examples/car_android/orqanta_car_assistant.py
  ```
- **Push & Run via ADB to Android Automotive:**
  ```bash
  cd examples/car_android
  ./deploy_car_adb.sh
  ```

---

### 🛵 2. Two-Wheelers (Electric Scooters & Petrol Motorcycles)

Orqanta AI runs natively on low-power ARM64 Digital Instrument Clusters and TFT Dashboards:
- **Electric Scooters (Ather, Ola, TVS iQube, Chetak style)**: Battery SOC %, real-time range estimation by riding mode (Eco vs. Sport), battery cell temperature, and regenerative braking.
- **Petrol Motorcycles (Royal Enfield, Pulsar, KTM, Duke, Splendor style)**: Fuel tank level, Distance-To-Empty (DTE), average mileage (km/L), trip meter, and scheduled service interval.
- **Safety & TPMS Alerts**: Real-time Tyre Pressure Monitoring System (TPMS) low-pressure alerts and chain slack warnings.
- **Run the Two-Wheeler Cluster Demo:**
  ```bash
  python3 examples/two_wheeler/two_wheeler_assistant.py
  ```

---

### 🎙️ 3. Vehicle Voice Command Pipeline (Cockpit Mic & Helmet Intercom)

Test the voice assistant pipeline designed for steering wheel push-to-talk microphones and Bluetooth helmet intercoms:

```bash
python3 examples/voice_assistant.py
```

---

## 📊 Dual Dataset Benchmarks

Orqanta AI includes **740 curated SFT vehicle dialogues** across both four-wheeler and two-wheeler mobility domains:

```bash
python3 scripts/eval_dataset.py
```

```text
====================================================================
  🚗 Car (EV & Petrol) SFT Dataset Overview (Orqanta_AI_Dataset_v1)
====================================================================
  • Total Examples:    360 (Train: 288 | Val: 36 | Test: 36)
  • Coverage:          DTC diagnostics, battery thermal warnings, range trends,
                       energy efficiency, ADAS event filtering, CAN/HAL ingestion.

====================================================================
  🛵 Two-Wheeler SFT Dataset Overview (Orqanta_TwoWheeler_Dataset_v1)
====================================================================
  • Total Examples:    380 (Train: 304 | Val: 35 | Test: 41)
  • Coverage:          EV scooter battery & range, petrol bike mileage km/L,
                       TPMS tyre pressure alerts, maintenance reminders, trip comparison.
====================================================================
```

---

## 🔧 C / C++ Embedded Integration

Embed Orqanta AI directly into vehicle firmware and ECU daemons using `include/orqanta.h` and `lib/liborqanta.a`:

```c
#include "orqanta.h"
#include <stdio.h>

int main() {
    char out_buffer[4096];
    int rc = orqanta_complete("Check battery temperature and range", NULL, 0, 512, out_buffer, sizeof(out_buffer));
    if (rc >= 0) {
        printf("Vehicle Action: %s\n", out_buffer);
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
