# Orqanta Orqanta-AI Two-Wheeler Assistant Dataset

Version: 1.0
Total examples: 380
- Train: 304
- Validation: 35
- Test: 41

## Supported vehicle categories
- Electric scooter
- Petrol scooter
- Electric motorcycle
- Petrol motorcycle

## Coverage
Electric range and charging; petrol mileage; trip comparison; maintenance reminders; diagnostic/warning explanation; safety-critical situations; voice/tool intents; missing-data handling; privacy and data boundaries.

## Format
Each JSONL row contains `id`, `category`, `vehicle_type`, `difficulty`, and `messages` in system/user/assistant chat format. CSV is provided for inspection and transformation.

## Important limitations
All examples are synthetic. They are useful for prototyping response behavior and testing data pipelines, not for teaching exact model-specific specifications or validating real diagnoses. Values are illustrative. Verify against the specific vehicle manual, real telemetry schemas, and domain experts before deployment.

This dataset is not an ECU/vehicle-control dataset. Never use it to train or authorize direct throttle, brake, steering, ignition, BMS, or other safety-critical control. The AI should be an informational/diagnostic assistant isolated from control systems.

## Recommended architecture
Use the model to classify intent, extract entities, and produce validated tool calls. Keep trip records, service history, DTCs, and telemetry in local storage. Retrieve relevant records at inference time and have the model explain them. Tool calls must be allow-listed, permission-checked, schema-validated, and confirmed by the device/app.

## Training advice
Start with a compatible pretrained instruction model and LoRA/QLoRA if using an LLM. If Orqanta is a compact intent/tool-call model, convert examples to its actual schema. Do not assume these JSONL chat records are directly compatible with the existing `.cact` format. Keep the test split untouched and add held-out, real or simulator-generated cases before claiming performance.
