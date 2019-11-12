import sys

from lexer import Lexer
from lexer import Token
from rdp import RDP

def main():

    files = sys.argv[1:]

    for file in files:
        parser = RDP(file)
        parser.parse()
        parser.write_output()

main()