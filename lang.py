###################################################
# CONSTANTS 
###################################################

DIGITS = '0123456789'

###################################################
# TOKENS 
###################################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS' 
TT_MINUS = 'MINUS'
TT_DIV = 'DIV'
TT_MUL = 'MUL'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type_, value=None) -> None:
        self.type_ = type_ 
        self.value = value 

    def __repr__(self) -> str:
        if self.value: return f'{self.type_}:{self.value}'
        return f'{self.type_}'
    
###################################################
# ERRORS 
###################################################

class Error:
    def __init__(self, details, error_name, pos_start, pos_end) -> None:
        self.details = details 
        self.error_name = error_name
        self.pos_start = pos_start 
        self.pos_end = pos_end
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.file_name}, Line {self.pos_start.ln + 1}'
        return result

class InvalidCharError(Error):
    def __init__(self, details, pos_start, pos_end) -> None:
        super().__init__(details, 'Illegal Character', pos_start, pos_end)
        
        
###################################################
# LEXER
# TURN SEQUENCE OF CHARACTERS INTO SEQUENCE OF TOKENS 
###################################################

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
    
###################################################
# POSITION
###################################################

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
    

###################################################
# NODES
###################################################

class NumberNode: 
    def __init__(self, tok) -> None:
        self.tok = tok 

    def __repr__(self) -> str:
        return f'{self.tok}'
    
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node 
        self.op_tok = op_tok 
        self.right_node = right_node 
    
    def __repr__(self) -> str:
        return f'{self.left_node}, {self.op_tok}, {self.right_node}'
    



###################################################
# PARSER
###################################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens 
        self.tok_idx = -1 
        self.advance()

    def advance(self):
        self.tok_idx +=1

        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens(self.tok_idx)
        return self.current_tok

    def factor(self):
        tok = self.current_tok 

        if tok.type in [TT_INT, TT_FLOAT]:
            self.advance()
            return NumberNode(tok)


    def term(self):
        return self.binOp(self.factor, (TT_DIV, TT_MUL))

    def expr(self):
        return self.binOp(self.term, (TT_PLUS, TT_MINUS))

    def binOp(self, func, ops):
        left = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok 
            right = func()
            left = BinOpNode(left, op_tok, right)

        return left
            


        




            
###################################################
# RUN
###################################################

def run(text):
    lexer = Lexer(text, 'test.py')
    tokens, error = lexer.make_token_sequence()

    return tokens, error



