from dataclasses import dataclass

@dataclass
class SavedFile:
    path: str = None
    rank: int = None
    name: str = None

    def __init__(self, path: str, rank: int, name: str):
        self.path = path
        self.rank = rank
        self.name = name

@dataclass
class UnsavedFile:
    content: str = None
    rank:    int = None
    name:    str = None

    def __init__(self, content: str, rank: int, name: str):
        self.content = content
        self.rank = rank
        self.name = name
