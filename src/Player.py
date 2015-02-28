import sys


class Player(object):
    def __init__(self, overall_draft_num, draft_round, team, name, pos):
        self.overall_draft_num = overall_draft_num
        self.draft_round = draft_round
        self.team = team
        self.name = name
        self.pos = pos
