import sys
import requests
from bs4 import BeautifulSoup

class Player(object):
    def __init__(self, overall_draft_num, draft_round, team, name, pos):
        self.overall_draft_num = overall_draft_num
        self.draft_round = draft_round
        self.team = team
        self.name = name
        self.pos = pos
        self.player_img = 0
        self.team_img = 0
        self.updatePlayerImgs()

    def __eq__(self, player):
        return  (self.overall_draft_num == player.overall_draft_num) and \
                (self.draft_round == player.draft_round) and \
                (self.team == player.team) and \
                (self.name == player.name) and \
                (self.pos == player.pos) and \
                (self.player_img == player.player_img) and \
                (self.team_img == player.team_img)

    def __ne__(self, player):
        return not self.__eq__(player)

    def updatePlayerImgs(self):
        self.player_img, self.team_img = self.getPlayerImgs()

    def getPlayerImgs(self):
        # This function is dependent on the html structure of the nhl.com search page
        player_index, nothing = self.checkPosition()
        if player_index != 0:
            player_name = self.name.replace(" ", "+")
            player_search_url = "http://www.nhl.com/ice/search.htm?tab=all&q=" + player_name
            r = requests.get(player_search_url)
            soup = BeautifulSoup(r.text, "html.parser")
            try:
                player_img_url = soup.find_all("ul", "results")[0].find_all("li")[player_index-1].div.div.a.img.get("src")
                player_img_data = requests.get(player_img_url).content
            except (IndexError, AttributeError):
                # Could not find player image give default one
                player_img_data = requests.get("http://3.cdn.nhle.com/photos/mugs/default.jpg").content

            try:
                team_img_data = soup.find_all("ul", "results")[0].find_all("li")[player_index-1].div.find_all("div")[1].a.div.img.get("title")
                #team_img_data = requests.get(team_img_url).content
            except (IndexError, AttributeError):
                # Could not find team image give default one
                #team_img_data = requests.get("http://www1.nhl.com/images/logos/medium.png").content
                team_img_data = "Default"

        else:
            # Player search fails for some reason (take default images)
            player_img_data = requests.get("http://3.cdn.nhle.com/photos/mugs/default.jpg").content
            team_img_data = requests.get("http://www1.nhl.com/images/logos/medium.png").content

        return player_img_data, team_img_data


    def checkPosition(self):
        # This function is dependent on the html structure of the nhl.com search page

        player_poss = []
        player_name = self.name.replace(" ", "+")
        player_search_url = "http://www.nhl.com/ice/search.htm?tab=all&q=" + player_name
        r = requests.get(player_search_url)
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            # Loop through all players till we run out of players
            i = 0
            while True:
                poss = []
                # Hack, the position value is sometimes on a different path? (stupid nhl.com)
                poss.append(soup.find_all("ul", "results")[0].find_all("li")[i].div.find_all("div")[1].find_all("span")[0].getText())
                poss.append(soup.find_all("ul", "results")[0].find_all("li")[i].div.find_all("div")[1].find_all("span")[1].getText())
                player_poss.append(poss)
                i += 1
        except (IndexError, AttributeError):
            if len(player_poss) == 0:
                # Player not found
                return False, self.name + " not found"

        for poss in player_poss:
            for pos in poss:
                if pos == "Center" or pos == "Left Wing" or pos == "Right Wing":
                    player_pos = 'F'
                elif pos == "Defenseman":
                    player_pos = 'D'
                elif pos == "Goalie":
                    player_pos = 'G'
                else:
                    # Player position not found
                    continue

                if self.pos != player_pos:
                    if player_poss.index(poss) == len(player_poss)-1:
                        return False, self.name + " is actually position " + player_pos + "....."
                    else:
                        # Multiple players with same name
                        continue
                else:
                    # SUPER HACKY!!!! Reusing this function in Player class to return the index of player and bool (encase there is multiple players with same name)
                    return player_poss.index(poss)+1, ""

        return False, self.name + " has no position :s"
