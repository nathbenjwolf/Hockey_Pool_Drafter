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
        self.parent = parent
        self.data = parent.pool_data

        main_layout = QtGui.QVBoxLayout()

        # Team list
        self.team_list = QtGui.QListWidget()
        self.team_list.setMinimumSize(400,200)
        self.team_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.team_list.setStyleSheet("QListView { alternate-background-color: lightgrey; }")
        self.team_list.setAlternatingRowColors(True)
        self.team_list.itemSelectionChanged.connect(self.teamSelected)
        self.populateTeamList()

        # Team Options
        self.selected_team = -1
        self.selected_team_label = QtGui.QLabel()
        self.team_options_view = self.teamOptionsView()

        main_layout.addWidget(self.team_list)
        main_layout.addWidget(self.team_options_view)
        self.setLayout(main_layout)

    def populateTeamList(self):
        for team_num in self.data.draft_order:
            self.createTeamEntry(team_num)

    def createTeamEntry(self, team_num):
        team = TeamEntry(team_num, self)
        myQListWidgetItem = QtGui.QListWidgetItem(self.team_list)
        myQListWidgetItem.setSizeHint(team.sizeHint())
        self.team_list.addItem(myQListWidgetItem)
        self.team_list.setItemWidget(myQListWidgetItem, team)

    def teamOptionsView(self):
        picking_group_box = QtGui.QGroupBox()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        team_label = QtGui.QLabel(self.tr("Team:"))
        self.updateSelectedTeam()

        self.inspect_btn = QtGui.QPushButton("Inspect")
        self.inspect_btn.clicked.connect(self.inspect)

        self.rename_btn = QtGui.QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename)

        self.reorder_btn = QtGui.QPushButton("Reorder")
        self.reorder_btn.clicked.connect(self.reorder)

        self.add_btn = QtGui.QPushButton("Add")
        self.add_btn.clicked.connect(self.add)

        self.remove_btn = QtGui.QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove)
        self.setButtonStatus()

        grid.addWidget(team_label, 1, 0)
        grid.addWidget(self.selected_team_label, 1, 1)

        grid.addWidget(self.inspect_btn, 2, 0)
        grid.addWidget(self.rename_btn, 2, 1)
        grid.addWidget(self.reorder_btn, 2, 2)
        grid.addWidget(self.add_btn, 2, 3)
        grid.addWidget(self.remove_btn, 2, 4)

        picking_group_box.setLayout(grid)

        return picking_group_box

    def teamSelected(self):
        self.selected_team = self.team_list.itemWidget(self.team_list.currentItem()).team_num
        self.updateSelectedTeam()
        self.setButtonStatus()

    def updateSelectedTeam(self):
        if self.selected_team == -1:
            self.selected_team_label.setText("(Select a Team)")
        else:
            # Called due to clear() changing the selection?
            try:
                self.selected_team_label.setText(self.data.teams[self.selected_team])
            except KeyError:
                self.selected_team = -1
                self.selected_team_label.setText("(Select a Team)")

    def setButtonStatus(self):
        # Default them to enabled
        self.inspect_btn.setEnabled(True)
        self.rename_btn.setEnabled(True)
        self.reorder_btn.setEnabled(True)
        self.add_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)

        if self.selected_team == -1:
            # No team selected
            self.inspect_btn.setEnabled(False)
            self.rename_btn.setEnabled(False)
            self.reorder_btn.setEnabled(False)
            self.remove_btn.setEnabled(False)

        if self.data.draftHasStarted():
            # Draft has started (can't manipulate certain team aspects)
            self.reorder_btn.setEnabled(False)
            self.add_btn.setEnabled(False)
            self.remove_btn.setEnabled(False)

    def inspect(self):
        print("inspect")

    def rename(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your teams new name:')
        if ok:
            self.data.renameTeam(self.selected_team, text.__str__())
            self.updateTeam(self.selected_team)
            self.updateSelectedTeam()
            self.parent.renameTeam(self.selected_team)

    def reorder(self):
        new_position, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog', 'Enter new drafting position for team: (starting at 1)',
                                             minValue=1, maxValue=len(self.data.teams))
        if ok:
            self.data.reorderTeam(self.selected_team, new_position-1)
            # Repopulate the list (just easier)
            self.team_list.clear()
            self.populateTeamList()
            self.parent.draftReordered()

    def add(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your teams name:')
        if ok:
            team_num = self.data.createNewTeam(text.__str__())
            if team_num != -1:
                self.createTeamEntry(team_num)
            else:
                # Something went wrong
                pass

    def remove(self):

        self.data.removeTeam(self.selected_team)
        # Repopulate the list (just easier)
        self.team_list.clear()
        self.populateTeamList()
        self.parent.draftReordered()

    def updateTeam(self, team_num):
        draft_order_num = self.data.draft_order.index(team_num)
        team = self.team_list.itemWidget(self.team_list.item(draft_order_num))
        team.updateWidgets()

        if self.data.draftJustStarted():
            # May have to update buttons
            self.setButtonStatus()