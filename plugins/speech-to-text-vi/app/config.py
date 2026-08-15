import pathlib
import yaml

DEFAULT_CONFIG = {
    "hotkey": "f9",
    "cancel_key": "esc",
    "language": "vi",
    "model_size": "small",
    "device": "cpu",
    "compute_type": "int8",
    "auto_paste": True,
    "sample_rate": 16000,
}

CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"


def load_config():
    config = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        config.update(user_config)
    return config
