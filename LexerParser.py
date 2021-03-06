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
        'nbsb'         :   'READ',
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
        #'lamangsiya'   :   'NEQ',
        #'basted'       :   'NOT',
        #'ot'           :   'OR',
        #'at'           :   'AND',
    }

    tokens = [
        'INT','FLOAT', 'EOL','ID','STRING',
        'PLUS','MINUS','MUL','DIV','MOD','ASSIGN',
        'OPENPAR','CLOSEPAR',
        'OPENCURLY','CLOSECURLY',
        'COMMA',
       #'OPENBRACE','CLOSEBRACE'
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
    t_COMMA       =   r'\,'
    t_EOL	      =   r';'
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
#m.test("solo x = 4")
#m.test("ayokona 0;")          # Build the lexer
#m.test("pda () { x1 = [ 4 + 3 ] ; }")     # Test it
#m.test("#\"hello\"") 
#m.test("\"Hello World\"")
#m.test("\'Hi Universe!\'")
#m.test(" syapala() { \'Hi Universe!\' }")

variableNames=[]
statementlist=[]
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
        'progStart : programHeading OPENCURLY decl statement endprog CLOSECURLY'
        t[0] = 0

    def p_program_main(self, t):
        'programHeading : MAIN OPENPAR CLOSEPAR'
        t[0] = 0

    def p_program_decl(self, t):
        'decl : type ID nextdecl EOL decl'
        variableNames.append(t[2])
        names[t[2]]= ''
        #print(names)

    def p_program_vempty(self, t):
    	'decl : empty'

    def p_program_decl_value(self, t):
        'decl : type ID ASSIGN value nextdecl EOL decl '
        #print(variableNames)
        #variableNames.append(t[2])
        #for j in range(0, len(variableNames)):
            #if variableNames[j]==t[2]: 
               # print(variableNames[j])
               # print("variable already exist")
               # break
            #else:
        variableNames.append(t[2]) 
        names[t[2]] = t[4]
                
 

    def p_program_nextdecl(self, t):
        'nextdecl : COMMA ID nextdecl'
        variableNames.append(t[2])
        names[t[2]]= ''       

    def p_program_declassign(self, t):
        'nextdecl : COMMA ID ASSIGN value nextdecl '
        variableNames.append(t[2])  
        names[t[2]]=t[4]
       

    def p_program_emptydecl(self, t):
        'nextdecl : empty'



    def p_program_number(self, t):
        '''value : INT 
		     | FLOAT'''
        t[0] = t[1]

    def p_program_type(self, t):
        '''type : INTN
        		| FLOATN
        		| CHARN
        		| STRINGN
        		| BOOLN'''
        t[0] = t[1]

    #def p_program_assignvar(self, t):
    #	'assignvar : ID ASSIGN expression EOL assignvar'
   # 	names[t[1]] = t[3]

    #def p_program_varempty(self, t):
    #	'assignvar : empty'
  

    def p_program_print(self, t):
        '''statement : PRINT OPENPAR STRING CLOSEPAR EOL statement  
        		| PRINT OPENPAR statement CLOSEPAR EOL statement'''
        #state = i + 1
        statementlist.append(t[3])
        #print(t[3])
        #print(statementlist)
        #print(state)
     
    def p_program_input(self, t):
    	'statement : READ OPENPAR ID CLOSEPAR EOL statement'
    	#x = input() 
    	statementlist.append("SCANVALUE")
    	names[t[3]] = 'SCANVAL' 
    	#statementlist.append(t[3])
    #def p_program_if(self, t):
    #	'statement : FOR OPENPAR logicOp CLOSEPAR OPENCURLY statement CLOSECURLY'

    #def p_program_cond(self, t):
    #	'logicOp : ID EQ ID'

    def p_statement_assign(self, t):
        'statement : ID ASSIGN expression EOL statement'
        #print(t[3])
        #if(names[t[1]] == ''):
        names[t[1]] = t[3]


    def p_statement_emptyState(self, t):
        'statement : empty'
        pass

    def p_statement_expr(self, t):
        'statement : expression'
        t[0] = t[1]
        #print(t[1])     # prints the value of evaluated expression		

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
            #names[t[1]] = 0
            print("Undefined name '%s'" % t[1])
            t[0] = 0
            #exit(0)

    
    def p_empty(self, t):
        'empty :'
        pass
   

    def p_program_end(self, t):
        'endprog : END INT EOL'
        #print(statementlist)
        #print(names)
        x = len(statementlist)

        for i in range(0, x):
            if(statementlist[x-1]=='SCANVALUE'):
            	input()
            else: print(statementlist[x-1])
           
            x = x-1

        if t[2] == 0 :  t[0] = 0
        else:  print("Invalid return value")


    def p_error(self, t):
        print("Parser: Syntax error at '%s'" % t.value)


    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    
