""" IMPLEMENTS CKY ALGO USING PCFG """

from grammar import PCFG
from collections import defaultdict
import json
import pprint

class CKYParser(object):

	def __init__(self, grammar):
		self.grammar = grammar

	# TODO
	def checkMembership(self, tokens):
		"""
		Membership checking. Parse the input tokens and return True if 
		the sentence is in the language described by the grammar. Otherwise return False
		"""
		n = len(tokens)
		# init backptrs table
		ptrs = defaultdict()
		for i in range(n+1):
			for j in range(i+1, n+1):
				ptrs[(i,j)] = defaultdict()

		for i, word in enumerate(tokens):
			for key, values in self.grammar.rhsrules.items():
				# print(key,values)
				if word == key[0]:
					for items in values:
						ptrs[(i, i+1)][items[0]] = word

		pprint.pprint(dict(ptrs))

		print('\n-------------------------------------------------------------\n')


		# print(pi)
        # pseudocode
        # for length=2…n:
        #     for i=0…(n-length):
        #         j = i + length
        #         for k=i+1…j-1:
        #             for A ∈ N:
        #               M={A|A->BC∈R and B ∈ ptrs[i,k] and C∈ ptrs[k,j]
        #               ptrs[i,j]=ptrs[i,j] union M

		"""
		via geeks4geeks:-
		For i = 1 to n:
		For each variable A:
		We check if A -> b is a rule and b = wi for some i:
		If so, we place A in cell (i, i) of our table. 

		For l = 2 to n:
		For i = 1 to n-l+1:
		j = i+l-1
		For k = i to j-1:
		For each rule A -> BC: 
		We check if (i, k) cell contains B and (k + 1, j) cell contains C:
		If so, we put A in cell (i, j) of our table. 
		"""

		for length in range(2, n+1):
			for i in range(n - length + 1):
				j = i + length
				for k in range(i + 1, j):
					for key, values in self.grammar.rhsrules.items():
						for B in ptrs[(i, k)]:
							for C in ptrs[(k, j)]:
								if key[0] == B and key[1] == C: #A->BC∈R
									for items in values:
										if items[0] in ptrs[(i, j)]:
											ptrs[(i, j)][items[0]].append(((key[0],i,k), (key[1],k,j))) # ptrs[i,j]=ptrs[i,j] union M
										else:
											ptrs[(i, j)][items[0]] = [((key[0],i,k), (key[1],k,j))] # ptrs[i,j]= M

		pprint.pprint(dict(ptrs))
		# print(dict(ptrs))

		if self.grammar.startsym in ptrs[(0, n)]:
			print("YES")
			return True
		else:
			print("NO")
			return False


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
	# with open('pcfg.cfg', 'r') as gramfile:
		grammar = PCFG(gramfile)
		parser = CKYParser(grammar)

		sentence = "Flights from miami to cleveland"
		inputokens = clean(sentence)

		#parse tree with backpointers and print table
		if parser.checkMembership(inputokens):
			pass