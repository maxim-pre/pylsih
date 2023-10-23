from tools.strings_with_arrows import *
class Error:
    def __init__(self, details, error_name, pos_start, pos_end) -> None:
        self.details = details 
        self.error_name = error_name
        self.pos_start = pos_start 
        self.pos_end = pos_end
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.file_name}, Line {self.pos_start.ln + 1}'
        result += '\n\n'
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class InvalidCharError(Error):
    def __init__(self, details, pos_start, pos_end) -> None:
        super().__init__(details, 'Illegal Character', pos_start, pos_end)


class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end) -> None:
        super().__init__(details, 'Invalid Syntax', pos_start, pos_end)