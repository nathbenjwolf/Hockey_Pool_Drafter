#!/usr/bin/python

import sys
from PySide import QtGui


class TeamEntry(QtGui.QWidget):
    def __init__(self, team_num, parent):
        super(TeamEntry, self).__init__(parent)
        self.allQHBoxLayout = QtGui.QHBoxLayout()
        self.team_num = team_num
        self.data = parent.data

        self.draft_order_label = QtGui.QLabel()
        self.team_name_label = QtGui.QLabel()
        self.forwards_label = QtGui.QLabel()
        self.defense_label = QtGui.QLabel()
        self.goalies_label = QtGui.QLabel()
        self.updateWidgets()

        self.allQHBoxLayout.addWidget(self.draft_order_label, 1)
        self.allQHBoxLayout.addWidget(self.team_name_label, 10)
        self.allQHBoxLayout.addWidget(self.forwards_label, 2)
        self.allQHBoxLayout.addWidget(self.defense_label, 2)
        self.allQHBoxLayout.addWidget(self.goalies_label, 2)

        self.setLayout(self.allQHBoxLayout)

    def updateWidgets(self):
        (f_remaining, d_remaining, g_remaining) = self.data.getRemainingPlayers(self.team_num)
        self.draft_order_label.setText(str(self.data.draft_order.index(self.team_num)+1))
        self.team_name_label.setText(self.data.teams[self.team_num])
        self.forwards_label.setText("F: " + str(f_remaining))
        self.defense_label.setText("D: " + str(d_remaining))
        self.goalies_label.setText("G: " + str(g_remaining))

class TeamTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.data = parent.pool_data

        main_layout = QtGui.QVBoxLayout()

        # Team list
        self.list = QtGui.QListWidget()
        self.list.setMinimumSize(400,200)
        self.list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.list.setStyleSheet("QListView { alternate-background-color: lightgrey; }")
        self.list.setAlternatingRowColors(True)
        self.populateTeamList()

        main_layout.addWidget(self.list)
        self.setLayout(main_layout)

    def populateTeamList(self):
        for team_num in self.data.draft_order:
            team = TeamEntry(team_num, self)
            myQListWidgetItem = QtGui.QListWidgetItem(self.list)
            myQListWidgetItem.setSizeHint(team.sizeHint())
            self.list.addItem(myQListWidgetItem)
            self.list.setItemWidget(myQListWidgetItem, team)

    def updateTeam(self, team_num):
        draft_order_num = self.data.draft_order.index(team_num)
        team = self.list.itemWidget(self.list.item(draft_order_num))
        team.updateWidgets()