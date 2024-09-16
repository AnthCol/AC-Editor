import os
import pygments.lexers

from .file import File

def update_files(containers):
    # rank = 1
    # for c in containers:
    #     if isinstance(c.file, UnsavedFile):
    #         c.file.content = c.codeview.get("1.0", "end-1c")
    #     c.file.rank = rank
    #     rank += 1
    return

# FIXME there has to be a better way to do this
def unsaved_rank(containers):
    # values = []
    # for c in containers:
    #     if isinstance(c.file, UnsavedFile):
    #         values.append(int(c.file.name.split()[1]))
    # values.sort()
    # count = 1 
    # for v in values:
    #     if v != count:
    #         break
    #     count += 1
    # return str(count)
    return


def determine_lexer(file):
    # lexer = pygments.lexers.TextLexer
    # if isinstance(file, SavedFile):
    #     try:
    #         lexer = pygments.lexers.get_lexel_for_filename(os.path.basename(file.path))
    #     except:
    #         lexer = pygments.lexers.TextLexer
    # return lexer
    return

def determine_rank(containers):
    return 1 + len(containers)

def codeview_contents(codeview):
    return codeview.get("1.0", "end-1c")

# FIXME might not work.
def remove_file(file_interface, index):
    del file_interface.containers[index]
    file_interface.notebook.forget(index)


