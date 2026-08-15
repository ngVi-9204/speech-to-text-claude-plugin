# Speech-to-Text cho Claude (faster-whisper)

Hai cách dùng, chọn 1 hoặc dùng cả hai:

- **Chế độ hotkey** (mục 1-6 bên dưới): nhấn phím tắt để ghi âm, nhấn lại để dừng —
  tự động dán văn bản vào ô đang gõ ở bất kỳ ứng dụng nào (Claude Desktop, Claude
  web, Claude Code trong terminal...).
- **Chế độ MCP connector cho Claude Desktop** (mục 7): không cần phím tắt, không
  cần double-click app nào — bạn chỉ cần nói trong hội thoại Claude Desktop
  ("bắt đầu ghi âm giúp tôi" ... "dừng lại và đọc cho tôi") và Claude sẽ tự gọi
  công cụ ghi âm/nhận dạng.

## 1. Cài đặt

Yêu cầu: Python 3.10+.

### Windows
```bash
run.bat
```
Lần chạy đầu sẽ tự tạo virtual environment và cài thư viện (mất vài phút vì phải
tải model faster-whisper lần đầu tiên).

### macOS
```bash
chmod +x run.sh
./run.sh
```

Nếu muốn cài thủ công thay vì dùng script:
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 2. Cấp quyền (bắt buộc trên macOS)

macOS chặn việc theo dõi phím tắt toàn cục và mô phỏng phím dán theo mặc định.
Vào **System Settings → Privacy & Security** và cấp quyền cho ứng dụng Terminal
(hoặc iTerm/trình chạy Python bạn dùng) ở hai mục:
- **Microphone** — để ghi âm.
- **Accessibility** — để mô phỏng phím Cmd+V (tự động dán).
- **Input Monitoring** — để nhận phím tắt toàn cục (F9).

Trên Windows thường không cần cấp quyền gì thêm.

## 3. Sử dụng

Có 2 chế độ, chọn bằng trường `mode` trong [config.yaml](config.yaml).

### Chế độ `hotkey` (thủ công, mặc định)

1. Chạy `run.bat` (Windows) hoặc `./run.sh` (macOS). Đợi dòng "Model đã sẵn sàng."
2. Click vào ô nhập liệu trong Claude (Desktop app, trình duyệt, hoặc terminal
   đang chạy Claude Code).
3. Nhấn **F9** để bắt đầu ghi âm, nói, rồi nhấn **F9** lần nữa để dừng.
4. Văn bản nhận dạng được sẽ tự động dán vào đúng vị trí con trỏ.
5. Nhấn **Esc** trong lúc đang ghi âm để hủy bỏ, không dán gì cả.
6. Nhấn **Ctrl+C** trong cửa sổ terminal để thoát chương trình.

### Chế độ `vad` (tự động, không cần bấm/nói "bắt đầu")

Đặt `mode: "vad"` trong `config.yaml`, rồi chạy như trên. Công cụ lắng nghe
micro liên tục: hễ bạn nói là tự ghi, im lặng khoảng `vad_silence_ms` là tự
dừng, nhận dạng và tự dán — không cần thao tác gì trong lúc nói.

- Click vào ô nhập liệu Claude trước khi nói (văn bản dán vào nơi đang focus).
- Nhấn phím `toggle_key` (mặc định cũng F9) để **tạm dừng/bật lại** việc lắng
  nghe — nên tắt đi khi không dùng để tránh ghi nhầm lúc gọi điện, nói chuyện
  xung quanh.
- Nếu bị bắt nhầm tiếng ồn nền hoặc bỏ sót câu nói khẽ, chỉnh `vad_threshold`
  trong `config.yaml` (tăng lên nếu bắt nhầm ồn, giảm xuống nếu bỏ sót giọng nói).

## 4. Cấu hình

Chỉnh sửa [config.yaml](config.yaml):

| Trường | Ý nghĩa |
|---|---|
| `mode` | `hotkey` (thủ công) hoặc `vad` (tự động phát hiện giọng nói) |
| `hotkey` | Phím bật/tắt ghi âm ở mode `hotkey` (mặc định `f9`) |
| `cancel_key` | Phím hủy bản ghi hiện tại ở mode `hotkey` (mặc định `esc`) |
| `toggle_key` | Phím tạm dừng/bật lại lắng nghe ở mode `vad` (mặc định `f9`) |
| `vad_threshold` | Ngưỡng âm lượng RMS để coi là "đang nói" ở mode `vad` (mặc định `0.02`) |
| `vad_silence_ms` | Im lặng bao lâu (ms) thì coi là nói xong, tự dừng (mặc định `800`) |
| `vad_min_speech_ms` | Bỏ qua đoạn ghi ngắn hơn mức này, lọc tiếng ồn (mặc định `300`) |
| `vad_max_utterance_s` | Giới hạn tối đa một lượt nói (giây), tránh ghi vô hạn (mặc định `30`) |
| `language` | `vi`, `en`, hoặc để trống (`null`) để tự động phát hiện ngôn ngữ |
| `model_size` | `tiny` / `base` / `small` / `medium` / `large-v3` — model càng lớn càng chính xác nhưng càng chậm |
| `device` | `cpu` hoặc `cuda` (nếu có GPU NVIDIA hỗ trợ) |
| `compute_type` | `int8` cho CPU, `float16` cho GPU |
| `auto_paste` | `true` để tự dán, `false` nếu chỉ muốn copy vào clipboard |

