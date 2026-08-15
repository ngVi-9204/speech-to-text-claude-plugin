from pynput.keyboard import Key, KeyCode


def parse_key(name: str):
    """Chuyển chuỗi cấu hình (vd: 'f9', 'esc', 'a') thành đối tượng phím của pynput."""
    if name is None:
        return None
    name = name.strip().lower().strip("<>")
    special = getattr(Key, name, None)
    if special is not None:
        return special
    if len(name) == 1:
        return KeyCode.from_char(name)
    raise ValueError(f"Không nhận diện được phím trong cấu hình: '{name}'")
