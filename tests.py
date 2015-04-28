#!/usr/bin/env python

import random
import lsystem
import unittest

DeterministicGrammar = {"1": "11", "0": "1[0]0"}
StochasticGrammar = {"1": "11", "0": ["1[0]0", "1"]}
ContextGrammar = {"a": [{"rule": "aba"}, {"rule": "abc", "prefix": "b", "postfix": "b"}]}

class LSystemTests(unittest.TestCase):
    def test_deterministic_0(self):
        ls = lsystem.LSystem(DeterministicGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=0))
        answer = '0'
        self.assertEquals(answer, response)

    def test_deterministic_1(self):
        ls = lsystem.LSystem(DeterministicGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=1))
        answer = '1[0]0'
        self.assertEquals(answer, response)

    def test_deterministic_2(self):
        ls = lsystem.LSystem(DeterministicGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=2))
        answer = '11[1[0]0]1[0]0'
        self.assertEquals(answer, response)

    def test_stochastic_0(self):
        random.seed(0)
        ls = lsystem.LSystem(StochasticGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=0))
        answer = '0'
        self.assertEquals(answer, response)

    def test_stochastic_1(self):
        random.seed(0)
        ls = lsystem.LSystem(StochasticGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=1))
        answer = '1'
        self.assertEquals(answer, response)
        # test other possible outcome
        random.seed(99)
        ls = lsystem.LSystem(StochasticGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=1))
        answer = '1[0]0'
        self.assertEquals(answer, response)

    def test_stochastic_2(self):
        random.seed(0)
        ls = lsystem.LSystem(StochasticGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=2))
        answer = '11'
        self.assertEquals(answer, response)
        # test other possible outcome
        random.seed(99)
        ls = lsystem.LSystem(StochasticGrammar)
        response = str.join('', ls.solve(axiom='0', iterations=2))
        answer = '11[1[0]0]1[0]0'
        self.assertEquals(answer, response)

    def test_context_0(self):
        ls = lsystem.LSystem(ContextGrammar)
        response = str.join('', ls.solve(axiom='a', iterations=2))
        print response


if __name__ == "__main__":
    unittest.main()
