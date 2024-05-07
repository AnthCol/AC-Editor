import json
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    colour: str = "monokai"
    font_type: str = "Consolas"
    font_size: int = 12
