class VimController:
    NORMAL = 0
    INSERT = 1
    mode = NORMAL
    insert_message = "--INSERT--"
    normal_message = "--NORMAL--"
    message = normal_message
    buffer = ""

    def display_message(self, label):
        label.config(text=self.message)
        label.pack()