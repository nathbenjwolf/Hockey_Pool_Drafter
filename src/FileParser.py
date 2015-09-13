__author__ = 'Nathan'

from Player import Player

class FileParser(object):

    @staticmethod
    def importData(filename):
        f = open(filename, 'r')

        with f:

            # Teams
            teams = FileParser.__unmarshalTeams(f.readline())

            # Draft Order
            draft_order = FileParser.__unmarshalDraftOrder(f.readline())

            # Config Totals
            rounds, forwards, defense, goalies = FileParser.__unmarshalTotals(f.readline())

            # Team Players
            teams_players = FileParser.__unmarshalTeamsPlayers(f.readline(), teams.keys())

        return teams, draft_order, rounds, forwards, defense, goalies, teams_players

    @staticmethod
    def exportData(filename, teams, draft_order, forwards, defense, goalies, teams_players):
        f = open(filename, 'w')

        with f:

            # Teams
            teams_string = FileParser.__marshalTeams(teams)
            f.write(teams_string)
            f.write('\n')

            # Draft Order
            draft_order_string = FileParser.__marshalDraftOrder(draft_order)
            f.write(draft_order_string)
            f.write('\n')

            # Config Totals
            totals_string = FileParser.__marshalTotals(forwards, defense, goalies)
            f.write(totals_string)
            f.write('\n')

            # Teams Players
            teams_players_string = FileParser.__marshalTeamsPlayers(teams_players, draft_order)
            f.write(teams_players_string)

    @staticmethod
    def appendPlayer(filename, player):
        f = open(filename, 'a')

        with f:

            player_string = FileParser.__marshalPlayer(player)
            f.write("," + player_string)

    @staticmethod
    def __unmarshalTeams(line):
        teams = {}
        for token in line.split(','):
            team_tuple = token.split(':')
            team_num = int(team_tuple[0])
            team_name = team_tuple[1].strip('\n')
            teams[team_num] = team_name

        return teams

    @staticmethod
    def __marshalTeams(teams):
        teams_string = ""
        for team_num, team_name in teams.items():
            teams_string = teams_string + str(team_num) + ":" + team_name + ","

        return teams_string.strip(",")

    @staticmethod
    def __unmarshalDraftOrder(line):
        draft_order = []
        for token in line.split(','):
            draft_order.append(int(token))

        return draft_order

    @staticmethod
    def __marshalDraftOrder(draft_order):
        draft_order_string = ""
        for team_num in draft_order:
            draft_order_string = draft_order_string + str(team_num) + ","

        return draft_order_string.strip(",")

    @staticmethod
    def __unmarshalTotals(line):
        tokens = line.split(',')
        forwards = int(tokens[0])
        defense = int(tokens[1])
        goalies = int(tokens[2])
        rounds = forwards + defense + goalies

        return rounds, forwards, defense, goalies

    @staticmethod
    def __marshalTotals(forwards, defense, goalies):
        totals_string = str(forwards) + ","
        totals_string = totals_string + str(defense) + ","
        totals_string = totals_string + str(goalies)

        return totals_string

    @staticmethod
    def __unmarshalTeamsPlayers(line, team_nums):
        teams_players = {}
        for team_num in team_nums:
            teams_players[team_num] = []

        if line:
            for player_string in line.split(','):
                player = FileParser.__unmarshalPlayer(player_string)
                teams_players[player.team].append(player)

        return teams_players

    @staticmethod
    def __marshalTeamsPlayers(teams_players, draft_order_original):
        if len(teams_players) == 0:
            return ""
        draft_order = draft_order_original[:]
        teams_players_string = ""
        # One extra iteration encase not all teams have the same amount of players drafted
        max_rounds = len(teams_players[teams_players.keys()[0]]) + 1

        for round in range(0, max_rounds):
            for team_num in draft_order:
                assert (team_num in teams_players.keys()), "Draft order has a non-existent team"
                try:
                    player_string = FileParser.__marshalPlayer(teams_players[team_num][round])
                    teams_players_string = teams_players_string + player_string + ","

                except IndexError:
                    # Ignore if on last round or 2nd last round
                    assert (round >= max_rounds-2), "Error with teams_players data, " + str(team_num) + ":" + str(round)

            # Reverse the order due to snake draft
            draft_order.reverse()

        return teams_players_string.strip(",")

    @staticmethod
    def __unmarshalPlayer(line):
        t = line.split('.')
        return Player(int(t[0]), int(t[1]), int(t[2]), t[3], t[4])

    @staticmethod
    def __marshalPlayer(player):
        player_string = str(player.overall_draft_num) + "."
        player_string = player_string + str(player.draft_round) + "."
        player_string = player_string + str(player.team) + "."
        player_string = player_string + player.name + "."
        player_string = player_string + player.pos

        return player_string