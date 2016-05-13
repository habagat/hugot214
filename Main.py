#from Query import *
#from FileReader import *
#from Select import *
#from Metadata import *
#from Data import *
from LexerParser import *

class Main:
#	database={}
#	md=Metadata()
		
	statement=''
	while statement!='quit':
		statement=input("HUGOT>")
		statement=statement.lower()
		#statement=statement.replace(","," ")

		if statement == 'quit':
			break
		else:
			lexer = SqlLexer().build()     #from LexerParser
			parser = SqlParser().build()	#from LexerParser
			result = parser.parse(statement)
			
			#if result != None:
				#statement = result
				#print('Result: ' + str(result))
				#q1=Query(statement,database)
				#q1.classify_query();
			
