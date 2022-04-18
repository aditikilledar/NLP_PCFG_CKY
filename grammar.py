""" MODULE TO PARSE PCFG GRAMMAR """

from collections import defaultdict

class pcfg(object):
	"""pcfg representation"""

	def __init__(self, grammarfile):
		self.readrules(grammarfile)
		self.startsym = None
		self.lhsrules = defaultdict(list)
		self.rhsrules = defaultdict(list)

	def readrules(self, gramfile):

		for line in gramfile:	
			line = line.strip()

			# if not commented and line exists,
			if not line.startswith('#') and line:
			
				if "->" in line:
					# if line is a rule 
					rule = self.parse(line)
					lhs, rhs, prob = rule
					# add rule to dict for rhs and lhs
					self.lhsrules[lhs].append(rule)
					self.rhsrules[rhs].append(rule)

				else: 
					# line is a start symbol
					start, prob = line.rsplit(';')
					self.startsym = start.strip()

	def parse(self, rule):

		lhs, rest = rule.split('->')
		lhs = lhs.strip()

		rhs, prob = rest.rsplit(";")
		rhstup = tuple(rhs.strip().split())
		prob = float(prob)

		print('lhs, rhs, prob \n', lhs, rhstup, prob)

	def verifyGram(self, gram):
		


if __name__ == '__main__':

	with open('probcfg.pcfg', 'r') as gramfile:
		grammar = PCFG(gramfile)

	if grammar.verifyGram():
		print("Yes, grammar is a valid PCFG in CNF")
	else:
		print("No, grammar is not a valid PCFG in CNF")