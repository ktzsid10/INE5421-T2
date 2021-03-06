# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalGrammarList = QtWidgets.QVBoxLayout()
        self.verticalGrammarList.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalGrammarList.setObjectName("verticalGrammarList")
        self.grammarListLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.grammarListLabel.setFont(font)
        self.grammarListLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.grammarListLabel.setObjectName("grammarListLabel")
        self.verticalGrammarList.addWidget(self.grammarListLabel)
        self.grammarList = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grammarList.sizePolicy().hasHeightForWidth())
        self.grammarList.setSizePolicy(sizePolicy)
        self.grammarList.setObjectName("grammarList")
        self.verticalGrammarList.addWidget(self.grammarList)
        self.horizontalLayout_2.addLayout(self.verticalGrammarList)
        self.verticalLayoutMain = QtWidgets.QVBoxLayout()
        self.verticalLayoutMain.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutMain.setSpacing(5)
        self.verticalLayoutMain.setObjectName("verticalLayoutMain")
        self.verticalGlc1 = QtWidgets.QVBoxLayout()
        self.verticalGlc1.setObjectName("verticalGlc1")
        self.grammarLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.grammarLabel.setFont(font)
        self.grammarLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.grammarLabel.setObjectName("grammarLabel")
        self.verticalGlc1.addWidget(self.grammarLabel)
        self.horizontalGlc1 = QtWidgets.QHBoxLayout()
        self.horizontalGlc1.setObjectName("horizontalGlc1")
        self.listButton = QtWidgets.QPushButton(self.centralwidget)
        self.listButton.setObjectName("listButton")
        self.horizontalGlc1.addWidget(self.listButton)
        self.importGrammarButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.importGrammarButton.setFont(font)
        self.importGrammarButton.setObjectName("importGrammarButton")
        self.horizontalGlc1.addWidget(self.importGrammarButton)
        self.exportGrammarButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exportGrammarButton.setFont(font)
        self.exportGrammarButton.setObjectName("exportGrammarButton")
        self.horizontalGlc1.addWidget(self.exportGrammarButton)
        self.verticalGlc1.addLayout(self.horizontalGlc1)
        self.horizontalGlc2 = QtWidgets.QHBoxLayout()
        self.horizontalGlc2.setObjectName("horizontalGlc2")
        self.prodTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.prodTextEdit.setObjectName("prodTextEdit")
        self.horizontalGlc2.addWidget(self.prodTextEdit)
        self.verticalGlc2 = QtWidgets.QVBoxLayout()
        self.verticalGlc2.setObjectName("verticalGlc2")
        self.runproductiveButton = QtWidgets.QPushButton(self.centralwidget)
        self.runproductiveButton.setObjectName("runproductiveButton")
        self.verticalGlc2.addWidget(self.runproductiveButton)
        self.runreachableButton = QtWidgets.QPushButton(self.centralwidget)
        self.runreachableButton.setObjectName("runreachableButton")
        self.verticalGlc2.addWidget(self.runreachableButton)
        self.rsimpleProdButton = QtWidgets.QPushButton(self.centralwidget)
        self.rsimpleProdButton.setObjectName("rsimpleProdButton")
        self.verticalGlc2.addWidget(self.rsimpleProdButton)
        self.tepsilonButton = QtWidgets.QPushButton(self.centralwidget)
        self.tepsilonButton.setObjectName("tepsilonButton")
        self.verticalGlc2.addWidget(self.tepsilonButton)
        self.tproperButton = QtWidgets.QPushButton(self.centralwidget)
        self.tproperButton.setObjectName("tproperButton")
        self.verticalGlc2.addWidget(self.tproperButton)
        self.rleftrecursionButton = QtWidgets.QPushButton(self.centralwidget)
        self.rleftrecursionButton.setObjectName("rleftrecursionButton")
        self.verticalGlc2.addWidget(self.rleftrecursionButton)
        self.checkEmptyButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkEmptyButton.setObjectName("checkEmptyButton")
        self.verticalGlc2.addWidget(self.checkEmptyButton)
        self.firstButton = QtWidgets.QPushButton(self.centralwidget)
        self.firstButton.setObjectName("firstButton")
        self.verticalGlc2.addWidget(self.firstButton)
        self.followButton = QtWidgets.QPushButton(self.centralwidget)
        self.followButton.setObjectName("followButton")
        self.verticalGlc2.addWidget(self.followButton)
        self.firstNTButton = QtWidgets.QPushButton(self.centralwidget)
        self.firstNTButton.setObjectName("firstNTButton")
        self.verticalGlc2.addWidget(self.firstNTButton)
        self.factorableButton = QtWidgets.QPushButton(self.centralwidget)
        self.factorableButton.setObjectName("factorableButton")
        self.verticalGlc2.addWidget(self.factorableButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalGlc2.addItem(spacerItem)
        self.horizontalGlc2.addLayout(self.verticalGlc2)
        self.verticalGlc1.addLayout(self.horizontalGlc2)
        self.verticalLayoutMain.addLayout(self.verticalGlc1)
        self.horizontalLayout_2.addLayout(self.verticalLayoutMain)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.grammarListLabel.setText(_translate("MainWindow", "Grammar List"))
        self.grammarLabel.setText(_translate("MainWindow", "Context Free Grammar"))
        self.listButton.setText(_translate("MainWindow", "Put In The List"))
        self.importGrammarButton.setText(_translate("MainWindow", "Import Grammar"))
        self.exportGrammarButton.setText(_translate("MainWindow", "Export Grammar"))
        self.runproductiveButton.setText(_translate("MainWindow", "Remove Unproductive"))
        self.runreachableButton.setText(_translate("MainWindow", "Remove Unreachable"))
        self.rsimpleProdButton.setText(_translate("MainWindow", "Remove Simple Productions"))
        self.tepsilonButton.setText(_translate("MainWindow", "Epsilon-free"))
        self.tproperButton.setText(_translate("MainWindow", "Proper Grammar"))
        self.rleftrecursionButton.setText(_translate("MainWindow", "Remove Left Recursion"))
        self.checkEmptyButton.setText(_translate("MainWindow", "Empty / Finite / Infinite"))
        self.firstButton.setText(_translate("MainWindow", "First"))
        self.followButton.setText(_translate("MainWindow", "Follow"))
        self.firstNTButton.setText(_translate("MainWindow", "First-NT"))
        self.factorableButton.setText(_translate("MainWindow", "Factorable"))

