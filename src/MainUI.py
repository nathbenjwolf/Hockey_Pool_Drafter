#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from PySide import QtCore
import DraftTab
import TeamTab
import ConfigTab
import PoolData

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

        self.pool_data = PoolData.PoolData()

        self.draft_tab = DraftTab.DraftTab(parent=self)
        self.team_tab = TeamTab.TeamTab(parent=self)
        self.config_tab = ConfigTab.ConfigTab(parent=self)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.draft_tab, self.tr("Draft"))
        tabWidget.addTab(self.team_tab, self.tr("Team"))
        tabWidget.addTab(self.config_tab, self.tr("Config"))

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

    def playerDrafted(self, team_num, player):
        self.team_tab.updateTeam(team_num)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    tab_dialog = TabDialog()

    sys.exit(tab_dialog.exec_())
