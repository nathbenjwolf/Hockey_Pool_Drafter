#!/usr/bin/python

import sys
from PySide import QtGui, QtCore
from Player import Player
from Globals import Globals


class DraftedPlayer(QtGui.QWidget):
    def __init__(self, pick_num, round_num, team_num, player, pos, parent):
        super(DraftedPlayer, self).__init__(parent)
        self.data = parent.data
        self.team_num = team_num
        self.round_num = round_num

        self.allQHBoxLayout = QtGui.QHBoxLayout()

        self.pick_num_label = QtGui.QLabel(str(pick_num))
        self.pick_num_label.setFont(Globals.medium_bold_font)
        self.round_num_label = QtGui.QLabel(str(self.round_num))
        self.round_num_label.setFont(Globals.medium_bold_font)
        self.team_label = QtGui.QLabel(self.data.teams[self.team_num])
        self.team_label.setFont(Globals.medium_font)
        self.player_label = QtGui.QLabel(player)
        self.player_label.setFont(Globals.medium_font)
        self.position_label = QtGui.QLabel(pos)
        self.position_label.setFont(Globals.medium_font)

        self.allQHBoxLayout.addWidget(self.pick_num_label, 1)
        self.allQHBoxLayout.addWidget(self.round_num_label, 1)
        self.allQHBoxLayout.addWidget(self.team_label, 10)
        self.allQHBoxLayout.addWidget(self.player_label, 10)
        self.allQHBoxLayout.addWidget(self.position_label, 0)

        self.setLayout(self.allQHBoxLayout)

    def updateTeamName(self):
        self.team_label.setText(self.data.teams[self.team_num])

    def updatePlayerName(self):
        self.player_label.setText(self.data.teams_players[self.team_num][self.round_num-1].name)


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
        self.picking_team = self.getPickingTeam()
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

        grid.addWidget(team_label, 1, 0)
        grid.addWidget(self.picking_team_label, 1, 1)
        grid.addWidget(round_label, 1, 2)
        grid.addWidget(self.round_num_label, 1, 3)

        grid.addWidget(player_label, 2, 0)
        grid.addWidget(self.player_input, 2, 1)
        grid.addWidget(position_label, 2, 2)
        grid.addWidget(self.position_input, 2, 3)

        grid.addWidget(draft_player_btn, 3, 0, 3, 4)
        picking_group_box.setLayout(grid)

        return picking_group_box

    def updatePickView(self):
        self.round_num_label.setText(self.tr(str(self.getRound())))
        self.picking_team_label.setText(self.tr(self.getPickingTeamName()))

    def getRound(self):
        # Plus 1 to account for the zero index (visually more correct first = 1)
        return self.round_num+1

    def getPickingTeamName(self):
        if self.picking_team == -1:
            return "<Must add teams>"
        else:
            return self.data.teams[self.picking_team]

    def getPickingTeam(self):
        if len(self.data.teams) == 0:
            return -1
        else:
            return self.data.draft_order[self.round_pick]

    def getNextPick(self):
        if self.round_num % 2 == 0:
            # even rounds go from head to tail of snake
            if self.round_pick+1 >= len(self.data.teams):
                self.round_num += 1
                # next round is odd
                self.round_pick = len(self.data.teams)-1
            else:
                self.round_pick += 1
        else:
            # odd rounds go from tail to head of snake
            if self.round_pick-1 < 0:
                self.round_num += 1
                # next round is even
                self.round_pick = 0
            else:
                self.round_pick -= 1

        self.picking_team = self.data.draft_order[self.round_pick]
        self.updatePickView()

    def getOverallPickNum(self):
        if self.round_num % 2 == 0:
            # Plus 1 to account for zero index
            return self.round_num * len(self.data.teams) + self.round_pick + 1
        else:
            # Odd round (tail->head) need to account for
            return self.round_num * len(self.data.teams) + (len(self.data.teams) - self.round_pick)

    def draftPlayer(self):
        player = Player(self.getOverallPickNum(), self.round_num, self.picking_team, self.player_input.text().__str__(), self.position_input.currentText().__str__())
        self.data.draftPlayer(player)

    def updatePlayerDrafted(self, player):
        drafted_player = DraftedPlayer(player.overall_draft_num, player.draft_round+1, player.team, player.name, player.pos, self)
        myQListWidgetItem = QtGui.QListWidgetItem(self.list)
        myQListWidgetItem.setSizeHint(drafted_player.sizeHint())
        self.list.addItem(myQListWidgetItem)
        self.list.setItemWidget(myQListWidgetItem, drafted_player)

        self.getNextPick()

        self.list.scrollToBottom()

        self.player_input.clear()

    def renameTeam(self, team_num):
        self.updatePickView()
        for i in range(self.list.count()):
            drafted_player = self.list.itemWidget(self.list.item(i))
            if drafted_player.team_num == team_num:
                drafted_player.updateTeamName()

    def renamedPlayer(self, team_num, player_index):
        # player_index represents the number of rounds
        if player_index % 2 == 0:
            list_index = player_index*len(self.data.teams) + self.data.draft_order.index(team_num)
        else:
            list_index = player_index*len(self.data.teams) + len(self.data.teams) - (self.data.draft_order.index(team_num) + 1)

        drafted_player = self.list.itemWidget(self.list.item(list_index))
        drafted_player.updatePlayerName()

