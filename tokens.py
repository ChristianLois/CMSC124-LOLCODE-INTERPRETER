class Token:
    def __init__(self, type_, value, line_num):
        self.type = type_
        self.value = value
        self.line_num = line_num