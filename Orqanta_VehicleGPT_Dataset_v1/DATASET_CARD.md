# Dataset card: Orqanta VehicleGPT

- Version: 1.0
- Purpose: starter SFT data for a local/offline natural-language vehicle information assistant.
- Total records: 360
- Format: JSONL chat messages plus CSV.
- Data origin: synthetically authored examples using illustrative values; no real driver or vehicle data.
- Intended use: prototype fine-tuning, prompt-behavior tests, and evaluation-pipeline development.
- Not intended for: safety certification, direct vehicle control, definitive diagnosis, or production use without validation.

## Coverage
Range trends, energy efficiency comparisons, ADAS/event timelines, battery thermal warnings, diagnostic trouble-code interpretation, missing-data responses, ingestion strategies for CAN/CAN-FD, SOME/IP, Android Vehicle HAL and QNX logs, safety/privacy boundaries, multi-record comparisons, and event filtering.

## Limitations
1. Synthetic records do not represent the distribution of a real vehicle fleet.
2. Answers can reflect the assumptions embedded in each example; domain expert review is required.
3. Generic DTC descriptions are not vehicle-specific service instructions.
4. The data is not a substitute for actual searchable telemetry. Runtime retrieval must provide the records needed for each answer.
5. No claim is made that this dataset alone will deliver sub-2-second latency, weeks of history, or reliable on-device inference. Those depend on model, hardware, indexing, and system design.

## Recommended evaluation
Keep the test split untouched until final evaluation. Score grounding, correctness against records, uncertainty when fields are missing, safety-policy compliance, and latency separately. Add a held-out test set based on new scenario templates and real/simulator-generated telemetry after schema validation.
