import threading
import time

import numpy as np
import sounddevice as sd


class VadListener:
    """Lắng nghe micro liên tục, tự động ghi âm khi phát hiện giọng nói và tự
    dừng khi im lặng — không cần bấm phím để bắt đầu/kết thúc từng lượt nói."""

    def __init__(
        self,
        sample_rate: int,
        threshold: float,
        silence_ms: int,
        min_speech_ms: int,
        max_utterance_s: float,
        on_utterance,
    ):
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.silence_s = silence_ms / 1000
        self.min_speech_s = min_speech_ms / 1000
        self.max_utterance_s = max_utterance_s
        self.on_utterance = on_utterance

        self.enabled = True
        self._state = "idle"  # idle | speaking
        self._frames = []
        self._speech_start = None
        self._silence_start = None
        self._stream = None

    def _callback(self, indata, frames, time_info, status):
        if not self.enabled:
            if self._state == "speaking":
                self._reset()
            return

        chunk = indata[:, 0]
        rms = float(np.sqrt(np.mean(np.square(chunk))))
        now = time.time()

        if rms >= self.threshold:
            if self._state == "idle":
                self._state = "speaking"
                self._speech_start = now
                self._frames = []
            self._frames.append(chunk.copy())
            self._silence_start = None
        elif self._state == "speaking":
            self._frames.append(chunk.copy())
            if self._silence_start is None:
                self._silence_start = now
            elif now - self._silence_start >= self.silence_s:
                self._finish_utterance()
                return

        if self._state == "speaking" and now - self._speech_start >= self.max_utterance_s:
            self._finish_utterance()

    def _reset(self):
        self._state = "idle"
        self._frames = []
        self._speech_start = None
        self._silence_start = None

    def _finish_utterance(self):
        frames = self._frames
        self._reset()
        if not frames:
            return
        audio = np.concatenate(frames, axis=0)
        duration_s = audio.size / self.sample_rate
        if duration_s < self.min_speech_s:
            return
        threading.Thread(target=self.on_utterance, args=(audio,), daemon=True).start()

    def start(self):
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        if not self.enabled:
            self._reset()
        return self.enabled
