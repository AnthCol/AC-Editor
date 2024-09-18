from classes.file import File

def end(window):
    window.destroy()

def extract_file(db_file):
    path, name, rank, content, is_unsaved = db_file
    file = File(path=path,
                name=name,
                rank=rank,
                content=content,
                is_unsaved=is_unsaved)
    return file

