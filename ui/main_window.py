# Joao Victor Fagundes
# Salomao Rodrigues Jacinto
# INE5421 - Trabalho Prático II Junho 2018

import re
import copy
from model.grammar import Grammar
from ui.main_window_ui import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QInputDialog, QFileDialog, QTableWidgetItem)

NON_TERMINAL='[A-Z][0-9]*'
TERMINAL='([a-z]|[0-9]|\+|-|\*|_|%|#|@|\?|!|/|\(|\))*'
SEQUENCE='(( +(' + NON_TERMINAL + '|' + TERMINAL + '))*| +& ?)'
GRAMMAR_INPUT=NON_TERMINAL + ' +->' + SEQUENCE  + '(\|' + SEQUENCE + ')*'

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)

        self._grammar = Grammar()
        self._grammar_list = list()
        self._item_data = ''

        #Grammar Buttons
        self.importGrammarButton.clicked.connect(self.import_grammar)
        self.exportGrammarButton.clicked.connect(self.export_grammar)
        self.addProdButton.clicked.connect(self.add_production)
        self.removeProdButton.clicked.connect(self.remove_production)
        self.firstButton.clicked.connect(self.first)
        self.firstNTButton.clicked.connect(self.firstNT)
        self.followButton.clicked.connect(self.follow)
        self.factorableButton.clicked.connect(self.factorable)
        self.checkEmptyButton.clicked.connect(self.check_empty)

        #Grammar Production List Connectors
        self.productionList.itemClicked.connect(self.grammar_item_clicked)
        self.productionList.itemDoubleClicked.connect(self.grammar_item_double_clicked)
        self.productionList.itemChanged.connect(self.update_grammar)

        #Grammar List
        self.grammarList.itemDoubleClicked.connect(self.grammar_list_double_clicked)

        #Grammar Operations
        self.actionRemove_Unproductive.triggered.connect(self.remove_unproductive)
        self.actionRemove_Unreachable.triggered.connect(self.remove_unreachable)
        self.actionTransform_into_Epsilon_free.triggered.connect(self.t_epsilon)
        self.actionRemove_Simple_Productions.triggered.connect(self.remove_simple_productions)
        self.actionTransform_into_Proper_Grammar.triggered.connect(self.t_proper)
        self.actionRemove_Left_Recursion.triggered.connect(self.remove_left_recursion)

    def add_grammar_to_list(self):
        if self.productionList.count() != 0:
            text, ok = QInputDialog.getText(self, 'Replace Grammar', 'You are going to '+
                            'replace the current grammar, give it a name or cancel to '+
                            'not add it to the list: ')
            if ok:
                new_grammar = copy.deepcopy(self._grammar)
                self._grammar_list.append(new_grammar)
                self.grammarList.addItem(text)

    def grammar_list_double_clicked(self, item):
        self.add_grammar_to_list()
        index = self.grammarList.row(item)
        self._grammar = self._grammar_list[index]
        self.update_production_list()

    def validate_grammar(self, grammar):
        for k, v in grammar.productions.items():
            text = k + ' -> '
            for p in v:
                text += p + ' | '
            if re.fullmatch(GRAMMAR_INPUT, text[:-2]) is None:
                return False

        return True

    def import_grammar(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            try:
                self.add_grammar_to_list()
                grammar = Grammar()
                grammar.load(path)
                if self.validate_grammar(grammar):
                    self._grammar = grammar
                    self.update_production_list()
                else:
                    QMessageBox.critical(self, 'Error', 'Not a valid grammar')

            except ValueError as error:
                QMessageBox.critical(self, 'Error', error.args[0])

    def export_grammar(self):
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self._grammar.save(path)

    def add_production(self):
        if self.productionList.count() == 0:
            text, ok = QInputDialog.getText(
                self, 'Add Initial Production', 'Input a production: ')

            if ok:
                while re.fullmatch(GRAMMAR_INPUT, text) is None:
                    text, ok = QInputDialog.getText(self, 'Add Initial Production',
                        'Invalid Production!')
                    if ok or not ok:
                        if text == '':
                            return

                self.productionList.addItem(text)
                key, set_values = text.split(' ->')
                values = [s.strip() for s in set_values.split('|')]
                self._grammar.add(key, set(values))

        else:
            text, ok = QInputDialog.getText(
                self, 'Add Production', 'Input a production: ')

            if ok:
                while re.fullmatch(GRAMMAR_INPUT, text) is None:
                    text, ok = QInputDialog.getText(self, 'Add Production',
                        'Invalid Production!')
                    if ok or not ok:
                        if text == '':
                            return

                key, set_values = text.split(' ->')
                values = [s.strip() for s in set_values.split('|')]
                keys = self._grammar.productions.keys()
                if key not in keys:
                    self.productionList.addItem(text)
                    self._grammar.add(key, set(values))
                else:
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()

    def remove_production(self):
        for item in self.productionList.selectedItems():
            key = item.text().split(' ->')[0]
            self._grammar.remove(key)
            self.productionList.takeItem(self.productionList.row(item))

    def grammar_item_clicked(self, item):
        self.productionList.itemChanged.disconnect(self.update_grammar)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self._item_data=item.text()
        self.productionList.itemChanged.connect(self.update_grammar)

    def grammar_item_double_clicked(self, item):
        self.productionList.itemChanged.disconnect(self.update_grammar)
        item.setText(self._item_data)
        self.productionList.itemChanged.connect(self.update_grammar)

    def update_grammar(self, item):
        self.productionList.itemChanged.disconnect(self.update_grammar)
        keys = self._grammar.productions.keys()
        if self.productionList.indexFromItem(item).row() == 0:
            if re.fullmatch(GRAMMAR_INPUT, item.text()) is None:
                item.setText(self._item_data)
                self.message.setText('Invalid Production')
                self.message.show()
            else:
                key, set_values = item.text().split(' ->')
                values = [s.strip() for s in set_values.split('|')]
                old_key = self._item_data.split(' ->')[0]
                if key not in keys or key == old_key:
                    self._grammar.edit_key(old_key, key, set(values))
                else:
                    item.setText(self._item_data)
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()

        else:
            if re.fullmatch(GRAMMAR_INPUT, item.text()) is None:
                item.setText(self._item_data)
                self.message.setText('Invalid Production!')
                self.message.show()
            else:
                key, set_values = item.text().split(' ->')
                values = [s.strip() for s in set_values.split('|')]
                old_key = self._item_data.split(' ->')[0]
                if key not in keys or key == old_key :
                    self._grammar.edit_key(old_key, key, set(values))
                else:
                    item.setText(self._item_data)
                    self.message.setText('This non terminal symbol already exists!')
                    self.message.show()

        self.productionList.itemChanged.connect(self.update_grammar)

    def update_production_list(self):
        self.productionList.clear()
        for k, v in self._grammar.productions.items():
            if v == set():
                continue
            text = k + ' -> '
            for p in v:
                text += p + ' | '
            self.productionList.addItem(text[:-2])

    #PROGRAM LOGIC FUNCTIONS
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
