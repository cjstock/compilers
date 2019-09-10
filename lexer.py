""" Questions:
        1. is '=' a separator or operator? Operator?
        2. Do I count comment symbols as separators too? Yes?

    Notes:
        1. Use isspace() to find whitespace

"""
import sys

class token:
    def __init__(self, t_type, t_value):
        self.t_type = t_type
        self.t_value = t_value

class lexer:
    def __init__(self):
        self.separators = ['%%','(',')',',','{','}',';','=','[*','*]']
        self.keywords = ['function','int','boolean','real','if','fi','otherwise','return','put','get','while','true','false']
        self.operators = ['==','/=','>','<','=>','<=','+','-','*','/']
