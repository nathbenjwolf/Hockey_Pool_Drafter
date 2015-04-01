import sys


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

        if(remaining_picks <= 0):
            return False

        # check if a team has already drafted that player
        if(self.isPlayerDrafted(player)):
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


    def renameTeam(self, team_num, new_name):
        self.teams[team_num] = new_name
        self.parent.renameTeam(team_num)

    def reorderTeam(self, team_num, new_position):
        # Cannot reorder the teams after the draft has started
        if not self.draftHasStarted():
            self.draft_order.remove(team_num)
            self.draft_order.insert(new_position, team_num)
            self.parent.draftReordered()

    def createNewTeam(self, team_name):
        # Cannot add a team after the draft has started
        if not self.draftHasStarted():
            team_num = self.getNewTeamNum()
            self.teams[team_num] = team_name
            self.teams_players[team_num] = []
            self.draft_order.append(team_num)

            self.parent.addTeam(team_num)

    def removeTeam(self, team_num):
        # Cannot remove a team while the draft has started
        if not self.draftHasStarted():
            del self.teams[team_num]
            del self.teams_players[team_num]
            self.draft_order.remove(team_num)

            self.parent.removeTeam(team_num)

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