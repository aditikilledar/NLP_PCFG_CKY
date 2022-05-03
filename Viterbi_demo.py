"""NLTK Viterbi Parser for PCFGs"""

import sys
import time

from functools import reduce
from nltk import tokenize
from nltk.grammar import PCFG
from Viterbi import ViterbiParser

pcfg1 = PCFG.fromstring(
    """
S -> NP VP [1.0]
NP -> Det N [0.5] | NP PP [0.25] | 'John' [0.1] | 'I' [0.15]
Det -> 'the' [0.8] | 'my' [0.2]
N -> 'man' [0.5] | 'telescope' [0.5]
VP -> VP PP [0.1] | V NP [0.7] | V [0.2]
V -> 'ate' [0.35] | 'saw' [0.65]
PP -> P NP [1.0]
P -> 'with' [0.61] | 'under' [0.39]
"""
)

pcfg2 = PCFG.fromstring(
    """
S    -> NP VP         [1.0]
VP   -> V NP          [.59]
VP   -> V             [.40]
VP   -> VP PP         [.01]
NP   -> Det N         [.41]
NP   -> Name          [.28]
NP   -> NP PP         [.31]
PP   -> P NP          [1.0]
V    -> 'saw'         [.21]
V    -> 'ate'         [.51]
V    -> 'ran'         [.28]
N    -> 'boy'         [.11]
N    -> 'cookie'      [.12]
N    -> 'table'       [.13]
N    -> 'telescope'   [.14]
N    -> 'hill'        [.5]
Name -> 'Jack'        [.52]
Name -> 'Bob'         [.48]
P    -> 'with'        [.61]
P    -> 'under'       [.39]
Det  -> 'the'         [.41]
Det  -> 'a'           [.31]
Det  -> 'my'          [.28]
"""
)

# Define two demos.  Each demo has a sentence and a grammar.
demos = [
    ("I saw the man with my telescope", pcfg1),
    ("the boy saw Jack with Bob under the table with a telescope", pcfg2),
]

# Ask the user which demo they want to use.
print()
for i in range(len(demos)):
    print(f"{i + 1:>3}: {demos[i][0]}")
    print("     %r" % demos[i][1])
    print()
print("Which demo (%d-%d)? " % (1, len(demos)), end=" ")
try:
    snum = int(sys.stdin.readline().strip()) - 1
    sent, grammar = demos[snum]
except:
    print("Bad sentence number")
    exit()

# Tokenize the sentence.
tokens = sent.split()

parser = ViterbiParser(grammar)
all_parses = {}

print(f"\nsent: {sent}\nparser: {parser}\ngrammar: {grammar}")
parser.trace(3)
t = time.time()
parses = parser.parse_all(tokens)
time = time.time() - t
average = (
    reduce(lambda a, b: a + b.prob(), parses, 0) / len(parses) if parses else 0
)
num_parses = len(parses)
for p in parses:
    all_parses[p.freeze()] = 1

parses = all_parses.keys()
if parses:
    p = reduce(lambda a, b: a + b.prob(), parses, 0) / len(parses)
else:
    p = 0
print("------------------------------------------")
print("%11s%11d%19.14f" % ("n/a", len(parses), p))

# Ask the user if we should draw the parses.
print()
print("Draw parses (y/n)? ", end=" ")
if sys.stdin.readline().strip().lower().startswith("y"):
    from nltk.draw.tree import draw_trees
    draw_trees(*parses)

print()
print("Print parses (y/n)? ", end=" ")
if sys.stdin.readline().strip().lower().startswith("y"):
    for parse in parses:
        print(parse)
