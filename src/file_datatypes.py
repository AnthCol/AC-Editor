from dataclasses import dataclass

@dataclass
class SavedFile:
    path:    str = None
    rank:    int = None

    def __init__(self, path, rank):
        self.path = path
        self.rank = rank

@dataclass
class UnsavedFile:
    content: str = None
    rank:    int = None

    def __init__(self, content, rank):
        self.content = content
        self.rank = rank
