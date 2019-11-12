import sys

from lexer import Lexer
from lexer import Token
from rdp import RDP

def main():

    parser = RDP()
    parser.parse()
    parser.write_output()

main()