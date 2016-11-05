import sys
import requests
from bs4 import BeautifulSoup
import os

class Player(object):
    def __init__(self, id, nhl_team, name, pos, page_url, overall_draft_num=None, draft_round=None, team=None):
        self.id = id
        self.nhl_team = nhl_team
        self.name = name
        self.pos = pos
        self.page_url = page_url

        self.team = team
        self.overall_draft_num = overall_draft_num
        self.draft_round = draft_round

        self.player_img = None
        self.team_img = None

    # Just used for test file (don't check the dynamic data that can change between years)
    # dynamic data: id, nhl_team, page_url
    def __eq__(self, player):
        return  (self.name == player.name) and \
                (self.pos == player.pos) and \
                (self.overall_draft_num == player.overall_draft_num) and \
                (self.draft_round == player.draft_round) and \
                (self.team == player.team)

    def __ne__(self, player):
        return not self.__eq__(player)

    def getPlayerImg(self):
        if self.player_img:
            return self.player_img
        else:
            self.updatePlayerImg()
        return self.player_img

    def getTeamImg(self):
        if self.team_img:
            return self.team_img
        else:
            self.updateTeamImg()
        return self.team_img

    def updatePlayerImg(self):
        if self.id:
            player_img_url = "https://nhl.bamcontent.com/images/headshots/current/168x168/" + self.id + ".jpg"
            result = requests.get(player_img_url)
        if not self.id or result.status_code == 404:
            if self.getPos() == 'G':
                self.player_img = requests.get("https://nhl.bamcontent.com/images/headshots/current/168x168/goalie.jpg").content
            else:
                self.player_img = requests.get("https://nhl.bamcontent.com/images/headshots/current/168x168/skater.jpg").content
        else:
            self.player_img = result.content

    def updateTeamImg(self):
        # Couldn't find the nhl.com url where team images stored (downloaded all team images)
        if self.nhl_team:
            self.team_img = os.getcwd().split('src')[0] + '/res/TeamImages/' + self.nhl_team + ".gif"
        else:
            self.team_img = os.getcwd().split('src')[0] + '/res/TeamImages/default.gif'

    def getPos(self):
        if self.pos in ['C', 'R', 'L']:
            return 'F'
        else:
            return self.pos

    # def updatePlayerImgs(self):
    #     self.player_img, self.team_img = self.getPlayerImgs()
    #
    # def getPlayerImgs(self):
    #
    #     # This function is dependent on the html structure of the nhl.com search page
    #     player_index, nothing = self.checkPosition()
    #     if player_index != 0:
    #         player_name = self.name.replace(" ", "+")
    #         player_search_url = "http://www.nhl.com/ice/search.htm?tab=all&q=" + player_name
    #         r = requests.get(player_search_url)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         try:
    #             player_img_url = soup.find_all("ul", "results")[0].find_all("li")[player_index-1].div.div.a.img.get("src")
    #             player_img_data = requests.get(player_img_url).content
    #         except (IndexError, AttributeError):
    #             # Could not find player image give default one
    #             player_img_data = requests.get("http://3.cdn.nhle.com/photos/mugs/default.jpg").content
    #
    #         try:
    #             team_img_data = soup.find_all("ul", "results")[0].find_all("li")[player_index-1].div.find_all("div")[1].a.div.img.get("title")
    #             #team_img_data = requests.get(team_img_url).content
    #         except (IndexError, AttributeError):
    #             # Could not find team image give default one
    #             #team_img_data = requests.get("http://www1.nhl.com/images/logos/medium.png").content
    #             team_img_data = "Default"
    #
    #     else:
    #         # Player search fails for some reason (take default images)
    #         player_img_data = requests.get("http://3.cdn.nhle.com/photos/mugs/default.jpg").content
    #         team_img_data = requests.get("http://www1.nhl.com/images/logos/medium.png").content
    #
    #     return player_img_data, team_img_data
