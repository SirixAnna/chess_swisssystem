from PQtGUI import *
# Todo
# start next round doesnt work, when current pairing table is not currentround
# empty players raise an error
# unable to create pairings, when round number is to high for player number
# sonneborn berger und bucholz (nach end tournament)

# test if all fide rules are fulfilled


def get_names(players):
    pn = []
    for p in players:
        pn += [p.name]
    return pn


def test_colors(pairing):
    p0 = pairing[0]
    p1 = pairing[1]
    p0.set_color_num()
    p1.set_color_num()
    p0.set_color()
    p1.set_color()
    if p0.color == p1.color:
        if p0.color == 0:
            return True
        else:
            return False
    else:
        return True


class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.stats = []
        self.colors = []
        self.color_num = 0
        self.color = 0
        self.opponents = []
        self.floater = None  # None, u(Up) or d(Down)
        self.bye = False
        self.sonneborn = 0
        self.buchholz = 0

    def set_sonneborn(self):
        s = 0
        for r in range(len(self.stats)):
            if self.stats[r] == 1.0:
                s += self.opponents[r].points
            elif self.stats[r] == 0.5:
                s += self.opponents[r].points / 2
        self.sonneborn = s

    def set_buchholz(self):
        b = 0
        for o in self.opponents:
            b += o.points
        self.buchholz = b

    def set_color_num(self):
        w = 0
        b = 0
        for color in self.colors:
            if color == "w":
                w += 1
            if color == "b":
                b += 1
        self.color_num = w-b

    def set_color(self):
        if len(self.colors) > 1:
            if self.color_num == -2 or (self.colors[-1] == "b" and self.colors[-2] == "b"):
                self.color = 1
            elif self.color_num == 2 or (self.colors[-1] == "w" and self.colors[-2] == "w"):
                self.color = -1
            else:
                self.color = 0
        else:
            self.color = 0


