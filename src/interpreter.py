from .data_types import Number
from .constants import *

class RTResult:
    def __init__(self):
        self.value = None 
        self.error = None 
    
    def register(self, res):
        if res.error: self.error = res.error 
        return res.value 
    
    def failure(self, error):
        self.error = error 
        return self
    
    def success(self, value):
        self.value = value 
        return self



class Interpreter:
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'no visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return RTResult().success(Number(node.tok.value).set_position(node.pos_start, node.pos_end))
    
    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        if res.error: return res 

        op_tok = node.op_tok 
        result = error = None

        if op_tok.type_ == TT_PLUS:
            result, error = left.added_to(right)
        if op_tok.type_ == TT_MINUS:
            result, error = left.subbed_to(right)
        if op_tok.type_ == TT_DIV:
            result, error = left.divided_to(right)
        if op_tok.type_ == TT_MUL:
            result, error = left.multiplied_to(right)
        
        if error: 
            return res.failure(error)
        else:
            return res.success(result)
        