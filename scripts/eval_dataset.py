#!/usr/bin/env python3
"""
Orqanta-AI Automotive Dataset Benchmark & Evaluation Tool
Evaluates Orqanta_AI_Dataset_v1 splits (train, validation, test)
and measures edge model latency, grounding rules, and category coverage.
"""

import os
import sys
import json
import time
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import orqanta

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Orqanta_AI_Dataset_v1"))

def load_split(filename: str):
    path = os.path.join(DATASET_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ Error: {path} not found.")
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

def print_dataset_summary():
    train_data = load_split("train.jsonl")
    val_data = load_split("validation.jsonl")
    test_data = load_split("test.jsonl")
    
    total = len(train_data) + len(val_data) + len(test_data)
    print("=" * 65)
    print("  Orqanta-AI Automotive SFT Dataset v1.0 Overview")
    print("=" * 65)
    print(f"  • Total Examples:    {total}")
    print(f"  • Training Split:    {len(train_data)} ({len(train_data)/total*100:.1f}%)")
    print(f"  • Validation Split:  {len(val_data)} ({len(val_data)/total*100:.1f}%)")
    print(f"  • Test Split:        {len(test_data)} ({len(test_data)/total*100:.1f}%)")
    print("-" * 65)
    
    cats = Counter(x.get("category", "unknown") for x in train_data + val_data + test_data)
    print("  Category Distribution:")
    for cat, count in cats.most_common():
        print(f"    - {cat:<24} : {count:>3} records")
    print("=" * 65)

def evaluate_sample_inferences(n_samples: int = 3):
    test_data = load_split("validation.jsonl")
    if not test_data:
        return
    
    print(f"\n🚗 Running Offline Edge Evaluation on {n_samples} Samples from Validation Split...")
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

        print(f"\n[{i+1}/{n_samples}] Record ID: {item.get('id')} | Category: {item.get('category')}")
        print(f"  Query: {user_msg.splitlines()[0]}")
        
        t0 = time.perf_counter()
        res = agent.run(user_msg[:120])
        elapsed_ms = (time.perf_counter() - t0) * 1000
        
        print(f"  Latency: {elapsed_ms:.1f} ms | RAM: {res.get('peak_ram_mb')} MB | TPS: {res.get('decode_tps')}")
        print(f"  Grounding Reference: \"{expected_asst[:120]}...\"")

if __name__ == "__main__":
    print_dataset_summary()
    evaluate_sample_inferences(3)
