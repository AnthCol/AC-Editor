from typing import List

NORMAL = 0 
INSERT = 1
INSERT_MESSAGE = "--INSERT--    |    "
NORMAL_MESSAGE = "--NORMAL--    |    "
EMPTY_BUFFER = ""


class VimBuffer:
    def __init__(self):
        self.mode = NORMAL
        self.mode_message = NORMAL_MESSAGE
        self.command_buffer = EMPTY_BUFFER

class VimController: 
    def __init__(self, label):
        self.label = label
        self.buffers : List[VimBuffer] = []

    def in_normal(self, index):
        return self.buffers[index].mode == NORMAL

    def in_insert(self, index):
        return self.buffers[index].mode == INSERT

    def append_buffer(self, char, index):
        self.buffers[index].command_buffer += char

    def new_buffer(self):
        self.buffers.append(VimBuffer())

    def update_display(self, index):
        mode = self.buffers[index].mode_message
        command = self.buffers[index].command_buffer
        text = mode + command
        self.label.config(text=text)

    def label_grid(self):
        self.label.grid(row=1, column=0, sticky="ew")

    def delete_char(self, index):
        buffer = self.buffers[index].command_buffer
        buffer = buffer[:-1]
        self.update_display(index)

    def current_command(self, index):
        buffer = self.buffers[index].command_buffer
        return buffer

    def reset_buffers(self, index):
        mode = self.buffers[index].mode
        self.buffers[index].mode_message = NORMAL_MESSAGE if (mode == NORMAL) else INSERT_MESSAGE
        self.buffers[index].command_buffer = EMPTY_BUFFER
        self.update_display(index)

    def switch_normal(self, index):
        self.buffers[index].mode = NORMAL
        self.reset_buffers(index)

    def switch_insert(self, index):
        self.buffers[index].mode = INSERT
        self.reset_buffers(index)
