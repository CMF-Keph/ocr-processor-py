#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

project_python=".venv/bin/python"

"$project_python" -m uvicorn server:app \
    --app-dir src \
    --host 127.0.0.1 \
    --port 8000 &

api_pid=$!

cleanup() {
    kill "$api_pid" 2>/dev/null || true
}

trap cleanup EXIT

"$project_python" src/main.py