import sys

from lexer import lexer
from lexer import token

def parse(path):
    with open(path) as file:
        for line in file:
            for char in line:

def main():
    for arg in sys.argv[1:]:
        parse(arg)

if __name__ == "__main__":
    main()