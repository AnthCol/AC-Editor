from PIL import Image, ImageTk

def make_icon(path):
    with Image.open(path) as image:
        icon = ImageTk.PhotoImage(image)
    return icon


def pad(string):
    if string != None:
        return "    " + string + "    "