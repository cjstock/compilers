""" Questions:

    Notes:
        1. Use isspace() to find whitespace

"""
import sys

class token:
    def __init__(self, t_type, t_value):
        """Initializes an instance of the token class"""
        self.t_type = t_type
        self.t_value = t_value

class lexer:
    def __init__(self):
        """Initializes the datastructures containing separators, keywords, and operators"""
        self.separators = ['%%','(',')',',','{','}',';','=','[*','*]']
        self.keywords = ['function','int','boolean','real','if','fi','otherwise','return','put','get','while','true','false']
        self.operators = ['==','/=','>','<','=>','<=','+','-','*','/']

    def parse(path):
        """Begins parsing the Rat19F file"""
        with open(path) as file:
            
