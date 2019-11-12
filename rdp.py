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
            "Rat19F": '\t<Rat19F> -> <Opt_Function_Definitions> \%\% <Opt_Declaration_List> <Statement_List> \%\%\n',
            "Opt_Function_Definitions1": '\t<Opt_Function_Definitions> -> <Function_Definitions>\n',
            "Opt_Function_Definitions2": '\t<Opt_Function_Definitions> -> ϵ\n',
            "Function_Definitions1": '\t<Function_Definitions> -> <Function>\n',
            "Functions_Definitions2": '\t<Function_Definitions> -> <Function> <Function_Definitions>\n',
            "Function": '\t<Function> -> function <Identifier> ( <Opt_Parameter_List> ) <Opt_Declaration_List> <Body>\n',
            "Opt_Parameter_List1": '\t<Opt_Parameter_List> -> <Parameter_List>\n',
            "Opt_Parameter_List2": '\t<Opt_Parameter_List> -> ϵ\n',
            "Parameter": '\t<Parameter> -> <IDs> <Qualifier>\n',
            "Parameter_List1": '\t<Parameter_List> -> <Parameter> ;\n',
            "Parameter_List2": '\t<Parameter_List> -> <Parameter> ; <Parameter_List>\n',
            "Opt_Declaration_List1": '\t<Opt_Declaration_List> -> <Declaration_List>\n',
            "Opt_Declaration_List2": '\t<Opt_Declaration_List> -> ϵ\n',
            "Declaration_List1": '\t<Declaration_List> -> <Declaration> ;\n',
            "Declaration_List2": '\t<Declaration_List> -> <Declaration> ; <Declaration_List>\n',
            "IDs1": '\t<IDs> -> <Identifier>\n',
            "IDs2": '\t<IDs> -> <Identifier> , IDs\n',
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
            "Condition": '\t<Condition> -> <Expression> <Relop> <Expression>\n',
            "Return1": '<Return>\n\t<Return> -> return ;\n',
            "Return2": '<Return>\n\t<Return> -> return <Expression> ;\n',
            "Print": '<Print>\n\t<Print> -> put ( <Expression> ) ;\n',
            "Scan": '<Scan>\n\t<Scan> -> get ( <IDs> ) ;\n',
            "While": '<While>\n\t<While> -> while ( <Condition> ) <Statement>\n',
            "Body": '\t<Body> -> { <Statement_List> }\n'
        }


    def add_output_statement(self, statement):
        self.output_statements.append(statement)


    def write_output(self):
        with open("output_{}.txt".format(self.file), 'w') as output:
            for statement in self.output_statements:
                output.write(statement)


    def throw_error(self, expected_token):
        if self.current_token:
            message = 'Expected {}, found "{}"!'.format(expected_token, self.current_token.t_value)
            self.add_output_statement('SYNTAX ERROR:: Line Number:TODO    Token:{}     Value:{}    Message:{}\n'.format(self.current_token.t_type, self.current_token.t_value, message))
        elif self.lex.done:
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
        if self.current_token and self.current_token.t_value == 'function':
            self.add_output_statement(self.statements["Function_Definitions1"])
            start_ids = len(self.output_statements) -1
            self.Function()

            if self.current_token and self.current_token.t_value == 'function':
                self.output_statements[start_ids] = self.statements["Function_Definitions2"]
                self.Function_Definitions()

        else: self.throw_error(expected_token='function')


    def Function(self):
        if self.current_token and self.current_token.t_value == 'function':
            self.add_output_statement(self.statements["Function"])
            self.get_next_token()
            if self.current_token and self.current_token.t_type == 'id':
                self.get_next_token()
                if self.current_token and self.current_token.t_value == '(':
                    self.get_next_token()
                    self.Opt_Parameter_List()
                    if self.current_token and self.current_token.t_value == ')':
                        self.get_next_token()
                        self.Opt_Declaration_List()
                        self.Body()
                    
                    else: self.throw_error(expected_token=')')
                else: self.throw_error(expected_token='(')
            else: self.throw_error(expected_token='<Identifier>')
        else: self.throw_error(expected_token='function')


    def Opt_Parameter_List(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Opt_Parameter_List"])
            self.Parameter_List()


    def Parameter_List(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Parameter_List"])
            start_ids = len(self.output_statements) -1
            self.Parameter()

            if self.current_token and self.current_token.t_value == ',':
                self.output_statements[start_ids] = self.statements["Parameter_List"]
                self.get_next_token()
                self.Parameter_List()

        else: self.throw_error(expected_token='<Identifier>')


    def Parameter(self):
        self.add_output_statement(self.statements["Parameter"])
        self.IDs()
        self.Qualifier()


    def Qualifier(self):
        if self.current_token and self.current_token.t_value == (
            'int' or
            'boolean' or
            'real'
        ):
            self.add_output_statement(statement='\t<Qualifier> -> {}\n'.format(self.current_token.t_value))
            self.get_next_token()

        else:
            self.throw_error(expected_token='Integer, Boolean, or Real')


    def Body(self):
        if self.current_token and self.current_token.t_value == '{':
            self.add_output_statement(self.statements["Body"])
            self.get_next_token()
            self.Statement_List()
            if self.current_token and self.current_token.t_value == '}':
                self.get_next_token()

            else: self.throw_error(expected_token='}')
        else: self.throw_error(expected_token='{')


    def Opt_Declaration_List(self):
        if self.current_token and self.current_token.t_value == (
            'int' or
            'boolean' or
            'real'
        ):
            self.add_output_statement(self.statements["Opt_Declaration_List"])
            self.Declaration_List()


    def Declaration_List(self):
        if self.current_token and self.current_token.t_value == (
            'int' or
            'boolean' or
            'real'
        ):
            self.add_output_statement(self.statements["Declaration_List1"])
            start_declarations_list = len(self.output_statements) -1
            self.Declaration()
            if self.current_token and self.current_token.t_value == ';':
                self.get_next_token()
                if self.current_token and self.current_token.t_value == (
                    'int' or
                    'boolean' or
                    'real'
                ):
                    self.output_statements[start_declarations_list] = self.statements["Declaration_List2"]
                    self.Declaration_List()
                
            else: self.throw_error(expected_token=';')
        else: self.throw_error(expected_token='<Integer, <Boolean> or <Real>')


    def Declaration(self):
        if self.current_token and self.current_token.t_value == (
            'int' or
            'boolean' or
            'real'
        ):
            self.add_output_statement(statement='\t<Declaration> -> {} <IDs>\n'.format(self.current_token.t_value))
            self.get_next_token()
            if self.current_token and self.current_token.t_type == 'id':
                self.IDs()

            else: self.throw_error(expected_token='<Identifier>')
        else: self.throw_error(expected_token='<Integer>, <Boolen>, or <Real>')


    def IDs(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["IDs1"])
            start_ids = len(self.output_statements) -1
            self.get_next_token()

            if self.current_token and self.current_token.t_value == ',':
                self.output_statements[start_ids] = self.statements["IDs2"]
                self.get_next_token()
                self.IDs()

        else: self.throw_error(expected_token='<Identifier>')


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
            self.throw_error(expected_token='<Identifier>, "{", "if", "return", "put", "get", or "while"')


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
        else: self.throw_error(expected_token='<Identifier>, Integer, Real, "(", "true", or "false"')


    def Primary(self):
        if self.current_token and self.current_token.t_type == 'id':
            self.add_output_statement(self.statements["Primary1"])
            start_primary = len(self.output_statements) -1
            self.get_next_token()

            if self.current_token and self.current_token.t_value == '(':
                self.output_statements[start_primary] = self.statements["Primary2"]
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

        else: self.throw_error(expected_token='<Identifier>, <Integer>, <Real>, "(", "true", or "false"')


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
        if self.current_token and (self.current_token.t_value == '+' or self.current_token.t_value == '-'):
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
        start_of_return = len(self.output_statements)
        self.add_output_statement(self.statements["Return1"])
        self.get_next_token()
        if (self.current_token and (
            self.current_token.t_type == 'id' or
            self.current_token.t_type == 'int' or
            self.current_token.t_type == 'real' or
            self.current_token.t_value == '(' or
            self.current_token.t_value == 'true' or
            self.current_token.t_value == '-' or
            self.current_token.t_value == 'false')
            ):
            self.output_statements[start_of_return] = self.statements["Return2"]
            self.Expression()
        elif self.current_token and self.current_token.t_value == ';':
            self.get_next_token()

        else: self.throw_error(expected_token='<Expression> or ";"')


    def Print(self):
        if self.current_token and self.current_token.t_value == 'put':
            self.get_next_token()
            if self.current_token and self.current_token.t_value == '(':
                self.get_next_token()
                self.Expression()
                if self.current_token and self.current_token.t_value == ')':
                    self.get_next_token()
                    if self.current_token and self.current_token.t_value == ';':
                        self.get_next_token()
                
                    else: self.throw_error(expected_token=';')
                else: self.throw_error(expected_token=')')
            else: self.throw_error(expected_token='(')
        else: self.throw_error(expected_token='put')


    def Scan(self):
        if self.current_token and self.current_token.t_value == 'get':
            self.get_next_token()
            if self.current_token and self.current_token.t_value == '(':
                self.get_next_token()
                self.IDs()
                if self.current_token and self.current_token.t_value == ')':
                    self.get_next_token()
                    if self.current_token and self.current_token.t_value == ';':
                        self.get_next_token()
                
                    else: self.throw_error(expected_token=';')
                else: self.throw_error(expected_token=')')
            else: self.throw_error(expected_token='(')
        else: self.throw_error(expected_token='get')


    def While(self):
        if self.current_token and self.current_token.t_value == 'while':
            self.get_next_token()
            if self.current_token and self.current_token.t_value == '(':
                self.get_next_token()
                self.Condition()
                if self.current_token and self.current_token.t_value == ')':
                    self.get_next_token()
                    self.Statement()
                else: self.throw_error(expected_token=')')
            else: self.throw_error(expected_token='(')
        else: self.throw_error(expected_token='while')

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

        elif self.current_token and self.current_token.t_value == 'return':
            self.add_output_statement(self.statements["Statement"])
            self.Return()

        elif self.current_token and self.current_token.t_value == 'put':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["Print"])
            self.Print()


        elif self.current_token and self.current_token.t_value == 'get':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["Scan"])
            self.Scan()

        elif self.current_token and self.current_token.t_value == 'while':
            self.add_output_statement(self.statements["Statement"])
            self.add_output_statement(self.statements["While"])
            self.While()

        else:
            self.throw_error(expected_token='<Identifier>, "{", "if", "return", "put", "get", or "while"')


    def parse(self):
        """Begins parsing the Rat19F file"""
        self.Statement_List()