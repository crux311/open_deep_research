#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export RAINDROP_LOCAL_DEBUGGER="${RAINDROP_LOCAL_DEBUGGER:-http://localhost:5899/v1/}"

if command -v raindrop >/dev/null 2>&1; then
  raindrop workshop start >/dev/null
elif [[ -x "$HOME/.raindrop/bin/raindrop" ]]; then
  "$HOME/.raindrop/bin/raindrop" workshop start >/dev/null
else
  echo "Raindrop CLI not found. Install with: curl -fsSL https://raindrop.sh/install | bash" >&2
  exit 1
fi

echo "Raindrop Workshop: http://localhost:5899"
echo "LangGraph API:      http://127.0.0.1:2024"
echo "LangGraph Docs:     http://127.0.0.1:2024/docs"
echo "LangGraph Studio:   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024"
echo

exec uv run langgraph dev --allow-blocking --no-browser --no-reload
