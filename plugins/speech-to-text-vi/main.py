import sys
import threading

from pynput import keyboard as pkeyboard

from app.config import load_config
from app.hotkeys import parse_key
from app.inserter import copy_and_paste
from app.recorder import Recorder
from app.transcriber import Transcriber
from app.vad_listener import VadListener


class HotkeyApp:
    """Chế độ thủ công: bấm phím tắt để bắt đầu ghi âm, bấm lại để dừng."""

    def __init__(self, config: dict, transcriber: Transcriber):
        self.config = config
        self.transcriber = transcriber
        self.hotkey = parse_key(config["hotkey"])
        self.cancel_key = parse_key(config["cancel_key"])
        self.recorder = Recorder(sample_rate=config["sample_rate"])
        self.recording = False
        self.busy = False
        self.lock = threading.Lock()

    def on_press(self, key):
        if key == self.hotkey:
            with self.lock:
                if self.busy:
                    return
                if not self.recording:
                    self._start_recording()
                else:
                    self._stop_and_process()
        elif key == self.cancel_key and self.recording:
            with self.lock:
                self._cancel_recording()

    def _start_recording(self):
        print("\n[●] Đang ghi âm... (nhấn lại phím tắt để dừng, Esc để hủy)")
        self.recorder.start()
        self.recording = True

    def _stop_and_process(self):
        print("[■] Đã dừng ghi âm. Đang nhận dạng...")
        audio = self.recorder.stop()
        self.recording = False
        self.busy = True
        threading.Thread(target=self._process, args=(audio,), daemon=True).start()

    def _cancel_recording(self):
        print("[x] Đã hủy bản ghi âm.")
        self.recorder.discard()
        self.recording = False

    def _process(self, audio):
        try:
            text = self.transcriber.transcribe(audio)
            if text:
                print(f"[✓] Kết quả: {text}")
                copy_and_paste(text, auto_paste=self.config["auto_paste"])
            else:
                print("[!] Không nhận dạng được nội dung nào.")
        finally:
            self.busy = False

    def run(self):
        print("=" * 60)
        print("Speech-to-Text cho Claude — chế độ HOTKEY, đã sẵn sàng.")
        print(f"Phím tắt bật/tắt ghi âm: {self.config['hotkey']}")
        print(f"Phím hủy: {self.config['cancel_key']}")
        print("Nhấn Ctrl+C trong cửa sổ này để thoát chương trình.")
        print("=" * 60)
        with pkeyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


class VadApp:
    """Chế độ tự động: không cần bấm gì hay nói 'bắt đầu' — hễ nói là tự ghi,
    im lặng một khoảng là tự dừng, nhận dạng và tự dán."""

    def __init__(self, config: dict, transcriber: Transcriber):
        self.config = config
        self.transcriber = transcriber
        self.toggle_key = parse_key(config["toggle_key"])
        self.listener = VadListener(
            sample_rate=config["sample_rate"],
            threshold=config["vad_threshold"],
            silence_ms=config["vad_silence_ms"],
            min_speech_ms=config["vad_min_speech_ms"],
            max_utterance_s=config["vad_max_utterance_s"],
            on_utterance=self._on_utterance,
        )

    def _on_utterance(self, audio):
        print("\n[…] Phát hiện giọng nói, đang nhận dạng...")
        text = self.transcriber.transcribe(audio)
        if text:
            print(f"[✓] Kết quả: {text}")
            copy_and_paste(text, auto_paste=self.config["auto_paste"])
        else:
            print("[!] Không nhận dạng được nội dung nào.")

    def on_press(self, key):
        if key == self.toggle_key:
            enabled = self.listener.toggle()
            state = "[🎤] Đang lắng nghe tự động..." if enabled else "[⏸] Đã tạm dừng lắng nghe."
            print(state)

    def run(self):
        print("=" * 60)
        print("Speech-to-Text cho Claude — chế độ TỰ ĐỘNG (VAD), đã sẵn sàng.")
        print("Cứ nói bình thường, công cụ tự ghi và tự dán — không cần bấm gì.")
        print(f"Phím {self.config['toggle_key']}: tạm dừng / bật lại việc lắng nghe.")
        print("Nếu bắt nhầm tiếng ồn hoặc bỏ sót câu nói, chỉnh 'vad_threshold' trong config.yaml.")
        print("Nhấn Ctrl+C trong cửa sổ này để thoát chương trình.")
        print("=" * 60)
        self.listener.start()
        with pkeyboard.Listener(on_press=self.on_press) as key_listener:
            key_listener.join()


def main():
    config = load_config()
    transcriber = Transcriber(
        model_size=config["model_size"],
        device=config["device"],
        compute_type=config["compute_type"],
        language=config["language"],
    )
    app_cls = VadApp if config.get("mode") == "vad" else HotkeyApp
    app = app_cls(config, transcriber)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nĐã thoát.")
        sys.exit(0)


if __name__ == "__main__":
    main()
