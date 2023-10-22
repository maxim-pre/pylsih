from .nodes import *
from .constants import *
from .errors import InvalidSyntaxError



class ParseResult:
    def __init__(self) -> None:
        self.node = None 
        self.error = None 

        # register parsed expression, terms and factors - keep track of errors
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error 

            return res.node 
        
        return res
    
    # called if syntax valid    
    def success(self, node):
        self.node = node 
        return self

    # called if syntax invalid  
    def failure(self, error):
        self.error = error 
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens 
        self.tok_idx = -1 
        self.advance()

    def advance(self):
        self.tok_idx +=1

        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        tok = self.current_tok 
        res = ParseResult()

        if tok.type_ in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        else:
            return res.failure(InvalidSyntaxError('Expected Int or Float', tok.pos_start, tok.pos_end))

        


    def term(self):
        return self.bin_op(self.factor, (TT_DIV, TT_MUL))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())

        while self.current_tok.type_ in ops:
            op_tok = self.current_tok 
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res 
            
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
            