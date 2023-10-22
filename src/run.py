from .tokenizer import Lexer
from .parser import Parser


def run(text):
    # generate tokens from text
    lexer = Lexer(text, 'test.py')
    tokens, error = lexer.make_token_sequence()

    #generate ast (abstract search tree)
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, error