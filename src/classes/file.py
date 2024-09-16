# Files can change state from saved to unsaved while the user types in them. 
# This explains the dual nature of this class. 

class File:
    def __init__(self, path, name, rank, content, is_unsaved):
        self.path = path if path != None else ""
        self.name = name
        self.rank = rank
        self.content = content if content != None else ""
        self.is_unsaved = True if content != None else False
