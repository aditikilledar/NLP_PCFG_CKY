"""Viterbi Parser NLTK implementation"""

from functools import reduce

from nltk.parse.api import ParserI
from nltk.tree import ProbabilisticTree, Tree

class ViterbiParser(ParserI):
    """
    A pseudo-code description of the algorithm used by
    ``ViterbiParser`` is:

    | Create an empty most likely constituent table, *MLC*.
    | For width in 1...len(text):
    |   For start in 1...len(text)-width:
    |     For prod in grammar.productions:
    |       For each sequence of subtrees [t[1], t[2], ..., t[n]] in MLC,
    |         where t[i].label()==prod.rhs[i],
    |         and the sequence covers [start:start+width]:
    |           old_p = MLC[start, start+width, prod.lhs]
    |           new_p = P(t[1])P(t[1])...P(t[n])P(prod)
    |           if new_p > old_p:
    |             new_tree = Tree(prod.lhs, t[1], t[2], ..., t[n])
    |             MLC[start, start+width, prod.lhs] = new_tree
    | Return MLC[0, len(text), start_symbol]

    :type _grammar: PCFG
    :ivar _grammar: The grammar used to parse sentences.
    :type _trace: int
    :ivar _trace: The level of tracing output that should be generated
        when parsing a text.

    """

    def __init__(self, grammar, trace=0):
        """
        Create a new ``ViterbiParser`` parser, that uses ``grammar`` to
        parse texts.

        """
        self._grammar = grammar
        self._trace = trace


    def grammar(self):
        return self._grammar


    def trace(self, trace=2):
        """
        Set the level of tracing output that should be generated when
        parsing a text.

        :type trace: int
        :param trace: The trace level.  A trace level of ``0`` will
            generate no tracing output; and higher trace levels will
            produce more verbose tracing output.
        :rtype: None

        """
        self._trace = trace


    def parse(self, tokens):
        # Inherit docs from ParserI

        tokens = list(tokens)
        self._grammar.check_coverage(tokens)

        # The most likely constituent table.  This table specifies the
        # most likely constituent for a given span and type.
        # Constituents can be either Trees or tokens.  For Trees,
        # the "type" is the Nonterminal for the tree's root node
        # value.  For Tokens, the "type" is the token's type.
        # The table is stored as a dictionary, since it is sparse.
        constituents = {}

        # Initialize the constituents dictionary with the words from
        # the text.
        if self._trace:
            print("Inserting tokens into the most likely" + " constituents table...")
        for index in range(len(tokens)):
            token = tokens[index]
            constituents[index, index + 1, token] = token
            if self._trace > 1:
                self._trace_lexical_insertion(token, index, len(tokens))

        # Consider each span of length 1, 2, ..., n; and add any trees
        # that might cover that span to the constituents dictionary.
        for length in range(1, len(tokens) + 1):
            if self._trace:
                print(
                    "Finding the most likely constituents"
                    + " spanning %d text elements..." % length
                )
            for start in range(len(tokens) - length + 1):
                span = (start, start + length)
                self._add_constituents_spanning(span, constituents, tokens)

        # Return the tree that spans the entire text & have the right cat
        tree = constituents.get((0, len(tokens), self._grammar.start()))
        if tree is not None:
            yield tree


    def _add_constituents_spanning(self, span, constituents, tokens):
        """
        Find any constituents that might cover ``span``, and add them
        to the most likely constituents table.

        """
        # Since some of the grammar productions may be unary, we need to
        # repeatedly try all of the productions until none of them add any
        # new constituents.
        changed = True
        while changed:
            changed = False

            # Find all ways instantiations of the grammar productions that
            # cover the span.
            instantiations = self._find_instantiations(span, constituents)

            # For each production instantiation, add a new
            # ProbabilisticTree whose probability is the product
            # of the childrens' probabilities and the production's
            # probability.
            for (production, children) in instantiations:
                subtrees = [c for c in children if isinstance(c, Tree)]
                p = reduce(lambda pr, t: pr * t.prob(), subtrees, production.prob())
                node = production.lhs().symbol()
                tree = ProbabilisticTree(node, children, prob=p)

                # If it's new a constituent, then add it to the
                # constituents dictionary.
                c = constituents.get((span[0], span[1], production.lhs()))
                if self._trace > 1:
                    if c is None or c != tree:
                        if c is None or c.prob() < tree.prob():
                            print("   Insert:", end=" ")
                        else:
                            print("  Discard:", end=" ")
                        self._trace_production(production, p, span, len(tokens))
                if c is None or c.prob() < tree.prob():
                    constituents[span[0], span[1], production.lhs()] = tree
                    changed = True

    def _find_instantiations(self, span, constituents):
        """
        :return: a list of the production instantiations that cover a
            given span of the text.  A "production instantiation" is
            a tuple containing a production and a list of children,
            where the production's right hand side matches the list of
            children; and the children cover ``span``.  :rtype: list
            of pair of Production, (list of
            (ProbabilisticTree or token.
        """
        rv = []
        for production in self._grammar.productions():
            childlists = self._match_rhs(production.rhs(), span, constituents)

            for childlist in childlists:
                rv.append((production, childlist))
        return rv

    def _match_rhs(self, rhs, span, constituents):
        """
        :return: a set of all the lists of children that cover ``span``
            and that match ``rhs``.
        :rtype: list(list(ProbabilisticTree or token)
        """
        (start, end) = span

        # Base case
        if start >= end and rhs == ():
            return [[]]
        if start >= end or rhs == ():
            return []

        # Find everything that matches the 1st symbol of the RHS
        childlists = []
        for split in range(start, end + 1):
            l = constituents.get((start, split, rhs[0]))
            if l is not None:
                rights = self._match_rhs(rhs[1:], (split, end), constituents)
                childlists += [[l] + r for r in rights]

        return childlists

    def _trace_production(self, production, p, span, width):
        """
        Print trace output indicating that a given production has been
        applied at a given location.
        """

        str = "|" + "." * span[0]
        str += "=" * (span[1] - span[0])
        str += "." * (width - span[1]) + "| "
        str += "%s" % production
        if self._trace > 2:
            str = f"{str:<40} {p:12.10f} "

        print(str)

    def _trace_lexical_insertion(self, token, index, width):
        str = "   Insert: |" + "." * index + "=" + "." * (width - index - 1) + "| "
        str += f"{token}"
        print(str)

    def __repr__(self):
        return "<ViterbiParser for %r>" % self._grammar
