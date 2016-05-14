from sys import *

tokens = []

def open_file(filename):
    data = open(filename, "r").read()
    return data

def lex(filecontents):
    tok = ""
    state = 0
    string = ""
    filecontents = list(filecontents)

    for char in filecontents:
      tok += char
      #print(tok)
      if tok == " " or tok == "\t":    # for empty string
          if state == 0:
	          tok = ""  
          else:
            tok = " "
      elif tok == "\n" or tok == ";" or tok == "tayona" or tok == "ayokona":
        tok = ""  
      elif tok == "pda" or tok =="PDA":   # for printing whatever is inside pda
        #print("FOUND A PRINT")
        tokens.append("PRINT")
        tok = ""
      elif tok == "(" or tok == ")" or tok == "{" or tok == "}":
        tok =""
      elif tok == "\"":
        if state == 0:    # print("Found A ( ")
          state = 1
        elif state == 1:
          # print("FOUND A STRING" )
          tokens.append("STRING:" + string)
          string = ""
          state = 0
          tok = ""
      elif state == 1:
        string += tok
        tok = ""
    #print(tokens)
    return tokens


def parse(toks):
  #print(toks)
  i = 0
  while(i < len(toks)):
    #print(i)
    #print(toks[i] + " " + toks[i+1])
    if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING":
      #print("FOUND STRING")
      print(toks[i+1][8:])
      i += 2

def run():
  data = open_file(argv[1])
  #lex(data)
  toks = lex(data)
  parse(toks)

run()
