#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class DraftTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        main_layout = QtGui.QVBoxLayout()

        # Draft History
        self.list = QtGui.QListView()
        self.model = QtGui.QStandardItemModel()

        # Next Pick
        self.round_num = 0
        self.picking_team = 0
        self.round_num_label = QtGui.QLabel()
        self.picking_team_label = QtGui.QLabel()
        self.player_input = QtGui.QLineEdit()
        self.position_input = QtGui.QLineEdit()

        draft_history = self.draftHistoryView()
        next_pick = self.nextPickView()

        main_layout.addWidget(draft_history)
        main_layout.addWidget(next_pick)
        self.setLayout(main_layout)

    def draftHistoryView(self):
        self.list.setMinimumSize(400,200)
        self.list.setModel(self.model)

        return self.list

    def nextPickView(self):
        picking_group_box = QtGui.QGroupBox(self.tr("Next Pick"))

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        round_label = QtGui.QLabel(self.tr("Round:"))
        team_label = QtGui.QLabel(self.tr("Team:"))
        self.updatePickView()

        player_label = QtGui.QLabel(self.tr("Player:"))
        position_label = QtGui.QLabel(self.tr("Pos:"))

        draft_player_btn = QtGui.QPushButton("Draft Player")
        draft_player_btn.clicked.connect(self.draftPlayer)

        grid.addWidget(round_label, 1, 0)
        grid.addWidget(self.round_num_label, 1, 1)
        grid.addWidget(team_label, 1, 2)
        grid.addWidget(self.picking_team_label, 1, 3)

        grid.addWidget(player_label, 2, 0)
        grid.addWidget(self.player_input, 2, 1)
        grid.addWidget(position_label, 2, 2)
        grid.addWidget(self.position_input, 2, 3)

        grid.addWidget(draft_player_btn, 3, 0, 3, 4)
        picking_group_box.setLayout(grid)

        return picking_group_box

    def updatePickView(self):
        self.round_num_label.setText(self.tr(str(self.getRound())))
        self.picking_team_label.setText(self.tr(self.getPickingTeam()))

    def getRound(self):
        return self.round_num

    def getPickingTeam(self):
        return "My Team"

    def draftPlayer(self):
        drafted_player = QtGui.QStandardItem(self.player_input.text())
        self.model.appendRow(drafted_player)
        self.round_num += 1
        self.updatePickView()