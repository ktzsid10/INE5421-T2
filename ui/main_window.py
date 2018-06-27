# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático II Junho 2018

import copy
from model.grammar import Grammar
from ui.main_window_ui import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QInputDialog, QFileDialog, QTableWidgetItem)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)

        self._grammar = Grammar()
        self._grammar_list = list()

        #Grammar Buttons
        self.listButton.clicked.connect(self.add_grammar_to_list)
        self.importGrammarButton.clicked.connect(self.import_grammar)
        self.exportGrammarButton.clicked.connect(self.export_grammar)

        self.firstButton.clicked.connect(self.first)
        self.firstNTButton.clicked.connect(self.firstNT)
        self.followButton.clicked.connect(self.follow)
        self.factorableButton.clicked.connect(self.factorable)
        self.checkEmptyButton.clicked.connect(self.check_empty)
        self.runproductiveButton.clicked.connect(self.remove_unproductive)
        self.runreachableButton.clicked.connect(self.remove_unreachable)
        self.rsimpleProdButton.clicked.connect(self.remove_simple_productions)
        self.rleftrecursionButton.clicked.connect(self.remove_left_recursion)
        self.tepsilonButton.clicked.connect(self.t_epsilon)
        self.tproperButton.clicked.connect(self.t_proper)

        #Grammar List
        self.grammarList.itemDoubleClicked.connect(self.grammar_list_double_clicked)

    def add_grammar_to_list(self):
        if self.update_grammar():
            text, ok = QInputDialog.getText(self, 'Grammar List', 'Give the grammar a name: ')
            if ok:
                new_grammar = copy.deepcopy(self._grammar)
                self._grammar_list.append(new_grammar)
                self.grammarList.addItem(text)

    def update_production_text(self):
        grammar_text = ''
        for k, v in self._grammar.productions.items():
            if v == set():
                continue
            text = k + ' -> '
            for p in v:
                text += p + ' | '
            grammar_text += text[:-2]+'\n'

        self.prodTextEdit.setPlainText(grammar_text)

    def update_grammar(self):
        try:
            self._grammar = Grammar(self.prodTextEdit.toPlainText())
            return True
        except ValueError as error:
            QMessageBox.critical(self, 'Error', error.args[0])
            return False

    def grammar_list_double_clicked(self, item):
        index = self.grammarList.row(item)
        self._grammar = self._grammar_list[index]
        self.update_production_text()

    def import_grammar(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            try:
                grammar = Grammar()
                grammar.load(path)
                if grammar.validate_grammar():
                    self._grammar = grammar
                    self.update_production_text()
                else:
                    QMessageBox.critical(self, 'Error', 'Not a valid grammar')

            except ValueError as error:
                QMessageBox.critical(self, 'Error', error.args[0])

    def export_grammar(self):
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self.update_grammar()
            self._grammar.save(path)

    #PROGRAM LOGIC FUNCTIONS
    def first(self):
        if not self.update_grammar():
            return

        first = self._grammar.first()
        nt = set()
        text = ''
        for k,v in first.items():
            if k not in nt:
                text += '\nFirst({}): '.format(k)
                text += '{}'.format(v)
                nt.add(k)
            else:
                text += ', {}'.format(v)
            
        QMessageBox.information(self, 'First', text)

    def firstNT(self):
        pass

    def follow(self):
        if not self.update_grammar():
            return

        follow = self._grammar.follow()
        nt = set()
        text = ''
        for k,v in follow.items():
            if k not in nt:
                text += '\nFollow({}): '.format(k)
                text += '{}'.format(v)
                nt.add(k)
            else:
                text += ', {}'.format(v)
            
        QMessageBox.information(self, 'Follow', text)

    def factorable(self):
        pass

    def remove_left_recursion(self):
        pass

    def check_empty(self):
        if not self.update_grammar():
            return
        
        grammar = copy.deepcopy(self._grammar)
        try:
            grammar.remove_unproductive()
        except ValueError as error:
            QMessageBox.information(self, 'Empty', error.args[0])
            return
        
        # NEED TO CHECK FINITE OR INFINITE

    def remove_unproductive(self):
        if not self.update_grammar():
            return

        try:
            grammar = copy.deepcopy(self._grammar)
            grammar.remove_unproductive()
            self._grammar = grammar
            self.update_production_text()
        except ValueError as error:
            QMessageBox.critical(self, 'Error', error.args[0])

    def remove_unreachable(self):
        if not self.update_grammar():
            return
        
        try:
            grammar = copy.deepcopy(self._grammar)
            grammar.remove_unreachable()
            self._grammar = grammar
            self.update_production_text()
        except ValueError as error:
            QMessageBox.critical(self, 'Error', error.args[0])

    def t_epsilon(self):
        if not self.update_grammar():
            return

        self._grammar.t_epsilon()
        self.update_production_text()

    def remove_simple_productions(self):
        if not self.update_grammar():
            return

        self._grammar.remove_simple_productions()
        self.update_production_text()

    def t_proper(self):
        grammars = self._grammar.t_proper()
        self._grammar_list.append(grammars[0])
        self.grammarList.addItem('intermediate epsilon free')
        self._grammar_list.append(grammars[1])
        self.grammarList.addItem('intermediate removing simple productions')
        self._grammar_list.append(copy.deepcopy(self._grammar))
        self.grammarList.addItem('final proper grammar')
        self.update_production_text()
        text = ('NF: '+str(grammars[2])+'\nVI: '+str(grammars[3])+
                '\nNE: '+str(grammars[4])+'\nNA: '+str(grammars[5]))
        QMessageBox.information(self, 'Sets', text)
