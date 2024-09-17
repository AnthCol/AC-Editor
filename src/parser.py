import re 

class Parser:
    def parse_movement(buffer):
        parts = re.split('h|j|k|l', buffer)
        print("In parse_movement, parts[0] = " + parts[0])
        return str(parts[0])