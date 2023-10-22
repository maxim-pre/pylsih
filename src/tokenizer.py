from .constants import *
from .position import Position
from .errors import InvalidCharError


class Token:
    def __init__(self, type_, value=None) -> None:
        self.type_ = type_ 
        self.value = value 

    def __repr__(self) -> str:
        if self.value: return f'{self.type_}:{self.value}'
        return f'{self.type_}'
    

class Lexer:
    def __init__(self, text, file_name) -> None:
        self.text = text 
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None 

    def make_number(self):
        num_str = ''
        dot_count = 0 

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 1:
            return Token(TT_FLOAT, float(num_str))
        else:
            return Token(TT_INT, int(num_str))



    def make_token_sequence(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char 
                return [], InvalidCharError("'" + char + "'", pos_start, self.pos)
        
        return tokens, None
    