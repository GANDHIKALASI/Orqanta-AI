#!/usr/bin/env bash
# ==============================================================================
# Orqanta AI - Local HTTP Server Runner for Linux Laptops / PCs
# Starts an ultra-fast REST API server on port 8080 (<80MB RAM, CPU only)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

PORT="${1:-8080}"
BIN="${ROOT_DIR}/bin/linux-x86_64/orqanta"
MODEL="${ROOT_DIR}/models/orqanta.cact"

if [ ! -f "$BIN" ]; then
    echo "Error: Binary not found at $BIN"
    exit 1
fi

if [ ! -f "$MODEL" ]; then
    echo "Error: Model not found at $MODEL"
    exit 1
fi

echo "=========================================================="
echo " Starting Orqanta AI Microservice (Psycho Engine)"
echo " Binary: $BIN"
echo " Model:  $MODEL"
echo " Port:   http://127.0.0.1:${PORT}"
echo " Endpoint: POST http://127.0.0.1:${PORT}/complete"
echo "=========================================================="
echo ""
echo "Example query:"
echo "  curl -X POST http://127.0.0.1:${PORT}/complete \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"input\": \"Check battery and set volume to 50\"}'"
echo ""

exec "$BIN" --model "$MODEL" --tools "${SCRIPT_DIR}/laptop_tools.json" --serve --port "$PORT"
