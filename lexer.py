import sys

class Token:

    """Holds the type and value, and length of a token"""
    def __init__(self, t_type, t_value):
        """Initializes an instance of the token class"""
        self.t_type = t_type
        self.t_value = t_value
        self.length = len(t_value)


class Lexer:
    """Can parse a file and check its syntactic validity in the Rat19F language"""

    separators = ['%%', '(', ')', ',', '{','}', ';', '=', '[*', '*]']
    keywords = ['function','int','boolean','real','if','fi','otherwise','return','put','get','while','true','false']
    operators = ['==','/=','>','<','=>','<=','+','-','*','/']
    opsep = separators + operators

    id_fsm = {
        'start': '0',
        'finals': [1, 2, 3, 4],
        'transitions': { 
            '0':[1],
            '1':[2, 3, 4],
            '2':[2, 3, 4],
            '3':[2, 3, 4],
            '4':[2, 3, 4],
        }
    }

    int_fsm = {
        'start' : '0',
        'finals': [1],
        'transitions': {
            '0': [1],
            '1': [1]
        }
    }

    real_fsm = {
        'start' : '0',
        'finals': [1],
        'transitions': {
            '0': [1],
            '1': [1, 2],
            '2': [3],
            '3': [3]
        }
    }


    def __init__(self, file):
       self.file_path = file
       self.chars_read = 0
       self.done = False

#==================================================================

# symbol handlers
#==================================================================
    def handle_percent(self, chars):
        return Token(t_type='separator', t_value=chars[0:2])


    def handle_open_paren(self, chars):
        return Token(t_type='separator', t_value=chars[0])


    def handle_close_paren(self, chars):
        return Token(t_type='separator', t_value=chars[0])


    def handle_comma(self, chars):
        return Token(t_type='separator', t_value=chars[0])


    def handle_open_curl(self, chars):
        return Token(t_type='separator', t_value=chars[0])
    

    def handle_close_curl(self, chars):
        return Token(t_type='separator', t_value=chars[0])
    

    def handle_semicolon(self, chars):
        return Token(t_type='separator', t_value=chars[0])


    def handle_equals(self, chars):
        if len(chars) == 1 or (chars[1] != '=' and chars[1] != '>'):
            t_type = 'operator'
            t_value = chars[0]
        
        else:
            t_type = 'operator'
            t_value = chars[0:2]
        
        return Token(t_type=t_type, t_value=t_value)


    def handle_open_bracket(self, chars):
        return Token(t_type='separator', t_value=chars[0:2])


    def handle_star(self, chars):
        if len(chars) == 1 or (chars[1] != ']'):
            t_type = 'operator'
            t_value = chars[0]

        else:
            t_type = 'separator'
            t_value = chars[0:2]

        return Token(t_type=t_type, t_value=t_value)


    def handle_slash(self, chars):
        if len(chars) == 1 or (chars[1] != '='):
            t_type = 'operator'
            t_value = chars[0]

        else:
            t_type = 'operator'
            t_value = chars[0:2]

        return Token(t_type=t_type, t_value=t_value)
        

    def handle_right_carr(self, chars):
        return Token(t_type='operator', t_value=chars[0])


    def handle_left_carr(self, chars):
        if len(chars) == 1 or (chars[1] != '='):
            t_type = 'operator'
            t_value = chars[0]

        else:
            t_type = 'operator'
            t_value = chars[0:2]

        return Token(t_type=t_type, t_value=t_value)


    def handle_plus(self, chars):
        return Token(t_type='operator', t_value=chars[0])


    def handle_minus(self, chars):
        return Token(t_type='operator', t_value=chars[0])
    
    # Python equivilent of a switch statement
    symbol_handlers = {
        '%': handle_percent,
        '(': handle_open_paren,
        ')': handle_close_paren,
        ',': handle_comma,
        '{': handle_open_curl,
        '}': handle_close_curl,
        ';': handle_semicolon,
        '=': handle_equals,
        '[': handle_open_bracket,
        '*': handle_star,
        '/': handle_slash,
        '>': handle_right_carr,
        '<': handle_left_carr,
        '+': handle_plus,
        '-': handle_minus
    }

    # Returns a token by calling the [char] key's associated function in the symbol_handlers dictionary
    def handle_opsep(self, chars):    # handle operators and separators
        return self.symbol_handlers[chars[0]](self=self, chars=chars)

#==================================================================

# int, id, and real look_up functions
#==================================================================

    def int_fsm_lookup(self, state, input):

        if input.isdigit():
            new_state = self.int_fsm['transitions']['1']

        elif input == '.':
            new_state = self.real_fsm['transitions']['2']

        else:
            return False

        return new_state


    def id_fsm_lookup(self, state, input):

        if input.isalpha():
            new_state = self.id_fsm['transitions']['2']

        elif input.isdigit():
            new_state = self.id_fsm['transitions']['3']

        elif input == '_':
            new_state = self.id_fsm['transitions']['4']

        else:
            return False

        return new_state

    def real_fsm_lookup(self, state, input):
        if input.isdigit():
            new_state = self.real_fsm['transitions']['3']

        else:
            return False

        return new_state

#==================================================================

    """handle_functions return tokens of type int, id, and real.
        They continuously get a state from their lookutp function until it receives false.
        Then it returns a token and sets it's t_value."""
#==================================================================
    def handle_int(self, chars):
        t_value = ''

        state = self.int_fsm['transitions'][self.int_fsm['start']]

        for char in chars:
            state = self.int_fsm_lookup(state, char)
            if state == self.real_fsm['transitions']['2']:
                return self.handle_real(chars, t_value + char)
            if state:
                t_value += char

            else:
                return Token(t_type='int', t_value=t_value)

        return Token(t_type='int', t_value=t_value)

    def handle_id(self, chars):
        t_value = ''

        state = self.id_fsm['transitions'][self.id_fsm['start']]

        for char in chars:
            state = self.id_fsm_lookup(state, char)

            if state:
                t_value += char

            else:
                return Token(t_type='id', t_value=t_value)

        return Token(t_type='id', t_value=t_value)


    def handle_real(self, chars, t_value):

        state = self.real_fsm['transitions']['2']
        unfinished = chars[len(t_value):]
        for char in unfinished:
            state = self.real_fsm_lookup(state, char)

            if state:
                t_value += char

            else:
                return Token(t_type='real', t_value=t_value)

        return Token(t_type='real', t_value=t_value)


#==================================================================

    """The lexer function opens a file, keeps track of its current parse position within the file,
    then return a token."""
#==================================================================
    def lexer(self):
        with open(self.file_path) as file:
            chars = file.read()     # get file as a string
            unprocessed = chars[self.chars_read:]       # get the unprocessed part of the file string
            done = False

            if self.chars_read >= len(chars):   # if we have read all the chars of the file, we are done
                self.done = True
                done = True
                return False

            cp = 0

            while not done:
                char = unprocessed[cp]

                if char in [s[0] for s in self.opsep]:  
                    token = self.handle_opsep(unprocessed)

                elif char.isalpha():
                    token = self.handle_id(unprocessed)
                    if token.t_value in self.keywords:
                        token = Token(t_type='keyword', t_value=token.t_value)

                elif char.isdigit():
                    token = self.handle_int(unprocessed)
                
                elif char.isspace():
                    token = Token(t_type='whitespace', t_value=char)

                else:   # handle unknown token
                    token = Token(t_type='unknown', t_value=char)

                cp += token.length   
 
                self.chars_read += token.length

                return token