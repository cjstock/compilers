import sys

from lexer import lexer
from lexer import token

def main():

    lex = lexer()

    lex.get_token(sys.argv[1])

if __name__ == "__main__":
    main()