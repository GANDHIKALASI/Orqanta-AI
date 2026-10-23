#!/usr/bin/env python3
"""
Orqanta AI - Vehicle Voice Command Pipeline
Handles hands-free voice commands in Car Cockpit (Microphone array)
and Two-Wheeler Helmet (Bluetooth Intercom headset).

Pure CPU execution | Sub-50ms latency | 79MB RAM
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import orqanta

# -----------------------------------------------------------------------------
# Vehicle Voice Actions (Car & Two-Wheeler)
# -----------------------------------------------------------------------------

@orqanta.tool
def set_vehicle_climate(temperature: int, fan: int = 3):
    """Adjust in-car climate temperature in Celsius and fan speed."""
    print(f"🚗 [HVAC Action] Cabin climate set to {temperature}°C (Fan: {fan})")
    return {"status": "ok", "target_temperature": temperature}

@orqanta.tool
def vehicle_media_control(action: str, query: str = ""):
    """Control audio and playlist playback: play, pause, next, volume_up, volume_down."""
    print(f"🎵 [Media Control] Action: {action.upper()} | Target: {query or 'current track'}")
    return {"status": "ok", "action": action}

@orqanta.tool
def check_vehicle_range(vehicle_type: str = "ev"):
    """Query vehicle estimated range, battery SOC, or petrol fuel distance-to-empty."""
    if "two_wheeler" in vehicle_type.lower() or "scooter" in vehicle_type.lower():
        print("🛵 [Two-Wheeler Cluster] Battery SOC: 74% | Estimated Range: 71 km (Ride mode)")
        return {"vehicle": "two_wheeler", "soc": 74, "range_km": 71}
    else:
        print("🚗 [Car Telemetry] EV Range: 366 km | Battery: 82% | BMS Status: Healthy")
        return {"vehicle": "car", "soc": 82, "range_km": 366}

def run_voice_pipeline(audio_transcript: str):
    """
    Takes the transcribed voice input (from car mic or helmet intercom)
    and executes Orqanta AI on the vehicle head-unit.
    """
    agent = orqanta.Orqanta(tools=[set_vehicle_climate, vehicle_media_control, check_vehicle_range])
    
    print(f"\n🎙️ Voice Heard: \"{audio_transcript}\"")
    result = agent.run(audio_transcript)
    
    print(f"🧠 Model Reasoning: {result.get('reasoning')}")
    print(f"⚙️ Actions Dispatched: {result.get('function_calls')}")
    print(f"⏱️ Response Time: {result.get('decode_tps')} tokens/sec | RAM: {result.get('peak_ram_mb')} MB\n")

if __name__ == "__main__":
    print("=" * 65)
    print(" Orqanta AI - Hands-Free Vehicle Voice Command Pipeline")
    print(" (Car Cockpit Microphone & Two-Wheeler Helmet Intercom)")
    print("=" * 65)
    
    sample_voice_commands = [
        "Hey, set the cabin temperature to 21 degrees please",
        "Skip to the next song",
        "How much driving range do I have left?"
    ]
    
    for voice_text in sample_voice_commands:
        run_voice_pipeline(voice_text)
