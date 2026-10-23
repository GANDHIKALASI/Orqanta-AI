#!/usr/bin/env python3
"""
Orqanta AI - Linux Laptop System Assistant Example
Runs seamlessly on any Linux laptop (x86_64 or ARM64) with <80MB RAM and 0% GPU.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import orqanta

@orqanta.tool
def get_battery_status():
    """Check current battery percentage and power state."""
    battery_pct = 88
    is_charging = True
    print(f"💻 [Power] Battery level: {battery_pct}% (Charging: {is_charging})")
    return {"battery_percent": battery_pct, "charging": is_charging}

@orqanta.tool
def set_system_volume(volume: int, mute: bool = False):
    """Set the system audio output volume."""
    print(f"💻 [Audio] System volume set to {volume}% (Muted: {mute})")
    return {"volume": volume, "muted": mute}

@orqanta.tool
def toggle_wifi(enabled: bool):
    """Enable or disable Wi-Fi networking."""
    state = "ENABLED" if enabled else "DISABLED"
    print(f"💻 [Network] Wi-Fi adapter has been {state}")
    return {"wifi_enabled": enabled}

@orqanta.tool
def open_application(app_name: str):
    """Launch an application on Linux."""
    print(f"💻 [Desktop] Launching application: {app_name}")
    return {"launched": True, "app": app_name}

def main():
    agent = orqanta.Orqanta(tools=[get_battery_status, set_system_volume, toggle_wifi, open_application])

    queries = [
        "What is my laptop battery percentage?",
        "Please turn the audio volume down to 30%",
        "Disable Wi-Fi connection",
        "Open the terminal application"
    ]

    print("==================================================")
    print("Orqanta AI - Linux Laptop System Controller Demo")
    print("==================================================")

    for q in queries:
        print(f"\nUser Command: '{q}'")
        res = agent.run(q)
        print(f"Reasoning: {res.get('reasoning')}")
        print(f"Results: {res.get('results')}")
        print(f"RAM: {res.get('peak_ram_mb')} MB | TPS: {res.get('decode_tps')}")

if __name__ == "__main__":
    main()
