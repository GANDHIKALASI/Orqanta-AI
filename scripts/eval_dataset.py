#!/usr/bin/env python3
"""
Orqanta-AI Vehicle Dataset Benchmark & Evaluation Tool
Evaluates both Car and Two-Wheeler datasets:
1. Orqanta_AI_Dataset_v1 (Cars: EV & Petrol)
2. Orqanta_TwoWheeler_Dataset_v1 (Two-Wheelers: EV & Petrol Scooters / Motorcycles)
"""

import os
import sys
import json
import time
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import orqanta

DATASETS = {
    "🚗 Car (EV & Petrol)": os.path.abspath(os.path.join(os.path.dirname(__file__), "../Orqanta_AI_Dataset_v1")),
    "🛵 Two-Wheeler (EV & Petrol)": os.path.abspath(os.path.join(os.path.dirname(__file__), "../Orqanta_TwoWheeler_Dataset_v1"))
}

def load_split(dataset_dir: str, filename: str):
    path = os.path.join(dataset_dir, filename)
    if not os.path.exists(path):
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

def print_dataset_summary(name: str, dataset_dir: str):
    train_data = load_split(dataset_dir, "train.jsonl")
    val_data = load_split(dataset_dir, "validation.jsonl")
    test_data = load_split(dataset_dir, "test.jsonl")
    
    total = len(train_data) + len(val_data) + len(test_data)
    print("=" * 68)
    print(f"  {name} SFT Dataset Overview")
    print("=" * 68)
    print(f"  • Total Examples:    {total}")
    print(f"  • Training Split:    {len(train_data)} ({len(train_data)/total*100:.1f}%)")
    print(f"  • Validation Split:  {len(val_data)} ({len(val_data)/total*100:.1f}%)")
    print(f"  • Test Split:        {len(test_data)} ({len(test_data)/total*100:.1f}%)")
    print("-" * 68)
    
    cats = Counter(x.get("category", "unknown") for x in train_data + val_data + test_data)
    print("  Category Distribution:")
    for cat, count in cats.most_common()[:8]:
        print(f"    - {cat:<24} : {count:>3} records")
    print("=" * 68 + "\n")

def evaluate_samples(dataset_dir: str, label: str, n_samples: int = 2):
    test_data = load_split(dataset_dir, "validation.jsonl")
    if not test_data:
        return
    
    print(f"⚡ Testing Offline Edge Latency on {label}...")
    agent = orqanta.Orqanta()
    
    for i, item in enumerate(test_data[:n_samples]):
        user_msg = ""
        for m in item["messages"]:
            if m["role"] == "user":
                user_msg = m["content"]
        
        expected_asst = ""
        for m in item["messages"]:
            if m["role"] == "assistant":
                expected_asst = m["content"]

        t0 = time.perf_counter()
        res = agent.run(user_msg[:120])
        elapsed_ms = (time.perf_counter() - t0) * 1000
        
        print(f"  [{i+1}/{n_samples}] ID: {item.get('id')} | Category: {item.get('category')}")
        print(f"      Latency: {elapsed_ms:.1f} ms | RAM: {res.get('peak_ram_mb')} MB | TPS: {res.get('decode_tps')}")

if __name__ == "__main__":
    for name, path in DATASETS.items():
        print_dataset_summary(name, path)
        evaluate_samples(path, name, n_samples=2)
        print()
