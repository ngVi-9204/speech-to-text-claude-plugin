import sys
import threading

from pynput import keyboard as pkeyboard

from app.config import load_config
from app.hotkeys import parse_key
from app.inserter import copy_and_paste
from app.recorder import Recorder
from app.transcriber import Transcriber


class App:
    def __init__(self, config: dict):
        self.config = config
        self.hotkey = parse_key(config["hotkey"])
        self.cancel_key = parse_key(config["cancel_key"])
        self.recorder = Recorder(sample_rate=config["sample_rate"])
        self.transcriber = Transcriber(
            model_size=config["model_size"],
            device=config["device"],
            compute_type=config["compute_type"],
            language=config["language"],
        )
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
        print("Speech-to-Text cho Claude — đã sẵn sàng.")
        print(f"Phím tắt bật/tắt ghi âm: {self.config['hotkey']}")
        print(f"Phím hủy: {self.config['cancel_key']}")
        print("Nhấn Ctrl+C trong cửa sổ này để thoát chương trình.")
        print("=" * 60)
        with pkeyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


def main():
    config = load_config()
    app = App(config)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nĐã thoát.")
        sys.exit(0)


if __name__ == "__main__":
    main()
