from .tokenizer import Lexer
from .parser_ import Parser
from .interpreter import Interpreter


def run(text):
    # generate tokens from text
    lexer = Lexer(text, 'test.py')
    tokens, error = lexer.make_token_sequence()

    if error: return None, error

    #generate ast (abstract search tree)
    parser = Parser(tokens)
    ast = parser.parse()
    
    if ast.error: return None, ast.error 

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    

    return result.value, result.error