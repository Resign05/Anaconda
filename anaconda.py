from sys import *

tokens = []

def open_file(fn):
	dta = open(fn, 'r').read()
	dta += "<EOF>"
	return dta

def canInt(string):
	try:
		int(string)
	except:
		return False
	return True

def lex(fcont):
	fcont = list(fcont)
	tok = ""
	isexpr = 0
	state = 0
	expr = ""
	string = ""
	n = ""
	for char in fcont:
		tok += char
		if tok == " ":
			if state == 0:
				tok = ""
			else:
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("Expression:" + expr)
				isexpr = 0
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("Number:"+expr)
				expr = ""
			tok = ""
		elif tok == "printf":
			tokens.append("Printf")
			tok = ""
		elif canInt(tok):
			expr += tok
			tok = ""
		elif tok in ['+','-','*','/']:
			isexpr = 1
			expr += tok
			tok = ""
		elif tok == "\"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("String:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok = ""

	return tokens

def parse(toks):
	i = 0
	t3l = [
	'Str',
	'Num',
	'Exp'
	]

	def printfparse(toks):
		if toks[i+1][0:6] == "String":
			print(toks[i+1][8:-1])
		elif toks[i+1][0:6] == "Number":
			print(toks[i+1][7:])
		elif toks[i+1][0:10] == "Expression":
			print(eval(toks[i+1][11:]))

	while(i < len(tokens)):
		if tokens[i] == "Printf":
			if toks[i+1][0:3] in t3l:
				printfparse(toks)
				i += 2
			else:
				i += 1

def run():
	dta = open_file(argv[1])
	toks = lex(dta)
	parse(toks)

run()