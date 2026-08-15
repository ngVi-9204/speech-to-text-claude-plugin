import sys

import numpy as np
from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self, model_size: str, device: str, compute_type: str, language: str | None):
        # In ra stderr, không phải stdout: khi chạy như MCP server, stdout là
        # kênh giao tiếp JSON-RPC với Claude Desktop, in nhầm ra đó sẽ làm hỏng kết nối.
        print(f"[*] Đang tải model faster-whisper '{model_size}' ({device}/{compute_type})...", file=sys.stderr)
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.language = language
        print("[*] Model đã sẵn sàng.", file=sys.stderr)

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size == 0:
            return ""
        segments, _info = self.model.transcribe(
            audio,
            language=self.language,
            vad_filter=True,
            beam_size=5,
        )
        return "".join(segment.text for segment in segments).strip()
