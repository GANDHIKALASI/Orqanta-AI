#!/usr/bin/env python3
"""
Orqanta AI - Voice Command Assistant
Accepts voice input from microphone, transcribes it, and executes device tools.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import orqanta

# Define your car / watch / laptop actions
@orqanta.tool
def set_cabin_ac(temperature: int, fan: int = 3):
    """Adjust AC temperature and fan speed."""
    print(f"🚗 [Car Action Executed] Setting AC to {temperature}°C (Fan: {fan})")
    return {"status": "ok", "temp": temperature}

@orqanta.tool
def control_music(action: str, song: str = ""):
    """Control audio and music playback: play, pause, next, volume_up, volume_down."""
    print(f"🎵 [Music Action Executed] Action: {action} (Song: {song})")
    return {"status": "playing", "action": action}

@orqanta.tool
def check_device_battery():
    """Query current device battery percentage."""
    print("🔋 [Battery Action Executed] Battery: 91% (Healthy)")
    return {"battery_percent": 91}

def run_voice_pipeline(audio_transcript: str):
    """
    Takes the transcribed voice input and triggers Orqanta AI.
    """
    agent = orqanta.Orqanta(tools=[set_cabin_ac, control_music, check_device_battery])
    
    print(f"\n🎙️ Voice Heard: \"{audio_transcript}\"")
    result = agent.run(audio_transcript)
    
    print(f"🧠 Model Reasoning: {result.get('reasoning')}")
    print(f"⚙️ Actions Dispatched: {result.get('function_calls')}")
    print(f"⏱️ Response Time: {result.get('decode_tps')} tokens/sec | RAM: {result.get('peak_ram_mb')} MB\n")

if __name__ == "__main__":
    print("=" * 60)
    print(" Orqanta AI - Voice Command Pipeline Demo")
    print("=" * 60)
    
    # Simulating 3 real-world voice inputs captured by mic in Car / Watch / Laptop
    sample_voice_commands = [
        "Hey car, set the AC to 22 degrees please",
        "Play the next song on my playlist",
        "How much battery do I have left?"
    ]
    
    for voice_text in sample_voice_commands:
        run_voice_pipeline(voice_text)
