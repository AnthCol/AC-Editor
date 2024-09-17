NORMAL = 0 
INSERT = 1
INSERT_MESSAGE = "--INSERT--    |    "
NORMAL_MESSAGE = "--NORMAL--    |    "
EMPTY_BUFFER = ""

class VimController: 
    def __init__(self):
        self.mode = NORMAL
        self.mode_message = NORMAL_MESSAGE
        self.command_buffer = EMPTY_BUFFER
        self.message = self.mode_message + self.command_buffer

    # def append_buffer(self, char):
    #     self.command_buffer += char

    # def update_display(self):
    #     text = self.mode_message + self.command_buffer
    #     self.label.config(text=text)

    # def delete_char(self):
    #     self.command_buffer = self.command_buffer[:-1]
    #     self.update_display()

    # def reset_buffer(self):
    #     self.mode_message = NORMAL_MESSAGE if (self.mode == NORMAL) else INSERT_MESSAGE
    #     self.command_buffer = EMPTY_BUFFER
    #     self.update_display()

    # def switch_normal(self):
    #     self.mode = NORMAL
    #     self.reset_buffer()

    # def switch_insert(self):
    #     self.mode = INSERT
    #     self.reset_buffer()
