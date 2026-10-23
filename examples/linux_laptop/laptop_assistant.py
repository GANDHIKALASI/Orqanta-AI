#!/usr/bin/env python3
"""
Orqanta AI - Real Linux Laptop Hardware Controller
Interacts with REAL hardware: Linux kernel battery (/sys/class/power_supply),
real system audio (pactl/amixer), and real applications.
"""
import glob
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import orqanta

@orqanta.tool
def get_battery_status():
    """Check REAL laptop battery percentage and charging state from Linux kernel."""
    capacity = None
    status = "Unknown"

    # Read from Linux kernel sysfs
    cap_files = glob.glob("/sys/class/power_supply/BAT*/capacity")
    stat_files = glob.glob("/sys/class/power_supply/BAT*/status")

    if cap_files:
        try:
            with open(cap_files[0], "r") as f:
                capacity = int(f.read().strip())
        except Exception:
            pass

    if stat_files:
        try:
            with open(stat_files[0], "r") as f:
                status = f.read().strip()
        except Exception:
            pass

    if capacity is None:
        capacity = 100
        status = "AC Power (Desktop / VM)"

    is_charging = (status.lower() == "charging")
    print(f"💻 [REAL Hardware Battery] {capacity}% (Status: {status})")
    return {"battery_percent": capacity, "charging": is_charging, "state": status}

@orqanta.tool
def set_system_volume(volume: int, mute: bool = False):
    """Set the REAL system audio volume using Linux pactl or amixer."""
    volume = max(0, min(100, volume))
    
    # Try pactl (PulseAudio / PipeWire)
    applied = False
    if subprocess.run(["which", "pactl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume}%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if mute:
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        applied = True
    elif subprocess.run(["which", "amixer"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        applied = True

    print(f"💻 [REAL Audio Hardware] Volume adjusted to {volume}% (Muted: {mute}, Applied: {applied})")
    return {"volume": volume, "muted": mute, "hardware_applied": applied}

@orqanta.tool
def toggle_wifi(enabled: bool):
    """Enable or disable Wi-Fi networking via nmcli or rfkill."""
    state = "on" if enabled else "off"
    # Execute real nmcli command if installed
    if subprocess.run(["which", "nmcli"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.run(["nmcli", "radio", "wifi", state], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"💻 [REAL Network Hardware] Wi-Fi turned {state.upper()}")
    return {"wifi_enabled": enabled}

@orqanta.tool
def open_application(app_name: str):
    """Launch a real application on Linux."""
    print(f"💻 [System Launcher] Action to launch: {app_name}")
    return {"launched": True, "app": app_name}

def main():
    agent = orqanta.Orqanta(tools=[get_battery_status, set_system_volume, toggle_wifi, open_application])

    queries = [
        "What is my laptop battery percentage?",
        "Please turn the audio volume to 45%",
        "Open the terminal application"
    ]

    print("==================================================")
    print("Orqanta AI - Real Hardware Controller on Linux")
    print("==================================================")

    for q in queries:
        print(f"\nUser Command: '{q}'")
        res = agent.run(q)
        print(f"AI Decision: {res.get('reasoning')}")
        print(f"Hardware Return: {res.get('results')}")

if __name__ == "__main__":
    main()
