"""MCP connector cho Claude Desktop: ghi âm giọng nói và nhận dạng bằng faster-whisper.

Đăng ký server này trong claude_desktop_config.json (xem README.md). Sau khi khởi
động lại Claude Desktop, bạn có thể nói trực tiếp trong hội thoại, ví dụ:
"bắt đầu ghi âm giúp tôi" -> nói -> "dừng ghi âm và đọc lại giúp tôi".
"""

import sys
import threading

from mcp.server.fastmcp import FastMCP

from app.config import load_config
from app.recorder import Recorder
from app.transcriber import Transcriber

config = load_config()
mcp = FastMCP("speech-to-text-vi")

_recorder = Recorder(sample_rate=config["sample_rate"])
_lock = threading.Lock()
_recording = False
_transcriber = None  # tải lười (lazy) để Claude Desktop khởi động server nhanh hơn


def _get_transcriber() -> Transcriber:
    global _transcriber
    if _transcriber is None:
        _transcriber = Transcriber(
            model_size=config["model_size"],
            device=config["device"],
            compute_type=config["compute_type"],
            language=config["language"],
        )
    return _transcriber


@mcp.tool()
def start_recording() -> str:
    """Bắt đầu ghi âm từ microphone của người dùng. Gọi tool này khi người dùng
    yêu cầu bắt đầu nói/ghi âm. Sau khi người dùng nói xong, gọi
    stop_recording_and_transcribe để lấy văn bản."""
    global _recording
    with _lock:
        if _recording:
            return "Đang ghi âm rồi, chưa cần bắt đầu lại."
        _recorder.start()
        _recording = True
    return "Đã bắt đầu ghi âm. Hãy nói, và cho tôi biết khi nào bạn nói xong để tôi dừng ghi và nhận dạng."


@mcp.tool()
def stop_recording_and_transcribe() -> str:
    """Dừng ghi âm và trả về văn bản tiếng Việt đã nhận dạng được từ giọng nói
    vừa ghi. Chỉ gọi sau khi đã gọi start_recording trước đó."""
    global _recording
    with _lock:
        if not _recording:
            return "Chưa có bản ghi âm nào đang chạy. Hãy gọi start_recording trước."
        audio = _recorder.stop()
        _recording = False
    if audio.size == 0:
        return "Không ghi được âm thanh nào."
    text = _get_transcriber().transcribe(audio)
    return text or "Không nhận dạng được nội dung nào, có thể do im lặng hoặc micro lỗi."


@mcp.tool()
def cancel_recording() -> str:
    """Hủy bản ghi âm đang chạy mà không nhận dạng, dùng khi người dùng đổi ý."""
    global _recording
    with _lock:
        if not _recording:
            return "Không có bản ghi âm nào đang chạy để hủy."
        _recorder.discard()
        _recording = False
    return "Đã hủy bản ghi âm."


if __name__ == "__main__":
    print("[*] Speech-to-text MCP server đang chạy (stdio)...", file=sys.stderr)
    mcp.run()
