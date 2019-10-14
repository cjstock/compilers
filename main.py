import sys

from lexer import Lexer
from lexer import Token

def main():

    files = sys.argv[1:]
    
    for file in files:
        lex = Lexer(file=file)
        tokens = []

        while not lex.done:
            token = lex.lexer()
            if token and token.t_type != 'whitespace':
                tokens.append(token)

        with open("output_{}.txt".format(file), 'w') as output:
            for t in tokens:
                output.write('{}      {}\n'.format(t.t_type, t.t_value))
main()