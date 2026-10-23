# Dataset Card: Orqanta Orqanta-AI

- Total: 380 synthetic examples
- Splits: train 304, validation 35, test 41
- Intended use: prototype a local two-wheeler informational assistant for EV and petrol scooters/motorcycles.
- Out of scope: autonomous vehicle control, certified diagnostics, safety decisions, or medical advice.
- Data source: synthetically authored records and illustrative telemetry; no real rider data.
- Known limitations: model-specific procedures/specifications are not represented; examples may be templated; validate and deduplicate before fine-tuning.
- Suggested metrics: intent accuracy, slot/entity accuracy, tool-call schema validity, grounded answer correctness, missing-data calibration, safety-policy compliance, latency, and memory footprint.
