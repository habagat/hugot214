
# -----------------------------------------------------------------------------
# update_select_delete.py
#
# -----------------------------------------------------------------------------

from ply import lex, yacc


class SqlLexer:
    
    tokens = [
        'NAME','INT','FLOAT',
        'PLUS','MINUS','MUL','DIV','MOD','ASSIGN',
        'OPENPAR','CLOSEPAR','OPENCURLY','CLOSECURLY','OPENBRACE','CLOSEBRACE'
       # 'CHARN','BOOLN','STRINGN','ID','COMMA','EOL',
    ]

    '''reserved = {
        'ikawna'       :   'IF',
        'syapala'      :   'ELSE',
        'akona'        :   'ELSEIF',
        'kamipa'       :   'WHILE',
        'ibalik'       :   'RETURN',
        'tayona'       :   'MAIN',
        'nbsb'         :   'READ',
        'pda'          :   'PRINT',
        'paasa'        :   'FOR',
        'habang'       :   'DO',
        'solo'         :   'INT',
        'pafall'       :   'FLOAT',
        'feelingera'   :   'CHAR',
        'assumera'     :   'STRING',
        'friendzone'   :   'BOOLEAN',
        'lovemosya'    :   'LT',
        'lovekita'     :   'GT',
        'maslovemosya' :   'LEQ',
        'maslovekita'  :   'GEQ',
        'pataskami'    :   'EQ',
        'lamangsita'   :   'NEQ',
        'basted'       :   'NOT',
        'ot'           :   'OR',
        'at'           :   'AND',
    }

    tokens += reserved.values()
    '''


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
    '''
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = SqlLexer.reserved.get(t.value,'ID')    # Check for reserved words
        # redis is case sensitive in hash keys but we want the sql to be case insensitive,
        # so we lowercase identifiers 
        t.value = t.value.lower()
        return t


    def t_STRING(self, t):
        # TODO: unicode...
        # Note: this regex is from pyparsing, 
        # TODO: may be better to refer to http://docs.python.org/reference/lexical_analysis.html 
        '(?:"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*")|(?:\'(?:[^\'\\n\\r\\\\]|(?:\'\')|(?:\\\\x[0-9a-fA-F]+)| (?:\\\\.))*\')'
        t.value = eval(t.value)
        t.value[1:-1]
        return t
      '''

    # Tokens
    #t_COMMA       =   r'\,'
    t_OPENCURLY   =   r'\{'
    t_CLOSECURLY  =   r'\}'
    t_OPENBRACE   =   r'\['
    t_CLOSEBRACE  =   r'\]'
    t_PLUS        =   r'\+'
    t_MINUS       =   r'-'
    t_MUL         =   r'\*'
    t_DIV         =   r'/'
    t_MOD         =   r'%'
    t_ASSIGN      =   r'='
    t_OPENPAR     =   r'\('
    t_CLOSEPAR    =   r'\)'
    t_NAME        = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
        
    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer


class SqlParser:

    tokens = SqlLexer.tokens

    # Parsing Rules

    precedence = (
        ('left','PLUS','MINUS'),
        ('left','MUL','DIV', 'MOD'),
        ('right','UMINUS'),
       # ('left', 'OR'),
       # ('left', 'AND'),
       # ('left', 'EQ', 'NEQ', 'LT', 'GT')
    )
    # dictionary of names
    names = { }

    def p_statement_assign(self, t):
        'statement : NAME ASSIGN expression'
        names[t[1]] = t[3]

    def p_statement_expr(self, t):
        'statement : expression'
        print(t[1])

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
        '''expression : OPENPAR expression CLOSEPAR
                    | OPENCURLY expression CLOSECURLY
                    | OPENBRACE expression CLOSEBRACE'''
        t[0] = t[2]

    def p_expression_number(self, t):
        '''expression : INT 
		| FLOAT'''
        t[0] = t[1]

    def p_expression_name(self, t):
        'expression : NAME'
        try:
            t[0] = names[t[1]]
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)


    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

