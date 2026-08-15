import pathlib
import yaml

DEFAULT_CONFIG = {
    "mode": "hotkey",  # "hotkey" hoặc "vad" (tự động phát hiện giọng nói)
    "hotkey": "f9",
    "cancel_key": "esc",
    "toggle_key": "f9",  # dùng ở mode "vad": bật/tắt lắng nghe tự động
    "language": "vi",
    "model_size": "small",
    "device": "cpu",
    "compute_type": "int8",
    "auto_paste": True,
    "sample_rate": 16000,
    "vad_threshold": 0.02,
    "vad_silence_ms": 800,
    "vad_min_speech_ms": 300,
    "vad_max_utterance_s": 30,
}

CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"


def load_config():
    config = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        config.update(user_config)
    return config
