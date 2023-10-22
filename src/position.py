class Position:
    def __init__(self, idx, ln, col, file_name, ftxt) -> None:
        self.idx = idx 
        self.ln = ln 
        self.col = col 
        self.file_name = file_name 
        self.ftxt = ftxt 
    
    def advance(self, current_char):
        self.idx +=1 
        self.col +=1 

        if (current_char == '\n'):
            self.col = 0 
            self.ln += 1

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.ftxt)