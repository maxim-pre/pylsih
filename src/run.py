from .tokenizer import Lexer
from .parser_ import Parser


def run(text):
    # generate tokens from text
    lexer = Lexer(text, 'test.py')
    tokens, error = lexer.make_token_sequence()

    if error: return None, error

    #generate ast (abstract search tree)
    parser = Parser(tokens)
    ast = parser.parse()
    print(type(ast.node.left_node))

    return ast.node, ast.error