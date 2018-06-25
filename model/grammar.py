# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático II Junho 2018

import json
import re
from collections import OrderedDict

NON_TERMINAL='[A-Z][0-9]*'
TERMINAL='([a-z]|[0-9]|\+|-|\*|_|%|#|@|\?|!|/|\(|\))*'
SEQUENCE='(( +(' + NON_TERMINAL + '|' + TERMINAL + '))*| +& ?)'
GRAMMAR_INPUT=NON_TERMINAL + ' +->' + SEQUENCE  + '(\|' + SEQUENCE + ')*'

class Grammar():

    def __init__(self, text=None):
        self.productions = OrderedDict()
        if text is not None:
            if self.validate_text(text):
                self._text_to_dict(text)
            else:
                raise ValueError('Not a valid context free grammar! Each symbol must '+
                                 'be separate with a space.')

    def validate_text(self, text):
        prods = text.splitlines()
        for p in prods:
            if re.fullmatch(GRAMMAR_INPUT, p) is None:
                return False

        return True
    
    def validate_grammar(self):
        for k, v in self.productions.items():
            text = k + ' -> '
            for p in v:
                text += p + ' | '
            if re.fullmatch(GRAMMAR_INPUT, text[:-2]) is None:
                return False

        return True

    def _text_to_dict(self, text):
        prods = text.splitlines()
        for p in prods:
            key, set_values = p.split(' ->')
            values = [s.strip() for s in set_values.split('|')]
            self.add(key, set(values))

    def initial_symbol(self):
        for k in self.productions.keys():
            return k

    def add(self, key, set_values):
        self.productions[key] = set_values

    def remove(self, key):
        self.productions.pop(key)
    
    def edit_key(self, old_key, new_key, set_values):
        self.productions = OrderedDict([(new_key, v) 
                        if k == old_key else (k,v) for k, v in self.productions.items()])
        self.add(new_key, set_values)

    def save(self, path):
        data = {}
        data['object'] = 'grammar'
        data_dict = OrderedDict()
        for k, v in self.productions.items():
            data_dict[k] = sorted(v)
        data['productions'] = data_dict

        with open(path, 'w') as grammar_file:
            json.dump(data, grammar_file, indent=4)

    def load(self, path):
        with open(path, 'r') as grammar_file:
            data = json.load(grammar_file, object_pairs_hook=OrderedDict)

        if data.get('object') == 'grammar':
            for k, v in data.get('productions').items():
                self.productions[k] = set(v)

        else:
            raise ValueError('Not a valid file!')

    def first(self):
        pass

    def firstNT(self):
        pass

    def follow(self):
        pass

    def factorable(self):
        pass

    def check_empty(self):
        self.remove_unproductive()

    def remove_unproductive(self):
        old_nf = set()
        new_nf = set()

        for k, v in self.productions.items():
            for p in v:
                if p == '&' or self._is_terminal(p):
                    new_nf.add(k)
        
        while old_nf != new_nf:
            old_nf = new_nf.copy()
            for k, v in self.productions.items():
                for p in v:
                    if self._is_productive(p, old_nf):
                        new_nf.add(k)

        print('Productive symbols: ' + str(new_nf))
        for k in self.productions.keys():
            if k not in new_nf:
                if k != self.initial_symbol():
                    self.remove(k)
                else:
                    raise ValueError('Initial symbol is not productive! The grammar recognizes empty language.')
                    
    def _is_terminal(self, production):
        symbols = production.split(' ')
        for s in symbols:
            if re.fullmatch(TERMINAL, s) is None:
                return False

        return True

    def _is_productive(self, production, nf_set):
        symbols = production.split(' ')
        for s in symbols:
            if re.fullmatch(TERMINAL, s) is None:
                if s not in nf_set:
                    return False

        return True

    def remove_unreachable(self):
        old_v = {self.initial_symbol()}
        new_v = {self.initial_symbol()}

        for v in self.productions[self.initial_symbol()]:
            for p in v:
                [new_v.add(s) for s in p.split(' ') if s != '']

        while old_v != new_v:
            old_v = new_v.copy()
            for symbol in old_v:
                if re.fullmatch(NON_TERMINAL, symbol) is not None:
                    for v in self.productions[symbol]:
                        [new_v.add(s) for s in v.split(' ') if s != '']
                    
        print('Reachable Symbols: ' + str(new_v))
        for k in self.productions.keys():
            if k not in new_v:
                self.remove(k)

    def t_epsilon(self):
        pass

    def remove_simple_productions(self):
        pass

    def t_proper(self):
        pass

    def remove_left_recursion(self):
        pass
