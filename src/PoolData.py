import sys
import os
from FileParser import FileParser
import requests
from bs4 import BeautifulSoup

class PoolData(object):
    def __init__(self, parent):

        self.parent = parent

        self.teams = {  0: "Team A",
                        1: "Team B",
                        2: "Team C"}

        self.draft_order = [2, 0, 1]

        self.teams_players = {}
        for team_num in self.teams.keys():
            self.teams_players[team_num] = []

        self.num_forwards = 12
        self.num_defense = 6
        self.num_goalies = 2
        self.num_rounds = 20
        self.import_path = ""
        self.export_path = ""

    def setRounds(self, rounds):
        if not self.draftHasStarted():
            self.num_rounds = rounds
            self.parent.totalsChanged()
            self.exportData()

    def setForwards(self, forwards):
        if not self.draftHasStarted():
            self.num_forwards = forwards
            self.parent.totalsChanged()
            self.exportData()

    def setDefense(self, defense):
        if not self.draftHasStarted():
            self.num_defense = defense
            self.parent.totalsChanged()
            self.exportData()

    def setGoalies(self, goalies):
        if not self.draftHasStarted():
            self.num_goalies = goalies
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
            FileParser.exportData(self.export_path, self.teams, self.draft_order, self.num_rounds, self.num_forwards, self.num_defense, self.num_goalies, self.teams_players)

    def storePlayer(self, player):
        if self.export_path:
            FileParser.appendPlayer(self.export_path, player)

    def checkPosition(self, player):
        # This function is dependent on the html structure of the nhl.com search page

        player_name = player.name.replace(" ", "+")
        player_search_url = "http://www.nhl.com/ice/search.htm?tab=all&q=" + player_name
        r = requests.get(player_search_url)
        soup = BeautifulSoup(r.text)
        try:
            pos = soup.find_all("ul", "results")[0].li.div.find_all("div")[1].find_all("span")[1].getText()
        except (IndexError, AttributeError):
            # Player not found (trust the position provided)
            return True

        if pos == "Center" or pos == "Left Wing" or pos == "Right Wing":
            player_pos = 'F'
        elif pos == "Defenseman":
            player_pos = 'D'
        elif pos == "Goalie":
            player_pos = 'G'
        else:
            # Player not a standard position
            return False

        return player.pos == player_pos

    def getPlayerImgs(self, player):
        # This function is dependent on the html structure of the nhl.com search page

        player_name = player.name.replace(" ", "+")
        player_search_url = "http://www.nhl.com/ice/search.htm?tab=all&q=" + player_name
        r = requests.get(player_search_url)
        soup = BeautifulSoup(r.text)
        try:
            player_img_url = soup.find_all("ul", "results")[0].li.div.div.a.img.get("src")
            player_img_data = requests.get(player_img_url).content
        except (IndexError, AttributeError):
            # Could not find player image give default one
            player_img_data = requests.get("http://3.cdn.nhle.com/photos/mugs/default.jpg").content

        try:
            team_img_url = soup.find_all("ul", "results")[0].li.div.find_all("div")[1].a.img.get("src")
            team_img_data = requests.get(team_img_url).content
        except (IndexError, AttributeError):
            # Could not find team image give default one
            team_img_data = requests.get("http://www1.nhl.com/images/logos/medium.png").content

        return player_img_data, team_img_data

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
                if player.name == drafted_player.name:
                    return True

        return False

    def canDraftPlayer(self, team_num, player):
        # check if team can draft that player position
        remaining_picks = 0
        if player.pos == 'F':
            (remaining_picks, _, _) = self.getRemainingPlayers(team_num)
        if player.pos == "D":
            (_, remaining_picks, _) = self.getRemainingPlayers(team_num)
        if player.pos == "G":
            (_, _, remaining_picks) = self.getRemainingPlayers(team_num)

        if remaining_picks <= 0:
            return False

        # check if a team has already drafted that player
        if self.isPlayerDrafted(player):
            return False

        # check if total rounds exhausted
        if len(self.teams_players[team_num]) >= self.num_rounds:
            return False

        # Check if the position is recorded correctly
        if not self.checkPosition(player):
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
        max_num = 0
        for team in self.teams.keys():
            if team > max_num:
                max_num = team

        return max_num+1

    def renamePlayer(self, team_num, player_index, new_name):
        player_list = self.teams_players[team_num]
        player = player_list[player_index]

        player.name = new_name

        self.parent.renamePlayer(team_num, player_index)
        self.exportData()

    def repositionPlayer(self, team_num, player_index, new_pos):
        player_list = self.teams_players[team_num]
        player = player_list[player_index]

        player.pos = new_pos

        self.parent.repositionPlayer(team_num, player_index)
        self.exportData()
