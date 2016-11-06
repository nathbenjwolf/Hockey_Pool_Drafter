#!/usr/bin/python

import sys
from threading import Event
from PySide import QtGui, QtCore
from Player import Player
from Globals import Globals
import os
import requests
import json


class DraftedPlayer(QtGui.QWidget):
    def __init__(self, player, parent):
        super(DraftedPlayer, self).__init__(parent)
        self.data = parent.data
        self.player = player

        self.allQHBoxLayout = QtGui.QHBoxLayout()

        self.pick_num_label = QtGui.QLabel(str(self.player.overall_draft_num))
        self.pick_num_label.setFont(Globals.medium_bold_font)
        self.round_num_label = QtGui.QLabel(str(self.player.draft_round+1))
        self.round_num_label.setFont(Globals.medium_bold_font)
        self.team_label = QtGui.QLabel(self.data.teams[self.player.team])
        self.team_label.setFont(Globals.medium_font)
        self.player_label = QtGui.QLabel(self.player.name)
        self.player_label.setFont(Globals.medium_font)
        self.position_label = QtGui.QLabel(self.player.pos)
        self.position_label.setFont(Globals.medium_font)

        player_pixmap = QtGui.QPixmap()
        player_pixmap.loadFromData(self.player.getPlayerImg())
        self.player_img_label = QtGui.QLabel()
        self.player_img_label.setPixmap(player_pixmap)

        team_pixmap = QtGui.QPixmap(player.getTeamImg())
        #team_pixmap.loadFromData(self.player.team_img)
        self.team_img_label = QtGui.QLabel()
        self.team_img_label.setPixmap(team_pixmap)

        self.allQHBoxLayout.addWidget(self.pick_num_label, 1)
        self.allQHBoxLayout.addWidget(self.round_num_label, 1)
        self.allQHBoxLayout.addWidget(self.player_img_label, 5)
        self.allQHBoxLayout.addWidget(self.team_img_label, 5)
        self.allQHBoxLayout.addWidget(self.team_label, 10)
        self.allQHBoxLayout.addWidget(self.player_label, 10)
        self.allQHBoxLayout.addWidget(self.position_label, 0)

        self.setLayout(self.allQHBoxLayout)

    def updateLabels(self):
        self.team_label.setText(self.data.teams[self.player.team])
        self.player_label.setText(self.data.teams_players[self.player.team][self.player.draft_round].name)
        self.position_label.setText(self.data.teams_players[self.player.team][self.player.draft_round].pos)

        player_pixmap = QtGui.QPixmap()
        player_pixmap.loadFromData(self.player.getPlayerImg())
        self.player_img_label.setPixmap(player_pixmap)

        team_pixmap = QtGui.QPixmap(self.player.getTeamImg())
        #team_pixmap.loadFromData(self.player.team_img)
        self.team_img_label.setPixmap(team_pixmap)


class DraftTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.data = parent.pool_data

        # thread variables
        self.stopped = Event()
        self.thread = self.findPlayersThread(self.stopped, self.data, 1)
        self.thread.thread_finished.connect(self.setPlayersFound)
        self.thread.start()

        main_layout = QtGui.QVBoxLayout()

        # Draft History
        self.list = QtGui.QListWidget()

        # Next Pick
        self.round_num = 0
        self.round_pick = 0
        self.picking_team = self.getPickingTeam()
        self.round_num_label = QtGui.QLabel()
        self.picking_team_label = QtGui.QLabel()
        #self.player_input = QtGui.QLineEdit()
        self.player_input = QtGui.QComboBox()
        self.loading_players = False

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

        self.draft_player_btn = QtGui.QPushButton("Draft Player")
        self.draft_player_btn.clicked.connect(self.draftPlayer)

        #self.player_input.textChanged.connect(self.inputChanged)
        self.player_input.editTextChanged.connect(self.inputChanged)
        self.player_input.setEditable(True)
        self.player_input.setCompleter(None)

        grid.addWidget(team_label, 1, 0)
        grid.addWidget(self.picking_team_label, 1, 1)
        grid.addWidget(round_label, 1, 2)
        grid.addWidget(self.round_num_label, 1, 3)

        grid.addWidget(player_label, 2, 0)
        grid.addWidget(self.player_input, 2, 1, 1, 3)

        grid.addWidget(self.draft_player_btn, 3, 0, 3, 4)
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
        if self.player_input.currentIndex() == -1:
            self.parent.errorMessage(self.player_input.currentText() + " is not in NHL database")
            return
        player = self.player_input.itemData(self.player_input.currentIndex(), Globals.player_data_role)
        player.overall_draft_num = self.getOverallPickNum()
        player.draft_round = self.round_num
        player.team = self.picking_team
        print player.id
        print player.nhl_team
        self.data.draftPlayer(player)

    def updatePlayerDrafted(self, player):
        drafted_player = DraftedPlayer(player, self)
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
            if drafted_player.player.team == team_num:
                drafted_player.updateLabels()

    def playerUpdate(self, team_num, player_index):
        # player_index represents the number of rounds
        if player_index % 2 == 0:
            list_index = player_index*len(self.data.teams) + self.data.draft_order.index(team_num)
        else:
            list_index = player_index*len(self.data.teams) + len(self.data.teams) - (self.data.draft_order.index(team_num) + 1)

        drafted_player = self.list.itemWidget(self.list.item(list_index))
        drafted_player.updateLabels()

    def dataImported(self):
        # Import all the players in order
        if len(self.data.teams_players) == 0:
            return ""
        draft_order = self.data.draft_order[:]
        teams_players_string = ""
        # One extra iteration encase not all teams have the same amount of players drafted
        max_rounds = len(self.data.teams_players[self.data.teams_players.keys()[0]]) + 1

        for round in range(0, max_rounds):
            for team_num in draft_order:
                assert (team_num in self.data.teams_players.keys()), "Draft order has a non-existent team"
                try:
                    self.updatePlayerDrafted(self.data.teams_players[team_num][round])

                except IndexError:
                    # Ignore if on last round or 2nd last round
                    assert (round >= max_rounds-2), "Error when importing teams_players data to draft tab, " + str(team_num) + ":" + str(round)

            # Reverse the order due to snake draft
            draft_order.reverse()


    def inputChanged(self):
        if len(self.player_input.currentText()) < 4:
            self.player_input.clear()
            return
        elif self.loading_players:
            return
        else:
            # Stop previous name search
            self.stopped.set()
            # Start new name search
            self.thread.setName(self.player_input.currentText())



    class findPlayersThread(QtCore.QThread):

        thread_finished = QtCore.Signal(object)

        def __init__(self, event, data, delay):
            QtCore.QThread.__init__(self)
            self.stopped = event
            self.data = data
            self.delay = delay
            self.name = None
            self.newRun = False

        def run(self):
            while True:
                if not self.stopped.wait(self.delay):
                    if self.newRun:
                        players = self.data.getPlayerList(self.name)
                        self.thread_finished.emit(players)
                        self.newRun = False
                else:
                    # Stopped was set
                    self.stopped.clear()


        def setName(self, name):
            self.name = name
            self.newRun = True

    def setPlayersFound(self, players):
        self.loading_players = True
        player_input_text = self.player_input.currentText()
        self.player_input.clear()
        model = QtGui.QStandardItemModel()
        view = QtGui.QTableView()
        for player in players:
            nameItem = QtGui.QStandardItem(player.name)
            nameItem.setData(player, QtCore.Qt.UserRole + 1)
            posItem = QtGui.QStandardItem(player.pos)
            teamItem = QtGui.QStandardItem(player.nhl_team)
            model.appendRow([nameItem, posItem, teamItem])
        self.player_input.setModel(model)
        self.player_input.setView(view)
        self.player_input.setEditText(player_input_text)
        if len(players) != 1 or player_input_text != players[0].name:
            # If we match the players name exactly don't bother showing popup
            # This occurs when we select a player from the drop down
            self.player_input.showPopup()
        self.loading_players = False

