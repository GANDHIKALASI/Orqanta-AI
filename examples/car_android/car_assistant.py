#!/usr/bin/env python3
"""
Orqanta AI - Android Automotive / In-Car Assistant Example
Runs with <80MB RAM on CPU without GPU, latency <50ms (<2s).
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import orqanta

@orqanta.tool
def set_climate(temperature: int, fan_speed: int = 3, ac_enabled: bool = True):
    """Adjust car cabin temperature and AC fan speed."""
    print(f"🚗 [HVAC Action] Setting temperature to {temperature}°C, Fan: {fan_speed}, AC: {'ON' if ac_enabled else 'OFF'}")
    return {"status": "ok", "target_temp": temperature, "fan_speed": fan_speed}

@orqanta.tool
def control_windows(target: str, action: str):
    """Open or close car windows or sunroof."""
    print(f"🚗 [Body Action] Window/Sunroof: {target} -> {action}")
    return {"status": "success", "target": target, "action": action}

@orqanta.tool
def set_navigation(destination: str, avoid_tolls: bool = False):
    """Start GPS navigation to a destination."""
    print(f"🚗 [GPS Navigation] Routing to: {destination} (Avoid tolls: {avoid_tolls})")
    return {"status": "routing", "destination": destination}

def main():
    agent = orqanta.Orqanta(tools=[set_climate, control_windows, set_navigation])

    queries = [
        "Hey Orqanta, set the cabin temperature to 21 degrees and fan to 4",
        "Open the sunroof for some fresh air",
        "Navigate to Downtown City Center avoiding tolls"
    ]

    print("==================================================")
    print("Orqanta AI - Car Android Automotive Demo (Sub-2s)")
    print("==================================================")

    for q in queries:
        print(f"\nUser Input: '{q}'")
        res = agent.run(q)
        print(f"Response: {res.get('reasoning')}")
        print(f"Function Calls: {res.get('function_calls')}")
        print(f"RAM Usage: {res.get('peak_ram_mb')} MB | TPS: {res.get('decode_tps')}")

if __name__ == "__main__":
    main()
