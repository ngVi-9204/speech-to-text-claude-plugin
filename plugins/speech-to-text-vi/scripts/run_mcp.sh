#!/usr/bin/env bash
# Tự tạo venv + cài thư viện ở lần chạy đầu tiên (Claude Code khởi động server này
# tự động, người dùng không cần cài đặt thủ công), sau đó chạy MCP server.
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/venv"

if [ ! -d "$VENV" ]; then
  echo "[setup] Đang tạo môi trường và cài thư viện lần đầu (có thể mất vài phút)..." >&2
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q -r "$ROOT/requirements.txt"
fi

exec "$VENV/bin/python" "$ROOT/mcp_server.py"
