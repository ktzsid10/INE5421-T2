# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático II Junho 2018

import json
import re
import copy
import itertools
from collections import OrderedDict

NON_TERMINAL='[A-Z][0-9]*'
TERMINAL='([a-z]|[0-9]|\+|-|\*|_|%|#|@|\?|!|;|/|\(|\))*'
SEQUENCE='(( +(' + NON_TERMINAL + '|' + TERMINAL + '))*| +& ?)'
GRAMMAR_INPUT=NON_TERMINAL + ' +->' + SEQUENCE  + '(\|' + SEQUENCE + ')*'

class Grammar():

    def __init__(self, text=None):
        self.productions = OrderedDict()
        self._first = dict()
        self._follow = dict()
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
        self._first = dict()
    
        #Step 2 of class algorithm
        for k,v in self.productions.items():
            first_set = set()
            for prod in v:
                symbols = prod.strip().split(' ')
                if self._is_terminal(symbols[0]) or symbols[0] == '&':
                    first_set.add(symbols[0])
            
                self._first[k] = first_set

        first_copy = copy.deepcopy(self._first)
        #Step 3 of class algorithm      
        while(True):
            for k,v in self.productions.items():
                first_set = set()
                for prod in v:
                    symbols = prod.strip().split(' ')
                    for i in range(len(symbols)):
                        first_nt = set()
                        if not self._is_terminal(symbols[i]) and symbols[i] != '&':
                            first_nt = first_nt | self._first[symbols[i]]
                            if '&' not in first_nt or i == (len(symbols) - 1):
                                first_set = first_set | first_nt
                                break
                        else:
                            first_set = first_set | first_nt
                            first_set.add(symbols[i])
                            break

                        first_set = first_set | first_nt

                if first_set != set():
                    self._first[k] = first_set

            if first_copy == self._first:
                break
            else:
                first_copy = copy.deepcopy(self._first)


    def firstNT(self):
        pass

    def follow(self):
        self.first()
        follow = self._first.fromkeys(self._first, set())
        follow_copy = copy.deepcopy(follow)
        #Step 1
        follow[self.initial_symbol()] = {'$'}

        while(True):
            for k,v in self.productions.items():
                for prod in v:
                    symbols = prod.strip().split(' ')
                    for i in range(len(symbols)):
                        #Step 2: B is non-terminal and has a Beta different of & after him
                        if not self._is_terminal(symbols[i]) and symbols[i] != '&' and (i < len(symbols) - 1):
                            #Step 2.a: Beta is a terminal
                            if self._is_terminal(symbols[i+1]):
                                follow[symbols[i]].add(symbols[i+1])
                            elif symbols[i+1] != '&':
                                #Step 2.b: Beta is non-terminal
                                follow[symbols[i]] = follow[symbols[i]] | self.first_sequence(symbols[i+1:])
                                #Step 3.b: & belongs to First(Beta)

                                if '&' in self.first_sequence(symbols[i+1:]):
                                    follow[symbols[i]] = follow[symbols[i]] | follow[k]
                        #Step 3.a: B is production's last symbol and non-terminal
                        elif not self._is_terminal(symbols[i]) and symbols[i] != '&':
                            follow[symbols[i]] = follow[symbols[i]] | follow[k]
            
            if follow_copy == follow:
                break
            else:
                follow_copy = copy.deepcopy(follow)
        
        return self.remove_epsilon_from_follow(follow)

    def remove_epsilon_from_follow(self, follow):
        for f in follow.values():
            f.discard('&')
        
        return follow

    def first_sequence(self, sequence):
        first = set()
        for i in range(len(sequence)):
            first.discard('&')
            if self._is_terminal(sequence[i]):
                first.add(sequence[i])
                break
            else:
                first = first | self._first[sequence[i]]
                if '&' not in first:
                    break

        return first

    def factorable(self):
        pass
    
    def remove_left_recursion(self):
        pass

    def check_empty(self):
        self.remove_unproductive()
        # NEED TO CHECK INFITE OR FINITE

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
        new_prods = copy.deepcopy(self.productions)
        for k in self.productions.keys():
            if k not in new_nf:
                if k != self.initial_symbol():
                    new_prods.pop(k)
                else:
                    raise ValueError('Initial symbol is not productive! The grammar recognizes empty language.')

        self.productions = new_prods
        for k, v in self.productions.items():
            prod_set = set()
            for p in v:
                symbols = p.split(' ')
                test = True
                for s in symbols:
                    if re.fullmatch(NON_TERMINAL, s) is not None:
                        if s not in new_nf:
                            test = False
                if test:
                    prod_set.add(p)
            
            self.edit_key(k, k, prod_set)

        return new_nf

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
        new_prods = copy.deepcopy(self.productions)
        for k in self.productions.keys():
            if k not in new_v:
                new_prods.pop(k)
        self.productions = new_prods

        return new_v

    def t_epsilon(self):
        old_ne = set()
        new_ne = set()
        for k, v in self.productions.items():
            for p in v:
                if p == '&':
                    new_ne.add(k)

        while new_ne != old_ne:
            old_ne = new_ne.copy()
            for k, v in self.productions.items():
                for p in v:
                    if self._is_in_ne(old_ne, p):
                        new_ne.add(k)
                        break

        print('NE set: ' + str(new_ne))

        for k, v in self.productions.items():
            new_prod = set()
            for p in v:
                if p == '&':
                    continue
                else:
                    [new_prod.add(new_p) for new_p in self._prod_combinations(new_ne, p)]
            self.edit_key(k, k, new_prod)

        if self.initial_symbol() in new_ne:
            new_prods = OrderedDict()
            i = 0
            new_key = self.initial_symbol() + str(i)
            while new_key in self.productions.keys():
                i += 1
                new_key = self.initial_symbol() + str(i)

            new_prods[new_key] = {self.initial_symbol(), '&'}

            for k, v in self.productions.items():
                new_prods[k] = v

            self.productions = new_prods
        
        return new_ne

    def _is_in_ne(self, old_ne, p):
        symbols = [s for s in p.split(' ') if s != '']
        for s in symbols:
            if s not in old_ne:
                return False
        
        return True
        
    def _prod_combinations(self, ne, p):
        new_prods = set()
        symbols = [s for s in p.split(' ') if s != '']
        non_terminal_s = set()
        for s in symbols:
            if re.fullmatch(NON_TERMINAL, s) is not None:
                if s in ne:
                    non_terminal_s.add(s)
        
        powerset = self._power_set(non_terminal_s)
        for combination in powerset:
            new_symbols = symbols.copy()

            for s in combination:
                new_symbols.remove(str(s))

            prod = ''
            for new_s in new_symbols:
                prod += new_s
                prod += ' '
            if prod != '':
                new_prods.add(prod.strip())

        return new_prods

    def _power_set(self, iterable):
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

    def remove_simple_productions(self):
        self.t_epsilon()
        first_na = dict()
        for k, v in self.productions.items():
            first_na[k] = {k}
            for p in v:
                if re.fullmatch(NON_TERMINAL, p.strip()) is not None:
                    first_na[k].add(p.strip())
        
        na = copy.deepcopy(first_na)
        for k, v in first_na.items():
            for p in v:
                if k != p.strip():
                    [na[k].add(new_p) for new_p in first_na[p]]

        print('NA dict: '+str(na))

        for k, v in self.productions.items():
            new_prod = set()
            for p in v:
                if re.fullmatch(NON_TERMINAL, p.strip()) is None:
                    new_prod.add(p)
            self.edit_key(k, k, new_prod)
        
        for k, v in na.items():
            for p in v:
                if k != p.strip():
                    new_prod = self.productions[p.strip()]
                    self.edit_key(k, k, self.productions[k]|new_prod)

        return na

    def t_proper(self):
        ne = self.t_epsilon()
        grammar_1 = copy.deepcopy(self)
        na = self.remove_simple_productions()
        grammar_2 = copy.deepcopy(self)
        nf = self.remove_unproductive()
        vi = self.remove_unreachable()
        return (grammar_1, grammar_2, nf, vi, ne, na)
