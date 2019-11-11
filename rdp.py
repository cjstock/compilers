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
            "Assign": '\t<Assign> -> <Identifier> = <Expression> ;\n',
            "Statement": '\t<Statement> -> <Assign>\n',
            "Compound": '\t<Compound> -> { <Statement_List }\n',
            "Statement_List1": '\t<Statement_List> -> <Statement>\n'
        }

    def add_output_statement(self, statement):
        self.output_statements.append(statement)

    def write_output(self):
        with open("output_{}.txt".format(self.file), 'w') as output:
            for statement in self.output_statements:
                output.write(statement)

    def throw_error(self, expected_token):
        message = 'Expected "{}", found {}'.format(expected_token, self.current_token.t_value)
        self.add_output_statement('SYNTAX ERROR:: Line Number:TODO    Token:{}     Value:{}    Message:{}\n'.format(self.current_token.t_type, self.current_token.t_value, message))
        sys.exit(1)

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
        if self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["IDs1"])
            self.get_next_token()

            if self.current_token.t_value == ',':
                self.add_output_statement(self.statements["IDs2"])
                self.get_next_token()
                self.IDs()

            else: self.throw_error(expected_token=',')
        else: self.throw_error(expected_token='Identifier')

    def Statement_List(self):
        self.add_output_statement(self.statements["Statement_List1"])
        self.Statement()
        if (
            self.current_token.t_type == 'id' or
            self.current_token.t_value == ( '{' or 'if' or 'return' or 'put' or 'get' or 'while')
            ):
                pass

    def Compound(self):
        if self.current_token.t_value == '{':
            self.add_output_statement(self.statements["Compound"])
            self.Statement_List()
            if self.current_token.t_value == '}':
                self.get_next_token()

            else: self.throw_error(expected_token='}')
        else: self.throw_error(expected_token='{')

    def If(self):
        pass

    def Return(self):
        pass

    def Print(self):
        pass

    def Scan(self):
        pass

    def While(self):
        pass

    def Condition(self):
        pass

    def Relop(self):
        pass

    def Factor(self):
        if self.current_token.t_value == '-':
            self.add_output_statement(self.statements['Factor1'])
            self.get_next_token()
            self.Primary()
        elif (
            self.current_token.t_type == 'id' or
            self.current_token.t_type == 'int' or
            self.current_token.t_type == 'real' or
            self.current_token.t_value == '(' or
            self.current_token.t_value == 'true' or
            self.current_token.t_value == 'false'
            ):
                self.add_output_statement(self.statements['Factor2'])
                self.Primary()
        else: self.throw_error(expected_token='Identifier, Integer, Real, "(", "true", or "false"')

    def Primary(self):
        if self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Primary1"])
            self.get_next_token()

            if self.current_token.t_value == '(':
                self.add_output_statement(self.statements["Primary2"])
                self.get_next_token()
                self.IDs()
                if self.current_token.t_value == ')':
                    self.get_next_token()
                else: self.throw_error(expected_token=')')

        elif self.current_token.t_type == 'int':
            self.add_output_statement(self.statements["Primary3"])
            self.get_next_token()

        elif self.current_token.t_value == '(':
            self.add_output_statement(self.statements["Primary4"])
            self.get_next_token()
            self.Expression()
            if self.current_token.t_value == ')':
                self.get_next_token()
            else: self.throw_error(expected_token=')')

        elif self.current_token.t_type == 'real':
            self.add_output_statement(self.statements["Primary5"])
            self.get_next_token()

        elif self.current_token.t_value == 'true':
            self.add_output_statement(self.statements["Primary6"])
            self.get_next_token()

        elif self.current_token.t_value == 'false':
            self.add_output_statement(self.statements["Primary7"])
            self.get_next_token()

        else: self.throw_error(expected_token='Identifier, Integer, Real, "(", "true", or "false"')

    def Empty(self):
        pass

    def Term_(self):
        if self.current_token.t_value == '*':
            self.add_output_statement(self.statements["Term'1"])
            self.get_next_token()
            self.Factor()
            self.Term_()

        elif self.current_token.t_value == '/':
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
        if self.current_token.t_value == '+':
            self.add_output_statement(self.statements["Expression'1"])
            self.get_next_token()
            self.Term()
            self.Expression_()

        elif self.current_token.t_value == '-':
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
        if self.current_token.t_value == '=':
            self.get_next_token()
            self.Expression()
            if self.current_token.t_value == ';':
                self.get_next_token()
            else: self.throw_error(expected_token=';')
        else: self.throw_error(expected_token='=')

    def Statement(self):
        if self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["Assign"])
            self.get_next_token()
            self.Assign()

    def parse(self):
        """Begins parsing the Rat19F file"""
        self.Statement()