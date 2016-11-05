from PySide import QtGui
import unittest
import sys
from PySide.QtCore import Qt
from PySide.QtTest import QTest
import time
from PlayerData import PlayerData
sys.path.insert(0, '../')
from MainUI import MainUI


class TestOverallProduct(unittest.TestCase):

    def startApp(self):
        QtGui.QApplication(sys.argv)
        app = MainUI()
        app.open()
        return app

    def configureForDraft(self, app, config):
        # Add teams
        for _, team in config.teams.iteritems():
            app.pool_data.createNewTeam(team)
            self.assertTrue(app.pool_data.teams[len(app.pool_data.teams)-1] == team)

        # Reorder teams
        for team_num in config.draft_order:
            app.pool_data.reorderTeam(team_num, config.draft_order.index(team_num))
            self.assertTrue(app.pool_data.draft_order[config.draft_order.index(team_num)] == team_num)

        # Configure limits
        app.pool_data.setForwards(config.num_forwards)
        self.assertTrue(app.pool_data.num_forwards == config.num_forwards)

        app.pool_data.setDefense(config.num_defense)
        self.assertTrue(app.pool_data.num_defense == config.num_defense)

        app.pool_data.setGoalies(config.num_goalies)
        self.assertTrue(app.pool_data.num_goalies == config.num_goalies)

    def draftPlayers(self, app, players):
        for player in players:
            QTest.keyClicks(app.draft_tab.player_input, player.name, 0, 10)
            self.assertEquals(app.draft_tab.player_input.currentText().__str__(), player.name)
            QTest.mouseClick(app.draft_tab.draft_player_btn, Qt.LeftButton)

    def confirmPlayersDrafted(self, app, players):
        for player in players:
            self.assertEquals(player, app.pool_data.teams_players[player.team][player.draft_round])

    def testDraft(self):
        app = self.startApp()
        players = PlayerData.getPlayerData()
        config = PlayerData.getAppConfig()
        self.configureForDraft(app, config)
        self.draftPlayers(app, players)
        self.confirmPlayersDrafted(app, players)

if __name__ == '__main__':
    unittest.main()