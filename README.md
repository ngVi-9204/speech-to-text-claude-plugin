# Speech-to-Text Claude Marketplace

Đây là một **Claude Code plugin marketplace** chứa 1 plugin duy nhất:
[speech-to-text-vi](plugins/speech-to-text-vi) — ghi âm giọng nói tiếng Việt và
nhận dạng bằng `faster-whisper`, chạy hoàn toàn local trên máy bạn.

## Cài đặt (trong Claude Code)

1. Mở dialog **Add marketplace** (như ảnh bạn gửi) và nhập:
   ```
   ngVi-9204/speech-to-text-claude-plugin
   ```
   hoặc chạy lệnh:
   ```
   /plugin marketplace add ngVi-9204/speech-to-text-claude-plugin
   ```
2. Cài plugin:
   ```
   /plugin install speech-to-text-vi@speech-to-text-claude-marketplace
   ```
3. Reload/khởi động lại Claude Code. Trong hội thoại, gõ hoặc nói:
   > "bắt đầu ghi âm giúp tôi" ... nói nội dung ... "dừng lại và đọc cho tôi"

Claude Code sẽ tự chạy `scripts/run_mcp.sh` trong plugin — script này tự tạo
virtualenv Python và cài `faster-whisper`/`sounddevice` ở lần đầu chạy (mất vài
phút, cần mạng để tải model + thư viện), các lần sau chạy ngay và hoàn toàn
offline.

Yêu cầu máy: Python 3.10+ (có sẵn `python3` trong PATH), microphone hoạt động,
và trên macOS cần cấp quyền **Microphone** + **Input Monitoring** cho ứng dụng
chạy Claude Code (Terminal/iTerm) trong System Settings → Privacy & Security.

## Chi tiết plugin

Xem [plugins/speech-to-text-vi/README.md](plugins/speech-to-text-vi/README.md)
để biết cấu hình (`config.yaml`), cấu trúc code, cách dùng chế độ hotkey độc lập
(không qua plugin), và cách đăng ký thủ công như MCP connector cho Claude Desktop.
