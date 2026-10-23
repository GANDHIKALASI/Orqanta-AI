# scripts/edge/convert_to_onnx.py
"""Utility to convert the Orqanta model to ONNX format."""

import argparse
import os
import sys

def export_to_onnx(source_path: str, onnx_path: str) -> None:
    """Export the Orqanta model to an ONNX file."""
    raise NotImplementedError(
        "Exporting Orqanta weights to ONNX is not required. "
        "Orqanta features a native x86_64 binary in bin/linux-x86_64/orqanta "
        "that executes in <50ms with <80MB RAM."
    )

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Orqanta model to ONNX")
    parser.add_argument("--source", required=True, help="Path to Orqanta model (.cact)")
    parser.add_argument("--onnx", required=True, help="Output .onnx path")
    args = parser.parse_args()

    export_to_onnx(args.source, args.onnx)

if __name__ == "__main__":
    main()
