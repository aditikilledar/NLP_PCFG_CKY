""" IMPLEMENTS CKY ALGO USING PCFG """

from grammar import PCFG
from collections import defaultdict

class CKYParser(object):

	def __init__(self, grammar):
		self.grammar = grammar

	# TODO
	def checkMembership(self, tokens):
		pass


	# TODO
	def backtrack(self, tokens):
		pass

def makeParseTree():
	# TODO
	pass

def clean(a):
	a = a.lower().strip().split()
	# split words like ["cat."] -> ["cat", "."]
	a[len(a)-1] = a[len(a)-1].replace(".", "")
	a.append(".")
	return a


if __name__ == "__main__":

	with open('probcfg.pcfg', 'r') as gramfile:
		grammar = PCFG(gramfile)
		parser = CKYParser(grammar)

		sentence = "Flights from miami to cleveland"
		inputokens = clean(sentence)
		#parse tree with backpointers and print table
		if parser.checkMembership(inputokens):
			pass