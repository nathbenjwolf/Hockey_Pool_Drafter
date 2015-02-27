#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from PySide import QtCore
import DraftTab
import TeamTab
import ConfigTab

# def main():
#
#     app = QtGui.QApplication(sys.argv)
#
#     w = QtGui.QWidget()
#     w.resize(250, 150)
#     w.move(300, 300)
#     w.setWindowTitle('Simple')
#     w.show()
#
#     sys.exit(app.exec_())

# class Form(QDialog):
#     def __init__(self, parent=None):
#         super(Form, self).__init__(parent)
#         self.setWindowTitle("Fantasy Hockey Pool")
#         self.edit = QLineEdit("Write name here")
#         self.button = QPushButton("Press me")
#         layout = QVBoxLayout()
#         layout.addWidget(self.edit)
#         layout.addWidget(self.button)
#         # Set dialog layout
#         self.setLayout(layout)
#         # Add button signal to greetings slot
#         self.button.clicked.connect(self.greetings)
#
#     # Greets the user
#     def greetings(self):
#         print ("Hello %s" % self.edit.text())

class TabDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(DraftTab.DraftTab(), self.tr("Draft"))
        tabWidget.addTab(TeamTab.TeamTab(), self.tr("Team"))
        tabWidget.addTab(ConfigTab.ConfigTab(), self.tr("Config"))

        okButton = QtGui.QPushButton(self.tr("OK"))
        cancelButton = QtGui.QPushButton(self.tr("Cancel"))

        self.connect(okButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Fantasy Hockey Pool"))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    tab_dialog = TabDialog()

    sys.exit(tab_dialog.exec_())
