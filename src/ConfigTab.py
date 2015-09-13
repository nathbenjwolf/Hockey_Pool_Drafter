#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from Globals import Globals

class ConfigTab(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.data = parent.pool_data

        main_layout = QtGui.QVBoxLayout()

        forwards_layout, self.total_forwards_spinbox = self.createNumberEntryWidget("Number of Forwards:", self.data.num_forwards)

        defensemen_layout, self.total_defensemen_spinbox = self.createNumberEntryWidget("Number of Defensemen:", self.data.num_defense)

        goalies_layout, self.total_goalies_spinbox = self.createNumberEntryWidget("Number of Goalies:", self.data.num_goalies)

        self.total_forwards_spinbox.valueChanged.connect(self.forwardsChanged)
        self.total_defensemen_spinbox.valueChanged.connect(self.defensemenChanged)
        self.total_goalies_spinbox.valueChanged.connect(self.goaliesChanged)

        import_layout = QtGui.QHBoxLayout()
        import_layout.addWidget(QtGui.QLabel("Import File:"))
        self.import_file_label = QtGui.QLabel("")
        self.import_file_label.setFont(Globals.small_font)
        import_layout.addWidget(self.import_file_label)
        self.import_file_selection = QtGui.QPushButton("Select File")
        self.import_file_selection.clicked.connect(self.importFileSelection)
        import_layout.addWidget(self.import_file_selection)

        export_layout = QtGui.QHBoxLayout()
        export_layout.addWidget(QtGui.QLabel("Export File:"))
        self.export_file_label = QtGui.QLabel("")
        self.export_file_label.setFont(Globals.small_font)
        export_layout.addWidget(self.export_file_label)
        self.export_file_selection = QtGui.QPushButton("Select File")
        self.export_file_selection.clicked.connect(self.exportFileSelection)
        export_layout.addWidget(self.export_file_selection)

        main_layout.addLayout(forwards_layout)
        main_layout.addLayout(defensemen_layout)
        main_layout.addLayout(goalies_layout)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(export_layout)

        self.setLayout(main_layout)

    def createNumberEntryWidget(self, label, defaultNum):

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel(label))
        spinbox = QtGui.QSpinBox()
        spinbox.setValue(defaultNum)
        layout.addWidget(spinbox)

        return layout, spinbox

    def forwardsChanged(self):
        self.data.setForwards(self.total_forwards_spinbox.value())

    def defensemenChanged(self):
        self.data.setDefense(self.total_defensemen_spinbox.value())

    def goaliesChanged(self):
        self.data.setGoalies(self.total_goalies_spinbox.value())

    def importFileSelection(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Import File', 'FantasyHockeyDraftData.csv', '(*.csv)')
        if fname:
            self.data.setImportPath(fname)

    def exportFileSelection(self):
        fdir = QtGui.QFileDialog.getExistingDirectory(self, 'Export File Location')
        if fdir:
            file_path = fdir.__str__() + '\FantasyHockeyDraftData.csv'
            self.data.setExportPath(file_path)
            self.export_file_label.setText(self.data.export_path)

    # Reactor
    def draftStarted(self):
        self.total_forwards_spinbox.setEnabled(False)
        self.total_defensemen_spinbox.setEnabled(False)
        self.total_goalies_spinbox.setEnabled(False)
        self.import_file_selection.setEnabled(False)

    # Reactor
    def dataImported(self):
        self.total_forwards_spinbox.setValue(self.data.num_forwards)
        self.total_defensemen_spinbox.setValue(self.data.num_defense)
        self.total_goalies_spinbox.setValue(self.data.num_goalies)
        self.import_file_label.setText(self.data.import_path)
        self.export_file_label.setText(self.data.export_path)