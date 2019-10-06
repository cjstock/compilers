""" Questions:

    Notes:
        1. Use isspace() to find whitespace

"""
import sys

class token:
    def __init__(self, t_type, t_value):
        self.t_type = t_type
        self.t_value = t_value

class lexer:

    separators = ['%%','(',')',',','{','}',';','=','[*','*]']
    keywords = ['function','int','boolean','real','if','fi','otherwise','return','put','get','while','true','false']
    operators = ['==','/=','>','<','=>','<=','+','-','*','/']

    def __init__(self):

    def get_token():
        pass