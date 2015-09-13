import sys
from TestConfig import TestConfig
sys.path.insert(0, '../')
from Player import Player

class PlayerData(object):
    @staticmethod
    def getPlayerData():
        playerList = []
        playerList.append(Player(1, 0, 1, "Sidney Crosby", "F"))
        playerList.append(Player(2, 0, 2, "Alex Ovechkin", "F"))
        playerList.append(Player(3, 0, 0, "Jason Spezza", "F"))
        playerList.append(Player(4, 1, 0, "Nicklas Backstrom", "F"))
        playerList.append(Player(5, 1, 2, "Daniel Sedin", "F"))
        playerList.append(Player(6, 1, 1, "Henrik Sedin", "F"))
        playerList.append(Player(7, 2, 1, "Jamie Benn", "F"))
        playerList.append(Player(8, 2, 2, "John Tavares", "F"))
        playerList.append(Player(9, 2, 0, "Claude Giroux", "F"))
        playerList.append(Player(10, 3, 0, "Jakub Voracek", "F"))
        playerList.append(Player(11, 3, 2, "Nick Foligno", "F"))
        playerList.append(Player(12, 3, 1, "Tyler Johnson", "F"))
        playerList.append(Player(13, 4, 1, "Steven Stamkos", "F"))
        playerList.append(Player(14, 4, 2, "Ryan Getzlaf", "F"))
        playerList.append(Player(15, 4, 0, "Corey Perry", "F"))
        playerList.append(Player(16, 5, 0, "Erik Karlsson", "D"))
        playerList.append(Player(17, 5, 2, "PK Subban", "D"))
        playerList.append(Player(18, 5, 1, "Alexander Edler", "D"))
        playerList.append(Player(19, 6, 1, "Mark Giordano", "D"))
        playerList.append(Player(20, 6, 2, "Sheldon Souray", "D"))
        playerList.append(Player(21, 6, 0, "Dustin Byfuglien", "D"))
        playerList.append(Player(22, 7, 0, "Toby Enstrom", "D"))
        playerList.append(Player(23, 7, 2, "Kevin Bieksa", "D"))
        playerList.append(Player(24, 7, 1, "Kris Letang", "D"))
        playerList.append(Player(25, 8, 1, "Tuukka Rask", "G"))
        playerList.append(Player(26, 8, 2, "Jonas Hiller", "G"))
        playerList.append(Player(27, 8, 0, "Ryan Miller", "G"))
        playerList.append(Player(28, 9, 0, "Henrik Lundqvist", "G"))
        playerList.append(Player(29, 9, 2, "Roberto Luongo", "G"))
        playerList.append(Player(30, 9, 1, "Carey Price", "G"))

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



