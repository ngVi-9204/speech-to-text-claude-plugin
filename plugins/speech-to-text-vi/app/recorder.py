import numpy as np
import sounddevice as sd


class Recorder:
    """Ghi âm micro trong một luồng nền cho tới khi được yêu cầu dừng."""

    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self._frames = []
        self._stream = None

    def start(self):
        self._frames = []
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, indata, frames, time_info, status):
        self._frames.append(indata.copy())

    def stop(self) -> np.ndarray:
        if self._stream is None:
            return np.zeros((0,), dtype="float32")
        self._stream.stop()
        self._stream.close()
        self._stream = None
        if not self._frames:
            return np.zeros((0,), dtype="float32")
        audio = np.concatenate(self._frames, axis=0).flatten()
        self._frames = []
        return audio

    def discard(self):
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._frames = []
