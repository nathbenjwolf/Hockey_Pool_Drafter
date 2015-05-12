#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from PySide import QtCore
from Globals import Globals
import DraftTab
import TeamTab
import ConfigTab
import PoolData


class MainUI(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.pool_data = PoolData.PoolData(self)

        self.draft_tab = DraftTab.DraftTab(parent=self)
        self.team_tab = TeamTab.TeamTab(parent=self)
        self.config_tab = ConfigTab.ConfigTab(parent=self)

        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.addTab(self.draft_tab, self.tr("Draft"))
        self.tab_widget.addTab(self.team_tab, self.tr("Team"))
        self.tab_widget.addTab(self.config_tab, self.tr("Config"))
        self.tab_widget.setFont(Globals.medium_font)

        self.tab_widget.currentChanged.connect(self.tabChanged)

        okButton = QtGui.QPushButton(self.tr("OK"))
        cancelButton = QtGui.QPushButton(self.tr("Cancel"))

        self.connect(okButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tab_widget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Fantasy Hockey Pool"))

        self.resize(Globals.window_width, Globals.window_height)

    def tabChanged(self):
        if self.tab_widget.currentIndex() != 1:
            # Is not the team tab (make sure to go back from the team specific page)
            self.team_tab.returnToTeamPage()

    def totalsChanged(self):
        # Team tab
        self.team_tab.totalsChanged()

    def draftJustStarted(self):
        # Team tab
        self.team_tab.setButtonStatus()

        # Config tab
        self.config_tab.draftStarted()

    def playerDrafted(self, player):
        # Draft tab
        self.draft_tab.updatePlayerDrafted(player)

        # Team tab
        self.team_tab.updateTeam(player.team)

    def renameTeam(self, team_num):
        # Draft tab
        self.draft_tab.renameTeam(team_num)

        # Team tab
        self.team_tab.updateTeam(team_num)

    def draftReordered(self):
        # Draft tab
        self.draft_tab.picking_team = self.draft_tab.getPickingTeam()
        self.draft_tab.updatePickView()

        # Team Tab: Repopulate the list (just easier)
        self.team_tab.team_list.clear()
        self.team_tab.populateTeamList()

    def addTeam(self, team_num):
        # Draft tab
        self.draft_tab.picking_team = self.draft_tab.getPickingTeam()
        self.draft_tab.updatePickView()

        # Team tab
        self.team_tab.createTeamEntry(team_num)

    def removeTeam(self, team_num):
        # Draft tab
        self.draft_tab.picking_team = self.draft_tab.getPickingTeam()
        self.draft_tab.updatePickView()

        # Team tab: Repopulate the list (just easier)
        self.team_tab.team_list.clear()
        self.team_tab.populateTeamList()

    def renamePlayer(self, team_num, player_index):
        # Draft tab
        self.draft_tab.playerUpdate(team_num, player_index)

    def repositionPlayer(self, team_num, player_index):
        # Draft tab
        self.draft_tab.playerUpdate(team_num, player_index)

        # Team tab
        self.team_tab.updateTeam(team_num)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    tab_dialog = MainUI()

    sys.exit(tab_dialog.exec_())
