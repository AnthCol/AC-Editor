import re

class VimController:
    NORMAL = 0
    INSERT = 1
    mode = NORMAL
    insert_message = "--INSERT--"
    normal_message = "--NORMAL--"
    message = normal_message
    buffer = ""

    valid_commands = {
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
    }


    def display_message(self, label):
        label.config(text=self.message)
        label.pack()

    def clear_buffer(self):
        self.buffer = ""
    
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
            self.clear_buffer()


