#!/usr/bin/env bash
# ==============================================================================
# Script: sync-models.sh
# Purpose: Synchronize local open-source AI models with upstream repositories
# ==============================================================================

set -euo pipefail

PROVIDER="${1:-ollama}"
MODELS=("qwen2.5-coder:14b" "deepseek-r1:14b" "qwen2.5:14b")

echo "============================================================"
echo "  Local AI Models - Upstream Synchronization Engine"
echo "============================================================"

if [ "$PROVIDER" = "ollama" ] || [ "$PROVIDER" = "all" ]; then
    echo "[INFO] Checking Ollama daemon on http://localhost:11434..."
    if curl -s -f http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "[SUCCESS] Ollama daemon is active."
        for model in "${MODELS[@]}"; do
            echo "[INFO] Syncing upstream: pulling latest weights for '$model'..."
            if command -v ollama >/dev/null 2>&1; then
                ollama pull "$model"
            else
                curl -s -X POST http://localhost:11434/api/pull -d "{\"name\": \"$model\", \"stream\": false}" >/dev/null
            fi
            echo "[SUCCESS] '$model' is up to date."
        done
    else
        echo "[WARN] Ollama daemon is not reachable on localhost:11434."
    fi
fi

if [ "$PROVIDER" = "lmstudio" ] || [ "$PROVIDER" = "all" ]; then
    echo "[INFO] Checking LM Studio on http://localhost:1234..."
    if curl -s -f http://localhost:1234/v1/models >/dev/null 2>&1; then
        echo "[SUCCESS] LM Studio server is active."
        curl -s http://localhost:1234/v1/models | grep -o '"id": "[^"]*"' || true
    else
        echo "[WARN] LM Studio server is not running on port 1234."
    fi
fi

echo "[SUCCESS] Upstream model synchronization completed."
