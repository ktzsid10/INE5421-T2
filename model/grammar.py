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
        pass

    def remove_unproductive(self):
        pass

    def remove_unreachable(self):
        pass

    def t_epsilon(self):
        pass

    def remove_simple_productions(self):
        pass

    def t_proper(self):
        pass

    def remove_left_recursion(self):
        pass
