#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class TeamTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        ownerGroup = QtGui.QGroupBox(self.tr("Ownership"))

        ownerLabel = QtGui.QLabel(self.tr("Owner"))

        ownerLayout = QtGui.QVBoxLayout()
        ownerLayout.addWidget(ownerLabel)
        ownerGroup.setLayout(ownerLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(ownerGroup)
        self.setLayout(mainLayout)