class Group:
    def __init__(self, players):
        self.players = players
        self.floaters = []
        self.new_floaters = []
        self.unpaired_players = None
        self.npairings = None
        self.pairings = []

    def create_pairings(self):
        self.order_by_points()
        self.unpaired_players = self.players.copy()
        self.npairings = int(len(self.players)/2)
        while len(self.unpaired_players) > 1:
            p0 = self.unpaired_players[0]
            found = False
            for p1 in self.unpaired_players[1:]:
                if p1 not in p0.opponents and test_colors([p0, p1]) and not found:
                    if p0.color > p1.color:
                        self.pairings += [[p0, p1]]
                    else:
                        self.pairings += [[p1, p0]]
                    self.unpaired_players.remove(p0)
                    self.unpaired_players.remove(p1)
                    found = True
            if not found:
                for pairing in self.pairings:
                    if not found:
                        p0_a = pairing[0]
                        p1_a = pairing[1]
                        if p0_a not in p0.opponents and test_colors([p0, p0_a]):
                            found = False
                            for p1 in self.unpaired_players[1:]:
                                if p1 not in p1_a.opponents and test_colors([p1_a, p1]) and not found:
                                    self.pairings.remove(pairing)
                                    if p0_a.color > p0.color:
                                        self.pairings += [[p0_a, p0]]
                                    else:
                                        self.pairings += [[p0, p0_a]]
                                    if p1_a.color > p1.color:
                                        self.pairings += [[p1_a, p1]]
                                    else:
                                        self.pairings += [[p1, p1_a]]
                                    self.unpaired_players.remove(p0)
                                    self.unpaired_players.remove(p1)
                                    found = True
                            if not found:
                                if p1_a not in p0.opponents and test_colors([p0, p1_a]):
                                    found = False
                                    for p1 in self.unpaired_players[1:]:
                                        if p1 not in p0_a.opponents and test_colors([p0_a, p1]) and not found:
                                            self.pairings.remove(pairing)
                                            if p1_a.color > p0.color:
                                                self.pairings += [[p1_a, p0]]
                                            else:
                                                self.pairings += [[p0, p1_a]]
                                            if p0_a.color > p1.color:
                                                self.pairings += [[p0_a, p1]]
                                            else:
                                                self.pairings += [[p1, p0_a]]
                                            self.unpaired_players.remove(p0)
                                            self.unpaired_players.remove(p1)
                                            found = True
                if not found:
                    self.unpaired_players.remove(p0)
                    self.new_floaters += [p0]
        self.new_floaters += self.unpaired_players
        self.unpaired_players = self.new_floaters.copy()
        self.new_floaters = []
        self.set_floaters()

    def add_from_above(self, floaters):
        self.players += floaters
        self.floaters += floaters
        self.order_by_points()

    def order_by_points(self):
        self.players.sort(key=lambda p: p.points, reverse=True)
        for player in self.players:
            if player.bye:
                self.players.remove(player)
                self.players = [player] + self.players

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
            points -= 0.5

    def create_pairings(self):
        for group in self.groups:
            group.add_from_above(self.leftovers)
            group.create_pairings()
            self.leftovers = group.unpaired_players
            for p in self.leftovers:
                group.players.remove(p)
            self.pairings += group.pairings
        if not len(self.leftovers) == 0:
            if len(self.leftovers) > 1:
                self.add_pairings()
            else:
                self.groups += [Group(self.leftovers)]
                for p in self.groups[-1].players:
                    if p.bye:
                        self.change_pairings(p)
                    else:
                        p.bye = True
                        self.pairings += [[p]]
        self.set_player_colors()
        self.set_player_opponents()

    def add_pairings(self):
        while len(self.leftovers) > 1:
            p_0 = self.leftovers[0]
            p_1 = self.leftovers[1]
            found = False
            for pairing in reversed(self.pairings):
                if not found:
                    p0 = pairing[0]
                    p1 = pairing[1]
                    if p_0 not in p0.opponents and test_colors([p_0, p0]) and \
                            p_1 not in p1.opponents and test_colors([p_1, p1]):
                        self.pairings.remove(pairing)
                        if p_0.color > p0.color:
                            self.pairings += [[p_0, p0]]
                        else:
                            self.pairings += [[p0, p_0]]
                        if p_1.color > p1.color:
                            self.pairings += [[p_1, p1]]
                        else:
                            self.pairings += [[p1, p_1]]
                        found = True
                    elif p_1 not in p0.opponents and test_colors([p_1, p0]) and \
                            p_0 not in p1.opponents and test_colors([p_0, p1]):
                        self.pairings.remove(pairing)
                        if p_1.color > p0.color:
                            self.pairings += [[p_1, p0]]
                        else:
                            self.pairings += [[p0, p_1]]
                        if p_0.color > p1.color:
                            self.pairings += [[p_0, p1]]
                        else:
                            self.pairings += [[p1, p_0]]
                        found = True
            if not found:
                if len(self.pairings) > 0:
                    pairing = self.pairings[-1]
                    self.leftovers += pairing
                    self.pairings.remove(pairing)
                else:
                    if len(self.groups[0].players) > 1:
                        self.pairings = []
                        self.groups[0].players[0], self.groups[0].players[1] = \
                            self.groups[0].players[1], self.groups[0].players[0]
                        print(1)
                        self.create_pairings()
                    else:
                        print("couldnt find pairing")
                        """
                        self.pairings = []
                        self.groups[1].players += self.groups[0].players
                        self.groups = self.groups[1:]
                        print(2)
                        self.create_pairings()
                        """

    def change_pairings(self, p):
        found = False
        for pairing in reversed(self.pairings):
            if not found:
                p0 = pairing[0]
                p1 = pairing[1]
                if not p0.bye:
                    if p not in p1.opponents and test_colors([p, p1]):
                        self.pairings.remove(pairing)
                        if p.color > p1.color:
                            self.pairings += [[p, p1]]
                        else:
                            self.pairings += [[p1, p]]
                        self.pairings += [[p0]]
                        p0.bye = True
                        found = True
                if not found:
                    if not p1.bye:
                        if p not in p0.opponents and test_colors([p, p0]):
                            self.pairings.remove(pairing)
                            if p.color > p0.color:
                                self.pairings += [[p, p0]]
                            else:
                                self.pairings += [[p0, p]]
                            self.pairings += [[p1]]
                            p1.bye = True
                            found = True

    def set_player_colors(self):
        for pairing in self.pairings:
            if len(pairing) == 2:
                pairing[0].colors += ["w"]
                pairing[1].colors += ["b"]
            else:
                pairing[0].colors += ["w"]

    def set_player_opponents(self):
        for pairing in self.pairings:
            if len(pairing) > 1:
                p0 = pairing[0]
                p1 = pairing[1]
                p0.opponents += [p1]
                p1.opponents += [p0]
            else:
                p0 = pairing[0]
                p0.opponents += [Player("bye")]

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

