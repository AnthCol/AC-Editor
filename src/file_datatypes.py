# Path represents the file path that the program will load from
# Content represents the contents of the file
# Rank represents the order in which they are to be presented as tabs within the editor
# Name represents the file name that is to be displayed on the tab in the editor

class SavedFile:
    def __init__(self, path, rank, name):
        self.path = path
        self.rank = rank
        self.name = name

class UnsavedFile:
    def __init__(self, content, rank, name):
        self.content = content
        self.rank = rank
        self.name = name
