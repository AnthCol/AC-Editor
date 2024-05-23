from dataclasses import dataclass

# Path represents the file path that the program will load from
# Content represents the 
# Rank represents the order in which they are to be presented as tabs within the editor
# Name represents the file name that is to be displayed on the tab in the editor

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
