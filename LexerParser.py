from ply import lex, yacc


class Lexer:
    

    reserved = {
        #'ikawna'       :   'IF',
        #'syapala'      :   'ELSE',
        #'akona'        :   'ELSEIF',
        #'kamipa'       :   'WHILE',
        #'ibalik'       :   'RETURN',
        'tayona'       :   'MAIN',
        'ayokona'       :   'END',
        #'nbsb'         :   'READ',
        'pda'          :   'PRINT',
        #'paasa'        :   'FOR',
        #'habang'       :   'DO',
        'solo'         :   'INTN',
        'pafall'       :   'FLOATN',
        'feelingera'   :   'CHARN',
        'assumera'     :   'STRINGN',
        'friendzone'   :   'BOOLN',
        #'lovemosya'    :   'LT',
        #'lovekita'     :   'GT',
        #'maslovemosya' :   'LEQ',
        #'maslovekita'  :   'GEQ',
        #'pataskami'    :   'EQ',
        #'lamangsita'   :   'NEQ',
        #'basted'       :   'NOT',
        #'ot'           :   'OR',
        #'at'           :   'AND',
    }

    tokens = [
        'INT','FLOAT', 'EOL','ID','STRING',
        'PLUS','MINUS','MUL','DIV','MOD','ASSIGN',
        'OPENPAR','CLOSEPAR',
        'OPENCURLY','CLOSECURLY',
       #'OPENBRACE','CLOSEBRACE'
       # 'CHARN','BOOLN','STRINGN','ID','COMMA',
    ] + list(reserved.values())


    #tokens += reserved.values()
    
 

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = Lexer.reserved.get(t.value,'ID')    # Check for reserved words
        # redis is case sensitive in hash keys but we want the sql to be case insensitive,
        # so we lowercase identifiers 
        t.value = t.value.lower()
        return t

    # Read in a float.  This rule has to be done before the int rule.
    def t_FLOAT(self, t):
        r'-?\d+\.\d*(e-?\d+)?'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_STRING(self, t):
        # TODO: unicode...
        # Note: this regex is from pyparsing, 
        # TODO: may be better to refer to http://docs.python.org/reference/lexical_analysis.html 
        '(?:"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*")|(?:\'(?:[^\'\\n\\r\\\\]|(?:\'\')|(?:\\\\x[0-9a-fA-F]+)| (?:\\\\.))*\')'
        t.value = eval(t.value)
        t.value[1:-1]
        return t
    
    # Tokens
    #t_COMMA       =   r'\,'
    t_EOL	  =   r';'
    #t_QUOTE	  =   r'\"'
    t_OPENCURLY   =   r'\{'
    t_CLOSECURLY  =   r'\}'
    #t_OPENBRACE   =   r'\['
    #t_CLOSEBRACE  =   r'\]'
    t_PLUS        =   r'\+'
    t_MINUS       =   r'-'
    t_MUL         =   r'\*'
    t_DIV         =   r'/'
    t_MOD         =   r'%'
    t_ASSIGN      =   r'='
    t_OPENPAR     =   r'\('
    t_CLOSEPAR    =   r'\)'


    # Ignored characters
    t_ignore = " \t"

    '''
    literals = [ '{', '}' ]

    def t_lbrace(self, t):
        r'\{'
        t.type = '{'      # Set token type to the expected literal
        return t

    def t_rbrace(self, t):
        r'\}'
        t.type = '}'      # Set token type to the expected literal
        return t
    '''

    def t_COMMENT(self,t):
        r'\#.*'
        pass
        # No return value. Token discarded

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    '''
    # Compute column. 
    #     input is the input text string
    #     token is a token instance
    def find_column(input,token):
        last_cr = input.rfind('\n',0,token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column
    '''

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
 
    ''' # EOF handling rule
    def t_eof(self, t):
        # Get more input (Example)
        more = raw_input('... ')
        if more:
            self.lexer.input(more)
            #return self.lexer.token()
        return None   
     '''

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    '''
    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                break
             print(tok)
    '''

# Build the lexer and try it out
#m = Lexer()
#m.build() 
#m.test("int x")
#m.test("ayokona 0;")          # Build the lexer
#m.test("pda () { x1 = [ 4 + 3 ] ; }")     # Test it
#m.test("#\"hello\"") 
#m.test("\"Hello World\"")
#m.test("\'Hi Universe!\'")
#m.test(" syapala() { \'Hi Universe!\' }")

variableNames=[]

# dictionary of names
names = { }


class Parser:

    tokens = Lexer.tokens

    # Parsing Rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','MUL','DIV', 'MOD'),
        ('right','UMINUS'),
       # ('left', 'OR'),
       # ('left', 'AND'),
       # ('left', 'EQ', 'NEQ', 'LT', 'GT')
    )

    def p_program_start_start(self, t):
        '''progStart : programHeading OPENCURLY decl statement endprog CLOSECURLY
                | programHeading'''
        t[0] = 0

    def p_program_main(self, t):
        'programHeading : MAIN OPENPAR CLOSEPAR'
        t[0] = 0

    def p_program_decl(self, t):
        '''decl : type ID EOL
        		| empty'''
        #variableNames.append(t[2])
        #print(variableNames)

    def p_program_decl_value(self, t):
        'decl : type ID ASSIGN expression EOL'
        names[t[2]] = t[4]
       # variableNames.append(t[2])
       # print(variableNames)

    def p_program_type(self, t):
        '''type : INTN
        		| FLOATN
        		| CHARN
        		| STRINGN
        		| BOOLN'''
        t[0] = t[1]

    def p_program_print(self, t):
        '''statement : PRINT OPENPAR STRING CLOSEPAR EOL
        		| PRINT OPENPAR statement CLOSEPAR EOL'''
        print(t[3])

    def p_statement_assign(self, t):
        'statement : ID ASSIGN expression EOL'
        names[t[1]] = t[3]

    def p_statement_expr(self, t):
        'statement : expression'
        t[0] = t[1]
        #print(t[1])     # prints the value ofe evaluated expression		

    def p_expression_binop(self, t):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression MOD expression'''
        if t[2] == '+'  : t[0] = t[1] + t[3]
        elif t[2] == '-': t[0] = t[1] - t[3]
        elif t[2] == '*': t[0] = t[1] * t[3]
        elif t[2] == '/': t[0] = t[1] / t[3]
        elif t[2] == '%': t[0] = t[1] % t[3]

    def p_expression_uminus(self, t):
        'expression : MINUS expression %prec UMINUS'
        t[0] = -t[2]

    def p_expression_group(self, t):
        'expression : OPENPAR expression CLOSEPAR'
                  
        t[0] = t[2]

    def p_expression_number(self, t):
        '''expression : INT 
		     | FLOAT'''
        t[0] = t[1]

    def p_expression_name(self, t):
        '''expression : ID'''
        try:
            t[0] = names[t[1]]
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    
    def p_empty(self, t):
        'empty :'
        pass
   

    def p_program_end(self, t):
        'endprog : END INT EOL'
        if t[2] == 0 :  t[0] = 0
        else:  print("Invalid return value")


    def p_error(self, t):
        print("Parser: Syntax error at '%s'" % t.value)


    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

