import sys
import os
from FileParser import FileParser
import requests
from bs4 import BeautifulSoup

class PoolData(object):
    def __init__(self, parent):

        self.parent = parent

        self.teams = {}

        self.draft_order = []

        self.teams_players = {}
        for team_num in self.teams.keys():
            self.teams_players[team_num] = []

        self.num_forwards = 12
        self.num_defense = 6
        self.num_goalies = 2
        self.num_rounds = 20
        self.import_path = ""
        self.export_path = ""

    def __setRounds(self):
        self.num_rounds = self.num_forwards + self.num_defense + self.num_goalies

    def setForwards(self, forwards):
        if not self.draftHasStarted():
            self.num_forwards = forwards
            self.__setRounds()
            self.parent.totalsChanged()
            self.exportData()

    def setDefense(self, defense):
        if not self.draftHasStarted():
            self.num_defense = defense
            self.__setRounds()
            self.parent.totalsChanged()
            self.exportData()

    def setGoalies(self, goalies):
        if not self.draftHasStarted():
            self.num_goalies = goalies
            self.__setRounds()
            self.parent.totalsChanged()
            self.exportData()

    def setImportPath(self, file_path):
        if not self.draftHasStarted():
            self.import_path = file_path
            # Write to the file you used to import as the draft continues
            self.export_path = file_path
            self.importData()

    def setExportPath(self, file_path):
        self.export_path = file_path
        self.exportData()

    def importData(self):
        self.teams, self.draft_order, self.num_rounds, self.num_forwards, self.num_defense, self.num_goalies, self.teams_players = FileParser.importData(self.import_path)
        self.parent.dataImported()
        if self.draftHasStarted():
            self.parent.draftJustStarted()

    def exportData(self):
        if self.export_path:
            FileParser.exportData(self.export_path, self.teams, self.draft_order, self.num_forwards, self.num_defense, self.num_goalies, self.teams_players)

    def generatePrettyOutput(self, filename):
        FileParser.generatePrettyOutput(filename, self.teams, self.draft_order, self.teams_players)

    def storePlayer(self, player):
        if self.export_path:
            FileParser.appendPlayer(self.export_path, player)

    def getRemainingPlayers(self, team_num):
        team_players = self.teams_players[team_num]
        forwards_remaining = self.num_forwards
        defense_remaining = self.num_defense
        goalies_remaining = self.num_goalies

        for player in team_players:
            if player.pos == "F":
                forwards_remaining -= 1
            if player.pos == "D":
                defense_remaining -= 1
            if player.pos == "G":
                goalies_remaining -= 1

        return forwards_remaining, defense_remaining, goalies_remaining

    def isPlayerDrafted(self, player):
        for _, drafted_players in self.teams_players.iteritems():
            for drafted_player in drafted_players:
                if player.name == drafted_player.name and player.pos == drafted_player.pos:
                    return True

        return False

    def canDraftPlayer(self, team_num, player):
        # check that the team exists
        if team_num not in self.teams.keys():
            self.parent.errorMessage("team doesn't exist")
            return False

        # check if total rounds exhausted
        if len(self.teams_players[team_num]) >= self.num_rounds:
            self.parent.errorMessage("Total rounds exhausted")
            return False

        # check if team can draft that player position
        remaining_picks = 0
        error_message = ""
        if player.pos == 'F':
            (remaining_picks, _, _) = self.getRemainingPlayers(team_num)
            error_message = self.teams[player.team] + " has no more forwards to pick"
        if player.pos == "D":
            (_, remaining_picks, _) = self.getRemainingPlayers(team_num)
            error_message = self.teams[player.team] + " has no more defense to pick"
        if player.pos == "G":
            (_, _, remaining_picks) = self.getRemainingPlayers(team_num)
            error_message = self.teams[player.team] + " has no more goalies to pick"

        if remaining_picks <= 0:
            self.parent.errorMessage(error_message)
            return False

        # check if a team has already drafted that player
        if self.isPlayerDrafted(player):
            self.parent.errorMessage(player.name + ", " + player.pos + " already drafted")
            return False

        # Check if the position is recorded correctly
        success, errMsg = player.checkPosition()
        if not success:
            self.parent.errorMessage(errMsg)
            return False

        return True

    def draftHasStarted(self):
        for team_num, team_players in self.teams_players.items():
            if len(team_players) > 0:
                return True

        return False

    def draftJustStarted(self):
        num_players_drafted = 0
        for team_num, team_players in self.teams_players.items():
            num_players_drafted += len(team_players)

        if num_players_drafted == 1:
            return True
        else:
            return False

    def draftPlayer(self, player):
        if self.canDraftPlayer(player.team, player):
            self.teams_players[player.team].append(player)
            self.parent.playerDrafted(player)
            self.parent.successMessage(self.teams[player.team] + " drafted " + player.name + ", " + player.pos)

            if self.draftJustStarted():
                self.parent.draftJustStarted()
                self.exportData()
            else:
                self.storePlayer(player)

    def renameTeam(self, team_num, new_name):
        self.teams[team_num] = new_name
        self.parent.renameTeam(team_num)
        self.exportData()

    def reorderTeam(self, team_num, new_position):
        # Cannot reorder the teams after the draft has started
        if not self.draftHasStarted():
            self.draft_order.remove(team_num)
            self.draft_order.insert(new_position, team_num)
            self.parent.draftReordered()
            self.exportData()

    def createNewTeam(self, team_name):
        # Cannot add a team after the draft has started
        if not self.draftHasStarted():
            team_num = self.getNewTeamNum()
            self.teams[team_num] = team_name
            self.teams_players[team_num] = []
            self.draft_order.append(team_num)

            self.parent.addTeam(team_num)
            self.exportData()

    def removeTeam(self, team_num):
        # Cannot remove a team while the draft has started
        if not self.draftHasStarted():
            del self.teams[team_num]
            del self.teams_players[team_num]
            self.draft_order.remove(team_num)

            self.parent.removeTeam(team_num)
            self.exportData()

    def getNewTeamNum(self):
        max_num = -1
        for team in self.teams.keys():
            if team > max_num:
                max_num = team

        return max_num+1

    def renamePlayer(self, team_num, player_index, new_name):
        player_list = self.teams_players[team_num]
        player = player_list[player_index]

        player.name = new_name
        player.updatePlayerImgs()

        self.parent.renamePlayer(team_num, player_index)
        self.exportData()

    def repositionPlayer(self, team_num, player_index, new_pos):
        player_list = self.teams_players[team_num]
        player = player_list[player_index]

        player.pos = new_pos

        self.parent.repositionPlayer(team_num, player_index)
        self.exportData()
