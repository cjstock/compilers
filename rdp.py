import sys
from lexer import Lexer, Token

class RDP:
    """Defines a Recursive Descent Parser for the Rat19F language"""

    def __init__(self):
        self.file = 'test.rat'
        self.lex = Lexer(file=self.file)
        self.output_statements = []
        self.get_next_token()

        self.statements = {
            "IDs1": '\t<IDs> -> <Identifier> ',
            "IDs2": ', <IDs>\n',
            "Factor1": '\t<Factor> -> - <Primary>\n',
            "Factor2": '\t<Factor> -> <Primary>\n',
            "Primary1": '\t<Primary> -> <Identifier>\n',
            "Primary2": '\t<Primary> -> <Identifier> ( <IDs> )\n',
            "Primary3": '\t<Primary> -> <Integer>\n',
            "Primary4": '\t<Primary> -> ( <Expression> )\n',
            "Primary5": '\t<Primary> -> <Real>\n',
            "Primary6": '\t<Primary> -> true\n',
            "Primary7": '\t<Primary> -> false\n',
            "Term'1": "\t<Term'> -> * <Factor> <Term'>\n",
            "Term'2": "\t<Term'> -> / <Factor> <Term'>\n",
            "Term'3": "\t<Term'> -> ϵ\n",
            "Term": "\t<Term> -> <Factor> <Term'>\n",
            "Expression'1": "\t<Expression'> -> + <Term> <Expression'>\n",
            "Expression'2": "\t<Expression'> -> - <Term> <Expression'>\n",
            "Expression'3": "\t<Expression'> -> ϵ\n",
            "Expression": "\t<Expression> -> <Term> <Expression'>\n",
            "Assign": '<Assign>\n\t<Assign> -> <Identifier> = <Expression> ;\n',
            "Statement": '\t<Statement> -> ',
            "Compound": '<Compound>\n\t<Compound> -> { <Statement_List> }\n',
            "If1": '<If>\n\tif ( <Condition> ) <Statement> fi\n',
            "If2": '<If>\n\tif ( <Condition> ) <Statement> otherwise <Statement> fi\n',
            "Statement_List1": '\t<Statement_List> -> <Statement>\n',
            "Statement_List2": '\t<Statement_List> -> <Statement> <Statement_List>\n',
            "Condition": '\t<Condition> -> <Expression> <Relop> <Expression>\n'
        }


    def add_output_statement(self, statement):
        self.output_statements.append(statement)


    def write_output(self):
        with open("output_{}.txt".format(self.file), 'w') as output:
            for statement in self.output_statements:
                output.write(statement)


    def throw_error(self, expected_token):
        if self.current_token:
            message = 'Expected "{}", found {}'.format(expected_token, self.current_token.t_value)
            self.add_output_statement('SYNTAX ERROR:: Line Number:TODO    Token:{}     Value:{}    Message:{}\n'.format(self.current_token.t_type, self.current_token.t_value, message))
        else:
            self.add_output_statement('SYNTAX ERROR:: Unexpected end of file!')
        self.write_output()
        sys.exit(0)


    def get_next_token(self):
        self.current_token = self.lex.lexer()
        if self.current_token:
            while self.current_token.t_type == 'whitespace':
                self.current_token = self.lex.lexer()
            
            self.add_output_statement('Token: {}   Lexeme: {}\n'.format(self.current_token.t_type, self.current_token.t_value))


    def Rat19F(self):
        self.add_output_statement(self.statements["Rat19F"])
        self.Opt_Function_Definitions()


    def Opt_Function_Definitions(self):
        pass


    def Function_Definitions(self):
        pass


    def Function(self):
        pass


    def Opt_Parameter_List(self):
        pass


    def Parameter_List(self):
        pass


    def Parameter(self):
        pass


    def Qualifier(self):
        pass


    def Body(self):
        pass


    def Opt_Declaration_List(self):
        pass


    def Declaration_List(self):
        pass


    def Declaration(self):
        pass


    def IDs(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["IDs1"])
            self.get_next_token()

            if self.current_token and self.current_token.t_value == ',':
                self.add_output_statement(self.statements["IDs2"])
                self.get_next_token()
                self.IDs()

            else: self.throw_error(expected_token=',')
        else: self.throw_error(expected_token='Identifier')


    def Statement_List(self):
        if (self.current_token and (
            self.current_token.t_type == 'id' or
            self.current_token.t_value == '{' or
            self.current_token.t_value == 'if' or
            self.current_token.t_value == 'return' or
            self.current_token.t_value == 'put' or
            self.current_token.t_value == 'get' or
            self.current_token.t_value == 'while')
        ):
                self.add_output_statement(self.statements["Statement_List1"])
                start_of_statement_list = len(self.output_statements) -1
                self.Statement()

                if (
                self.current_token and (
                    self.current_token.t_type == 'id' or
                    self.current_token.t_value == '{' or
                    self.current_token.t_value == 'if' or
                    self.current_token.t_value == 'return' or
                    self.current_token.t_value == 'put' or
                    self.current_token.t_value == 'get' or
                    self.current_token.t_value == 'while'
                )
                ):
                    self.output_statements[start_of_statement_list] = self.statements["Statement_List2"]
                    self.Statement_List()
        else:
            self.throw_error(expected_token='Identifier, "{", "if", "return", "put", "get", or "while"')


    def Compound(self):
        if self.current_token and self.current_token.t_value == '{':
            self.get_next_token()
            self.Statement_List()
            if self.current_token and self.current_token.t_value == '}':
                self.get_next_token()

            else: self.throw_error(expected_token='}')
        else: self.throw_error(expected_token='{')


    def Factor(self):
        if self.current_token and self.current_token.t_value == '-':
            self.add_output_statement(self.statements['Factor1'])
            self.get_next_token()
            self.Primary()
        elif (self.current_token and (
            self.current_token.t_type == 'id' or
            self.current_token.t_type == 'int' or
            self.current_token.t_type == 'real' or
            self.current_token.t_value == '(' or
            self.current_token.t_value == 'true' or
            self.current_token.t_value == 'false')
            ):
                self.add_output_statement(self.statements['Factor2'])
                self.Primary()
        else: self.throw_error(expected_token='Identifier, Integer, Real, "(", "true", or "false"')


    def Primary(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Primary1"])
            self.get_next_token()

            if self.current_token and self.current_token.t_value == '(':
                self.add_output_statement(self.statements["Primary2"])
                self.get_next_token()
                self.IDs()
                if self.current_token and self.current_token.t_value == ')':
                    self.get_next_token()
                else: self.throw_error(expected_token=')')

        elif self.current_token and self.current_token.t_type == 'int':
            self.add_output_statement(self.statements["Primary3"])
            self.get_next_token()

        elif self.current_token and self.current_token.t_value == '(':
            self.add_output_statement(self.statements["Primary4"])
            self.get_next_token()
            self.Expression()
            if self.current_token and self.current_token.t_value == ')':
                self.get_next_token()
            else: self.throw_error(expected_token=')')

        elif self.current_token and self.current_token.t_type == 'real':
            self.add_output_statement(self.statements["Primary5"])
            self.get_next_token()

        elif self.current_token and self.current_token.t_value == 'true':
            self.add_output_statement(self.statements["Primary6"])
            self.get_next_token()

        elif self.current_token and self.current_token.t_value == 'false':
            self.add_output_statement(self.statements["Primary7"])
            self.get_next_token()

        else: self.throw_error(expected_token='Identifier, Integer, Real, "(", "true", or "false"')


    def Term_(self):
        if self.current_token and self.current_token.t_value == '*':
            self.add_output_statement(self.statements["Term'1"])
            self.get_next_token()
            self.Factor()
            self.Term_()

        elif self.current_token and self.current_token.t_value == '/':
            self.add_output_statement(self.statements["Term'2"])
            self.get_next_token()
            self.Factor()
            self.Term_()

        else:
            self.add_output_statement(self.statements["Term'3"])


    def Term(self):
        self.add_output_statement(self.statements["Term"])
        self.Factor()
        self.Term_()


    def Expression_(self):
        if self.current_token and self.current_token.t_value == '+':
            self.add_output_statement(self.statements["Expression'1"])
            self.get_next_token()
            self.Term()
            self.Expression_()

        elif self.current_token and self.current_token.t_value == '-':
            self.add_output_statement(self.statements["Expression'2"])
            self.get_next_token()
            self.Term()
            self.Expression_()

        else:
            self.add_output_statement(self.statements["Expression'3"])


    def Expression(self):
        self.add_output_statement(self.statements["Expression"])
        self.Term()
        self.Expression_()


    def Assign(self):
        if self.current_token and self.current_token.t_value == '=':
            self.get_next_token()
            self.Expression()
            if self.current_token and self.current_token.t_value == ';':
                self.get_next_token()
            else: self.throw_error(expected_token=';')
        else: self.throw_error(expected_token='=')


    def If(self):
        start_of_if = len(self.output_statements)
        self.add_output_statement(self.statements["If1"])
        self.get_next_token()
        if self.current_token and self.current_token.t_value == '(':
            self.get_next_token()
            self.Condition()

            if self.current_token and self.current_token.t_value == ')':
                self.get_next_token()
                self.Statement()

                if self.current_token and self.current_token.t_value == 'fi':
                    self.get_next_token()

                elif self.current_token and self.current_token.t_value == 'otherwise':
                    self.output_statements[start_of_if] = self.statements["If2"]
                    self.get_next_token()
                    self.Statement()
                    if self.current_token and self.current_token.t_value == 'fi':
                        self.get_next_token()

                else:
                    self.throw_error(expected_token='"fi" or "otherwise"')

            else:
                self.throw_error(expected_token=')')
        else:
            self.throw_error(expected_token='(')


    def Return(self):
        pass


    def Print(self):
        pass


    def Scan(self):
        pass


    def While(self):
        pass


    def Condition(self):
        self.add_output_statement(self.statements["Condition"])
        self.Expression()
        self.Relop()
        self.Expression()


    def Relop(self):
        if self.current_token and self.current_token.t_value == (
            '==' or
            '/=' or
            '>' or
            '<' or
            '=>' or
            '<='
        ):
            self.add_output_statement(statement='\t<Relop> -> {}\n'.format(self.current_token.t_value))
            self.get_next_token()

        else:
            self.throw_error(expected_token='"==", "/=", ">", "<", "=>", or "<="')


    def Statement(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["Assign"])
            self.get_next_token()
            self.Assign()
        elif self.current_token and self.current_token.t_value == 'if':
            self.add_output_statement(self.statements["Statement"])
            self.If()

        elif self.current_token and self.current_token.t_value == '{':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["Compound"])
            self.Compound()

        else:
            self.throw_error(expected_token='Identifier, "{", "if", "return", "put", "get", or "while"')


    def parse(self):
        """Begins parsing the Rat19F file"""
        self.Statement_List()