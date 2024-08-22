from dataclasses import dataclass

@dataclass
class VimController:
    NORMAL = 0
    INSERT = 1
    mode = NORMAL
    buffer = ""




