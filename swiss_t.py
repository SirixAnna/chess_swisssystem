# import time
import sys
from PQtGUI import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTableWidget, QTableWidgetItem, QMainWindow, QPushButton


def get_names(players):
    pn = []
    for p in players:
        pn += [p.name]
    return pn


class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.stats = []
        self.colors = []
        self.color_num = 0
        self.opponents = []
        self.floater = None  # None, u(Up) or d(Down)

    def set_color_num(self):
        w = 0
        b = 0
        for color in self.colors:
            if color == "w":
                w += 1
            if color == "b":
                b += 1
        self.color_num = w-b


class SubGroup:
    def __init__(self):
        self.players = []
        self.b_players = []
        self.w_players = []
        self.wob_players = []


class Group:
    def __init__(self, players):
        self.sub0 = SubGroup()  # subgroups
        self.sub1 = SubGroup()
        self.players = players
        self.floaters = []
        self.b_players = []
        self.w_players = []
        self.wob_players = []
        self.unpaired_players = None
        self.npairings = None
        self.pairings = []

    def create_subs(self):
        unsubed_p = self.players.copy()
        n_p = int(len(self.players)/2)  # num players per sub
        f = 0
        a = 0
        while len(self.sub0.players) < n_p:
            if f < len(self.floaters):
                self.sub0 += [self.floaters[f]]
                unsubed_p.remove(self.floaters[f])
                f += 1
            else:
                if self.players[a] in unsubed_p:
                    self.sub0 += [self.players[a]]
                    unsubed_p.remove(self.players[a])
                a += 1
        self.sub1.players = unsubed_p

    def add_from_above(self, floaters):
        self.players += floaters
        self.floaters += floaters
        self.order_by_points()

    def order_by_points(self):
        self.players.sort(key=lambda p: p.points, reverse=True)

    def set_player_colors(self):
        for p in self.unpaired_players:
            if p.color_num == 2:
                self.b_players += [p]
            elif p.color_num == -2:
                self.w_players += [p]
            else:
                self.wob_players += [p]

    def create_pairings(self):
        self.order_by_points()
        self.unpaired_players = self.players.copy()
        self.npairings = int(len(self.players)/2)
        for k in range(self.npairings):
            self.pairings += [[self.players[k], self.players[k+self.npairings]]]
            self.unpaired_players.remove(self.players[k])
            self.unpaired_players.remove(self.players[k+self.npairings])
        self.set_floaters()

    def set_floaters(self):
        for pairing in self.pairings:
            p0 = pairing[0]
            p1 = pairing[1]
            if not p0.points == p1.points:
                if p0.points > p1.points:
                    p0.floater = "d"
                    p1.floater = "u"
                else:
                    p0.floater = "u"
                    p1.floater = "d"
            else:
                p0.floater = None
                p1.floater = None


class Round:
    def __init__(self, players):
        self.players = players
        self.groups = []
        self.cround = 0
        self.leftovers = []
        self.pairings = []

    def get_pairings(self):
        pairings = []
        for pairing in self.pairings:
            players = []
            for pl in pairing:
                players += [pl.name]
            pairings += [players]
        return pairings

    def order_by_points(self):
        self.players.sort(key=lambda p: p.points, reverse=True)

    def create_groups(self):
        self.order_by_points()
        ungrouped_players = self.players.copy()
        points = self.cround
        while not len(ungrouped_players) == 0:
            group = []
            for p in self.players:
                if p.points == points:
                    group += [p]
                    ungrouped_players.remove(p)
            self.groups += [Group(group)]
            points -= 1

    def create_pairings(self):
        for group in self.groups:
            group.add_from_above(self.leftovers)
            group.create_pairings()
            self.leftovers = group.unpaired_players
            for p in self.leftovers:
                group.players.remove(p)
            self.pairings += group.pairings
        if not len(self.leftovers) == 0:
            self.groups += [Group(self.leftovers)]
            self.pairings += [self.groups[-1].players]
        self.set_player_colors()

    def set_player_colors(self):
        for pairing in self.pairings:
            if len(pairing) == 2:
                pairing[0].colors += ["w"]
                pairing[1].colors += ["b"]
            else:
                pairing[0].colors += [None]

    def set_player_color_nums(self):
        for p in self.players:
            p.set_color_num()


class Tournament:
    def __init__(self, players):
        self.players = players
        self.round = None
        self.standing = []

    def start_round(self, cround):
        self.round = Round(self.players)
        self.round.set_player_color_nums()
        self.round.cround = cround
        self.round.order_by_points()
        self.round.create_groups()
        self.round.create_pairings()


if __name__ == '__main__':
    '''
    print("Please enter Player names. Press enter after each name. Press enter again, when finished")
    finished = False
    playerNames = []
    while not finished:
        nameP = input("name:")
        if not nameP == "":
            playerNames += [Player(nameP)]
        else:
            finished = True
    playerNames.sort(key=lambda p: p.name)
    numRounds = input("Enter number of rounds:")
    tournament = Tournament(playerNames)
    '''

    # GUI
    app = QApplication(sys.argv)

    # get screen geometry
    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    w = rect.width()
    h = rect.height()

    # create window
    window = MainWindow(w, h)
    names = []
    #window.set_players(names)  # set players
    window.show()

    sys.exit(app.exec())
    ####

'''
    for i in range(int(numRounds)):
        tournament.start_round(i)
        for player in tournament.players:
            player.points += float(input("result player "+player.name))
'''



