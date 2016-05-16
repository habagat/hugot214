from LexerParser import *
from sys import *

class Main:

	def open_file(filename):
		data = open(filename, "r").read()
		return data

	statement = open_file(argv[1])
	#statement=statement.lower()

	lexer = SqlLexer().build()     #from LexerParser
	parser = SqlParser().build()	#from LexerParser
	result = parser.parse(statement)
			

	#statement=''
	#while statement!='quit':
		#statement=input("HUGOT>")
		#if statement == 'quit':
			#break
		#else:
			#lexer = SqlLexer().build()     #from LexerParser
			#parser = SqlParser().build()	#from LexerParser
			#result = parser.parse(statement)

			
