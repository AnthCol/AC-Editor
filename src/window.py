

def bind_window(window):
    return

def update_title(window, file):
    title = file.name if file.is_unsaved else file.path
    window.title("ac_editor - " + title)

