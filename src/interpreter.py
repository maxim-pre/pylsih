from.data_types import *

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



class interpreter:
    def __init__(self, node):
        self.node = node
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'no visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return RTResult().success(Number(node.tok.value).set_position(node.pos_start, node.pos_end))