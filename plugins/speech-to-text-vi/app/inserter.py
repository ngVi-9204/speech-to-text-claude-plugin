import sys
import time

import pyperclip
from pynput.keyboard import Controller, Key

_controller = Controller()


def copy_and_paste(text: str, auto_paste: bool):
    if not text:
        return
    pyperclip.copy(text)
    if not auto_paste:
        return

    # Nhường một chút thời gian để phím hotkey được nhả ra hoàn toàn
    # trước khi giả lập tổ hợp phím dán, tránh xung đột phím.
    time.sleep(0.1)

    modifier = Key.cmd if sys.platform == "darwin" else Key.ctrl
    with _controller.pressed(modifier):
        _controller.press("v")
        _controller.release("v")
