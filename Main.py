from LexerParser import *
from sys import *

class Main:

	def open_file(filename):
		data = open(filename, "r").read()
		return data

	statement = open_file(argv[1])

	lexer = Lexer().build()     #from LexerParser
	parser = Parser().build()	#from LexerParser
	result = parser.parse(statement)
			