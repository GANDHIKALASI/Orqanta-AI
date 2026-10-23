# Orqanta VehicleGPT starter fine-tuning dataset

## What this is
A compact, synthetic supervised fine-tuning (SFT) starter dataset for the VehicleGPT case study: natural-language querying over local vehicle telemetry, event logs, diagnostic records, trend comparisons, and safe handling of missing data.

Total examples: 360
- Train: 288
- Validation: 36
- Test: 36

The examples are synthetic and are not real vehicle telemetry or validated automotive diagnoses. Review and validate before using in a demo or production system.

## Files
- `train.jsonl`, `validation.jsonl`, `test.jsonl`: chat-message format, one JSON object per line.
- `vehiclegpt_dataset.csv`: flat format for inspection and quick data review.
- `DATASET_CARD.md`: scope, assumptions, limitations, and recommended use.
- `sample_preview.json`: a few examples for inspection.

## Recommended use
Use this as an initial SFT dataset to teach response style, grounding, event summarization, comparison, uncertainty, privacy, and safety boundaries. It does NOT teach the model actual vehicle-specific facts or replace retrieval over live/local records. At inference time, query a local database/search layer and pass the relevant retrieved records into the prompt.

For a small on-device model, start with parameter-efficient fine-tuning (LoRA/QLoRA) of a compatible pretrained instruct model rather than training a language model from scratch. Split by scenario or source when evaluating generalization; do not evaluate on near-duplicates of training examples.

## Important safety note
This dataset is for a non-control, informational assistant only. Keep AI inference isolated from braking, steering, battery management, ADAS actuation, and other safety-critical control functions. Do not treat generated explanations as authoritative fault diagnosis.
