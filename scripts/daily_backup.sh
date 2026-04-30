#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"${PROJECT_ROOT}/.venv/bin/python" "${PROJECT_ROOT}/scripts/backup_db.py"
