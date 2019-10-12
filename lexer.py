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

class Lexer:

    separators = ['%%','(',')',',','{','}',';','=','[*','*]']
    keywords = ['function','int','boolean','real','if','fi','otherwise','return','put','get','while','true','false']
    operators = ['==','/=','>','<','=>','<=','+','-','*','/']

    def __init__(self, ):
        pass
    
    def handle_serparators(self):
        pass

    def handle_keywords(self):
        pass

    def handle_operators(self):
        pass

    def handle_id(self):
        pass

    def handle_int(self):
        pass

    def handle_real(self):
        pass

    def lexer(self):
        pass
