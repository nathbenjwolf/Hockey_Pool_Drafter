import sys


class PoolData(object):
    def __init__(self):

        self.teams = {  1: "Team A",
                        2: "Team B",
                        3: "Team C"}

        self.draft_order = [3,2,1]

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