import re

NORMAL = 0 
INSERT = 1
INSERT_MESSAGE = "--INSERT--    |    "
NORMAL_MESSAGE = "--NORMAL--    |    "


class VimController:
    
    def __init__(self, label):
        self.mode = NORMAL
        self.buffer = NORMAL_MESSAGE
        self.label = label
        self.valid_commands = {
            "[0-9]+h" : lambda: 10,
            "[0-9]+j" : lambda: 10,
            "[0-9]+k" : lambda: 10,
            "[0-9]+l" : lambda: 10,
            "i"       : lambda: 10,
            "A"       : lambda: 10,
            "\^"      : lambda: 10,
            "\$"      : lambda: 10, 
            ":w"      : lambda: 10,
            ":q"      : lambda: 10, 
            ":wq"     : lambda: 10, 
            ":q!"     : lambda: 10, 
            "gg"      : lambda: 10,
            "G"       : lambda: 10
        }

    def display_message(self):
        self.label.config(text=self.buffer)

    def reset_buffer(self):
        self.buffer = NORMAL_MESSAGE if (self.mode == NORMAL) else INSERT_MESSAGE
        self.display_message()

    def switch_normal(self):
        self.mode = NORMAL
        self.reset_buffer()

    def switch_insert(self):
        self.mode = INSERT
        self.reset_buffer()

    def is_valid_command(self, command):
        for regex in self.valid_commands:
            if re.match(regex, command):
                return (True, regex)
        return (False, None)

    def interpret_buffer(self):
        values = self.is_valid_command(self.buffer)
        valid = values[0]
        regex = values[1]

        if valid:
            self.reset_buffer()


