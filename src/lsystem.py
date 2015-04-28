import random
import re

class LContextRule(object):
    def __init__(self, prefex='', token='', postfix=''):
        self.prefix = prefix
        self.token = token
        self.postfix = postfix
        self._str = self.prefix + self.token + self.postfix

    def __len__(self):
        return len(self._str)
    
    def __str__(self):
        return self._str

class LGrammar(dict):
    def __init__(self, grammar=None):
        super(LGrammar, self).__init__()
        if grammar == None:
            grammar = {}
        self.update(grammar)

    def update(self, grammar):
        for key in grammar:
            rules = grammar[key]
            if isinstance(rules, basestring):
                rules = [{"rule": rules}]
            for rule in rules:
                if not isinstance(rule, dict):
                    rule = {"rule": rule}
                self.add_rule(key, **rule)

    def add_rule(self, token, rule='', weight=1, prefix='', postfix=''):
        if token not in self:
            self[token] = []
        rule = {"rule": rule, "prefix": prefix, "postfix": postfix, "weight": weight}
        self[token].append(rule)

class LCursor(object):
    def __init__(self, lstring):
        if isinstance(lstring, basestring):
            lstring = iter(lstring)
        self.lstring = lstring
        self.token_index = -1
        self.cache = ''
        self.token = None

    def __iter__(self):
        return self
    
    def next(self):
        self.token_index += 1
        return self[self.token_index]

    def __getitem__(self, idx):
        if type(idx) == slice:
            start = self.token_index + idx.start
            stop = self.token_index + idx.stop
            idx = slice(start, stop)
        else:
            stop = idx
        while len(self.cache) < (stop + 1):
            self.cache += self.lstring.next()
        return self.cache[idx]

class LState(object):
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, lstring):
        cursor = LCursor(lstring)
        for token in cursor:
            for ch in self.expand(token, cursor):
                yield ch

    def select_rule(self, rules):
        wtotal = sum(rule["weight"] for rule in rules)
        choice = random.uniform(0, wtotal)
        offset = 0
        for rule in rules:
            if rule["weight"] + offset > choice:
                return rule
            offset += rule["weight"]

    def check_prefix(self, prefix, cursor):
        if not prefix:
            return True
        print "PRE", prefix, cursor[-len(prefix):0]
        return prefix == cursor[-len(prefix):0]

    def check_postfix(self, postfix, cursor):
        if not postfix:
            return True
        print "POST", postfix, cursor[0:len(postfix)]
        return postfix == cursor[0:len(postfix)]

    def expand(self, token, cursor):
        if token not in self.grammar:
            return token
        rlist = self.grammar[token]
        rule_matches = []
        for rule in rlist:
            prefix = rule["prefix"]
            postfix = rule["postfix"]
            if not self.check_prefix(prefix, cursor):
                continue
            if not self.check_postfix(postfix, cursor):
                continue
            if prefix and postfix:
                print "matched context rule"
            rule_matches.append(rule)
        if len(rule_matches) == 1:
            rule = rule_matches[0]
        else:
            rule = self.select_rule(rule_matches)
        return rule["rule"]

class LSystem(object):
    def __init__(self, grammar):
        if not isinstance(grammar, LGrammar):
            grammar = LGrammar(grammar)
        self.grammar = grammar
        
    def process(self, tokens):
        state = LState(self.grammar)
        return state.parse(tokens)

    def solve(self, axiom='', iterations=0):
        chain = axiom
        for iteration in range(iterations):
            chain = self.process(chain)
        return chain
