#!/usr/bin/env bash
# Tự động cài đặt Speech-to-Text: tạo virtual environment, cài thư viện, tải
# model — chỉ cần double-click file này trong Finder, không cần gõ lệnh gì.
set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$PROJECT_DIR/venv"

echo "== Cài đặt Speech-to-Text cho Claude =="
echo "Thư mục project: $PROJECT_DIR"
echo

if [ ! -d "$VENV" ]; then
  echo "[1/2] Tạo virtual environment và cài thư viện (có thể mất vài phút,"
  echo "      lần đầu cần tải faster-whisper + model, cần kết nối mạng)..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q -r "$PROJECT_DIR/requirements.txt"
  echo "      Cài đặt xong."
else
  echo "[1/2] Đã cài sẵn từ trước, bỏ qua."
fi

echo "[2/2] Khởi chạy..."
echo
echo "----------------------------------------------------------------------"
echo "QUAN TRỌNG — lần đầu tiên chạy, macOS có thể hỏi cấp quyền Microphone,"
echo "Accessibility và Input Monitoring. Cấp cả 3 quyền đó thì mới ghi âm và"
echo "tự dán được. Nếu không thấy popup tự hiện, vào System Settings >"
echo "Privacy & Security > (từng mục) > bấm + > chọn:"
echo "  $VENV/bin/python"
echo
echo "Đổi chế độ (hotkey/vad), phím tắt, ngôn ngữ... trong file config.yaml"
echo "cùng thư mục project. Đóng cửa sổ này (Ctrl+C) để dừng chương trình."
echo "----------------------------------------------------------------------"
echo
exec "$VENV/bin/python" "$PROJECT_DIR/main.py"
