import json
from dataclasses import dataclass, asdict


@dataclass
class Settings:
    colour: str = "monokai"
    font_type: str = "Consolas"
    font_size: int = 12

    

    # def load(self):
    #     try:
    #         with open(self.SETTINGS_PATH, "r") as f:
    #             data = f.read()
    #             if data:
    #                 data = json.loads(data)
    #                 self.colour = data.get("colour", self.colour)
    #                 self.font_type = data.get("font_type", self.font_type)
    #                 self.font_size = data.get("font_size", self.font_size)
    #     except FileNotFoundError:
    #         print("File not found. Using default settings.\n") 
    #     return 

    # def save(self):
    #     with open(self.SETTINGS_PATH, "w") as f:
    #         json.dump(asdict(self), f)
