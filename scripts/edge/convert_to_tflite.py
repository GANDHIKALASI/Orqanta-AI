# scripts/edge/convert_to_tflite.py
"""Utility to convert the Orqanta AI model to TensorFlow Lite format."""

import argparse
import os
import sys

def export_to_savedmodel(source_path: str, export_dir: str) -> None:
    """Export the native Orqanta model to a TensorFlow SavedModel."""
    raise NotImplementedError(
        "Exporting Orqanta weights to TensorFlow SavedModel is not implemented. "
        "Use the native Orqanta ARM64 binary for optimal performance on Android."
    )

def convert_to_tflite(savedmodel_dir: str, tflite_path: str) -> None:
    """Convert a TensorFlow SavedModel to a .tflite file.

    Requires `tensorflow` (`pip install tensorflow` or `tensorflow-cpu`).
    The conversion options can be tuned for size vs. accuracy.
    """
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise RuntimeError(
            "TensorFlow is required for TFLite conversion. Install via `pip install tensorflow`."
        ) from exc

    converter = tf.lite.TFLiteConverter.from_saved_model(savedmodel_dir)
    # Enable optimizations for edge devices (quantization, etc.)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # For full integer quantization you would provide a representative dataset.
    # Here we keep the default to produce a float16 model.
    tflite_model = converter.convert()
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    print(f"TFLite model written to {tflite_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Needle model to TFLite")
    parser.add_argument("--source", required=True, help="Path to the Needle model file (e.g., .cact)")
    parser.add_argument("--out-dir", required=True, help="Directory to store intermediate SavedModel")
    parser.add_argument("--tflite", required=True, help="Output .tflite file path")
    args = parser.parse_args()

    # Step 1: Export to TensorFlow SavedModel (stub)
    export_to_savedmodel(args.source, args.out_dir)
    # Step 2: Convert to TFLite
    convert_to_tflite(args.out_dir, args.tflite)

if __name__ == "__main__":
    main()
