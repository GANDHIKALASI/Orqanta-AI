#!/usr/bin/env python3
"""
Orqanta AI - Smartwatch (WearOS / Linux Wearables) Assistant Example
Runs within tight smartwatch hardware limits (<80MB RAM, sub-50ms CPU latency).
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import orqanta

@orqanta.tool
def get_heart_rate():
    """Read the user's current heart rate in BPM."""
    bpm = 72
    print(f"⌚ [Sensor] PPG Heart Rate sensor reading: {bpm} BPM (Normal)")
    return {"heart_rate_bpm": bpm, "status": "resting"}

@orqanta.tool
def set_timer(minutes: int, label: str = "Timer"):
    """Set a countdown timer on the smartwatch."""
    print(f"⌚ [Alarm/Timer] Timer set for {minutes} minute(s) - '{label}'")
    return {"timer_set": True, "minutes": minutes, "label": label}

@orqanta.tool
def get_step_count():
    """Get today's total recorded step count."""
    steps = 8450
    print(f"⌚ [Pedometer] Today's step count: {steps} / 10,000 steps (84.5% of goal)")
    return {"steps": steps, "goal": 10000}

@orqanta.tool
def send_quick_reply(recipient: str, message: str):
    """Send a quick reply to a contact."""
    print(f"⌚ [Messaging] Sent to {recipient}: \"{message}\"")
    return {"sent": True, "recipient": recipient, "message": message}

def main():
    agent = orqanta.Orqanta(tools=[get_heart_rate, set_timer, get_step_count, send_quick_reply])

    queries = [
        "What is my current heart rate?",
        "Set a 15 minute timer for workout session",
        "How many steps did I walk today?",
        "Reply to Alex: I am running 5 minutes late"
    ]

    print("==================================================")
    print("Orqanta AI - Smartwatch Wearable Demo (Ultra-Fast)")
    print("==================================================")

    for q in queries:
        print(f"\nUser Query: '{q}'")
        res = agent.run(q)
        print(f"Confidence: {res.get('confidence')} | Latency TPS: {res.get('decode_tps')}")
        print(f"Executed: {res.get('results')}")

if __name__ == "__main__":
    main()