Lần chạy đầu tiên với mỗi `model_size`, `faster-whisper` sẽ tự tải model về máy
(lưu cache tại `~/.cache/huggingface`) nên cần kết nối mạng; các lần sau chạy
hoàn toàn offline.

## 5. Cấu trúc dự án

```
main.py              # Điểm khởi động, vòng lặp lắng nghe phím tắt
app/config.py         # Đọc config.yaml
app/recorder.py        # Ghi âm micro (sounddevice)
app/transcriber.py     # Nhận dạng giọng nói (faster-whisper)
app/inserter.py         # Copy vào clipboard + mô phỏng phím dán
app/hotkeys.py          # Chuyển tên phím trong config thành phím pynput
config.yaml           # Cấu hình người dùng
```

## 6. Xử lý sự cố

- **Không ghi được âm thanh / lỗi PortAudio**: cài lại `sounddevice`
  (`pip install --force-reinstall sounddevice`) hoặc kiểm tra micro mặc định
  trong Sound Settings của hệ điều hành.
- **Phím tắt không phản hồi trên macOS**: kiểm tra lại quyền Input Monitoring
  và Accessibility ở bước 2, sau đó khởi động lại Terminal.
- **Nhận dạng chậm**: đổi `model_size` sang `base` hoặc `tiny` trong
  `config.yaml`.
- **Dán nhầm vào cửa sổ khác**: đảm bảo ô nhập liệu Claude đang được focus
  *trước khi* nhấn F9 lần thứ hai để dừng ghi âm.

## 7. Dùng như MCP connector cho Claude Desktop (không cần phím tắt, không cần mở app riêng)

Đây là cách tích hợp trực tiếp vào Claude Desktop dưới dạng "connector": Claude
Desktop sẽ tự khởi động tiến trình `mcp_server.py` ở nền mỗi khi mở app — bạn
không cần tự chạy `run.bat`/`run.sh` hay double-click gì cả, chỉ cần khai báo
một lần trong file cấu hình.

### 7.1. Cài thư viện trước một lần

```bash
python -m venv venv
# Windows: venv\Scripts\activate      macOS: source venv/bin/activate
pip install -r requirements.txt
```

### 7.2. Lấy đường dẫn Python trong venv

- Windows: `C:\đường-dẫn-tới-project\venv\Scripts\python.exe`
- macOS: `/đường-dẫn-tới-project/venv/bin/python`

Phải dùng đường dẫn Python **bên trong venv** (không phải `python` suông), vì
Claude Desktop chạy lệnh trực tiếp, không tự kích hoạt venv giúp bạn.

### 7.3. Khai báo connector trong claude_desktop_config.json

Mở file cấu hình:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Thêm (hoặc gộp vào) mục `mcpServers`:

```json
{
  "mcpServers": {
    "speech-to-text-vi": {
      "command": "C:\\đường-dẫn-tới-project\\venv\\Scripts\\python.exe",
      "args": ["C:\\đường-dẫn-tới-project\\mcp_server.py"]
    }
  }
}
```

Trên macOS thay bằng đường dẫn kiểu Unix, ví dụ:

```json
{
  "mcpServers": {
    "speech-to-text-vi": {
      "command": "/Users/ban/speech-to-text-claude/venv/bin/python",
      "args": ["/Users/ban/speech-to-text-claude/mcp_server.py"]
    }
  }
}
```

Khởi động lại Claude Desktop. Vào phần connector/tool trong Claude Desktop kiểm
tra thấy `speech-to-text-vi` với 3 tool: `start_recording`,
`stop_recording_and_transcribe`, `cancel_recording`.

### 7.4. Cách nói chuyện với nó

Trong ô chat Claude Desktop, gõ (hoặc nói bằng dictation của OS) ví dụ:

> "Bắt đầu ghi âm giúp tôi"

Claude sẽ gọi `start_recording`. Bạn nói nội dung cần nhập, rồi gõ tiếp:

> "Xong rồi, dừng ghi âm và cho tôi xem văn bản"

Claude gọi `stop_recording_and_transcribe` và trả về đúng văn bản tiếng Việt đã
nhận dạng, bạn có thể yêu cầu Claude dùng luôn nội dung đó để trả lời/viết tiếp.

**Lưu ý:** đây là kiểu tương tác qua hội thoại (Claude chủ động gọi tool khi bạn
yêu cầu bằng lời/chữ), khác với chế độ hotkey ở trên vốn dán trực tiếp vào con
trỏ chuột theo thời gian thực. Nếu cần dán tức thì vào bất kỳ ứng dụng nào, dùng
chế độ hotkey; nếu chỉ cần nói chuyện với riêng Claude Desktop mà không muốn mở
thêm cửa sổ nào, dùng connector này.
