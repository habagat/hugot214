from LexerParser import *
from sys import *

class Main:

	def open_file(filename):
		if filename.endswith(".hgt"):
			data = open(filename, "r").read()
		else:
			print("Invalid file type. File extension should be '.hgt'")
			exit(0)
		return data

	statement = open_file(argv[1])

	lexer = Lexer().build()     #from LexerParser
	parser = Parser().build()	#from LexerParser
	result = parser.parse(statement)
			
