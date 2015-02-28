#!/usr/bin/python

import sys
from PySide import QtGui, QtCore
from Player import Player


class DraftedPlayer(QtGui.QWidget):
    def __init__(self, pick_num, round_num, team, player, pos, parent=None):
        super(DraftedPlayer, self).__init__(parent)
        self.allQHBoxLayout = QtGui.QHBoxLayout()

        self.pick_num_label = QtGui.QLabel(str(pick_num))
        self.round_num_label = QtGui.QLabel(str(round_num))
        self.team_label = QtGui.QLabel(team)
        self.player_label = QtGui.QLabel(player)
        self.position_label = QtGui.QLabel(pos)

        self.allQHBoxLayout.addWidget(self.pick_num_label, 1)
        self.allQHBoxLayout.addWidget(self.round_num_label, 1)
        self.allQHBoxLayout.addWidget(self.team_label, 10)
        self.allQHBoxLayout.addWidget(self.player_label, 10)
        self.allQHBoxLayout.addWidget(self.position_label, 0)


        self.setLayout(self.allQHBoxLayout)


class DraftTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.data = parent.pool_data

        main_layout = QtGui.QVBoxLayout()

        # Draft History
        self.list = QtGui.QListWidget()

        # Next Pick
        self.round_num = 0
        self.round_pick = 0
        self.picking_team = self.data.draft_order[self.round_pick]
        self.round_num_label = QtGui.QLabel()
        self.picking_team_label = QtGui.QLabel()
        self.player_input = QtGui.QLineEdit()
        self.position_input = QtGui.QComboBox()

        main_layout.addWidget(self.draftHistoryView())
        main_layout.addWidget(self.nextPickView())
        self.setLayout(main_layout)

    def draftHistoryView(self):
        self.list.setMinimumSize(400,200)
        self.list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.list.setStyleSheet("QListView { alternate-background-color: lightgrey; }")
        self.list.setAlternatingRowColors(True)

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
        self.position_input.addItem("F")
        self.position_input.addItem("D")
        self.position_input.addItem("G")

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
        # Plus 1 to account for the zero index (visually more correct first = 1)
        return self.round_num+1

    def getPickingTeam(self):
        return self.data.teams[self.picking_team]

    def getNextPick(self):
        if self.round_pick+1 >= len(self.data.teams):
            self.round_num += 1
            self.round_pick = 0
        else:
            self.round_pick += 1

        self.picking_team = self.data.draft_order[self.round_pick]
        self.updatePickView()

    def getOverallPickNum(self):
        # Plus 1 to account for zero index
        return self.round_num * len(self.data.teams) + self.round_pick + 1

    def draftPlayer(self):
        player = Player(self.getOverallPickNum(), self.round_num, self.picking_team, self.player_input.text(), self.position_input.currentText())
        if(self.data.canDraftPlayer(player.team, player)):
            self.data.teams_players[player.team].append(player)
        else:
            # Cannot draft player for some reason (player already drafted, or that team can't draft that position anymore)
            return

        drafted_player = DraftedPlayer(player.overall_draft_num, self.getRound(), self.getPickingTeam(), player.name, player.pos)
        myQListWidgetItem = QtGui.QListWidgetItem(self.list)
        myQListWidgetItem.setSizeHint(drafted_player.sizeHint())
        self.list.addItem(myQListWidgetItem)
        self.list.setItemWidget(myQListWidgetItem, drafted_player)

        self.parent.playerDrafted(player.team, player)
        self.getNextPick()

        self.list.scrollToBottom()