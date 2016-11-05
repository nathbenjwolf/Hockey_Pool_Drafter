import sys
from TestConfig import TestConfig
sys.path.insert(0, '../')
from Player import Player

class PlayerData(object):
    @staticmethod
    def getPlayerData():
        playerList = []
        # None values we don't check in the __eq__ for player because they change between years
        # This list needs to be updated if players retire or are inactive though
        playerList.append(Player(None, None, "Sidney Crosby", "F", None, 1, 0, 1))
        playerList.append(Player(None, None, "Alex Ovechkin", "F", None, 2, 0, 2))
        playerList.append(Player(None, None, "Jason Spezza", "F", None, 3, 0, 0))
        playerList.append(Player(None, None, "Nicklas Backstrom", "F", None, 4, 1, 0))
        playerList.append(Player(None, None, "Daniel Sedin", "F", None, 5, 1, 2))
        playerList.append(Player(None, None, "Henrik Sedin", "F", None, 6, 1, 1))
        playerList.append(Player(None, None, "Jamie Benn", "F", None, 7, 2, 1))
        playerList.append(Player(None, None, "John Tavares", "F", None, 8, 2, 2))
        playerList.append(Player(None, None, "Claude Giroux", "F", None, 9, 2, 0))
        playerList.append(Player(None, None, "Jakub Voracek", "F", None, 10, 3, 0))
        playerList.append(Player(None, None, "Nick Foligno", "F", None, 11, 3, 2))
        playerList.append(Player(None, None, "Tyler Johnson", "F", None, 12, 3, 1))
        playerList.append(Player(None, None, "Steven Stamkos", "F", None, 13, 4, 1))
        playerList.append(Player(None, None, "Ryan Getzlaf", "F", None, 14, 4, 2))
        playerList.append(Player(None, None, "Corey Perry", "F", None, 15, 4, 0))
        playerList.append(Player(None, None, "Erik Karlsson", "D", None, 16, 5, 0))
        playerList.append(Player(None, None, "P.K. Subban", "D", None, 17, 5, 2))
        playerList.append(Player(None, None, "Alexander Edler", "D", None, 18, 5, 1))
        playerList.append(Player(None, None, "Mark Giordano", "D", None, 19, 6, 1))
        playerList.append(Player(None, None, "Brent Burns", "D", None, 20, 6, 2))
        playerList.append(Player(None, None, "Dustin Byfuglien", "D", None, 21, 6, 0))
        playerList.append(Player(None, None, "Toby Enstrom", "D", None, 22, 7, 0))
        playerList.append(Player(None, None, "Kevin Bieksa", "D", None, 23, 7, 2))
        playerList.append(Player(None, None, "Kris Letang", "D", None, 24, 7, 1))
        playerList.append(Player(None, None, "Tuukka Rask", "G", None, 25, 8, 1))
        playerList.append(Player(None, None, "Jacob Markstrom", "G", None, 26, 8, 2))
        playerList.append(Player(None, None, "Ryan Miller", "G", None, 27, 8, 0))
        playerList.append(Player(None, None, "Henrik Lundqvist", "G", None, 28, 9, 0))
        playerList.append(Player(None, None, "Roberto Luongo", "G", None, 29, 9, 2))
        playerList.append(Player(None, None, "Carey Price", "G", None, 30, 9, 1))

        return playerList

    @staticmethod
    def getAppConfig():
        teams = {  0: "Team A",
                    1: "Team B",
                    2: "Team C"}

        draft_order = [1, 2, 0]

        num_forwards = 5
        num_defense = 3
        num_goalies = 2

        return TestConfig(teams, draft_order, num_forwards, num_defense, num_goalies)



