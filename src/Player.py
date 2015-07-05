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

    def updatePlayerImgs(self):
        self.player_img, self.team_img = self.getPlayerImgs()

    def getPlayerImgs(self):
        # This function is dependent on the html structure of the nhl.com search page

        player_name = self.name.replace(" ", "+")
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