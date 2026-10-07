#!/usr/bin/env bash
set -eu

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJECT_ROOT"

if [ -z "${PYTHON_BIN:-}" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN=python3
    else
        PYTHON_BIN=python
    fi
fi

echo "Iniciando servidores RPC nas portas 9000, 9001 e 9002..."
"$PYTHON_BIN" src/servidor_encurtador.py 0 &
PID_0=$!
"$PYTHON_BIN" src/servidor_encurtador.py 1 &
PID_1=$!
"$PYTHON_BIN" src/servidor_encurtador.py 2 &
PID_2=$!

cleanup() {
    kill "$PID_0" "$PID_1" "$PID_2" 2>/dev/null || true
}
trap cleanup INT TERM EXIT
wait
