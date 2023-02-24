import math
# continue with c


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
        self.color_num = w - b


class SubGroup:
    def __init__(self):
        self.players = []


class Group:
    def __init__(self, players):
        self.sub0 = SubGroup()  # subgroups
        self.sub1 = SubGroup()
        self.players = players
        self.floaters = []
        self.unpaired_players = None
        self.npairings = None
        self.pairings = []
        self.x = 0
        self.w = 0
        self.b = 0
        self.q = 0

        self.trials = 0

    def create_subs(self):
        unsubed_p = self.players.copy()
        n_p = int(len(self.players) / 2)  # num players per sub
        if len(self.floaters) > 0:
            for p in self.floaters:
                if len(self.sub0.players) < n_p:
                    self.sub0.players += [p]
                    unsubed_p.remove(p)
            self.sub1.players = unsubed_p
        else:
            while len(self.sub0.players) < n_p:
                self.sub0.players += [unsubed_p[0]]
                unsubed_p.remove(unsubed_p[0])
            self.sub1.players = unsubed_p

    def add_from_above(self, floaters):
        self.players += floaters
        self.floaters += floaters
        self.order_by_points()

    def order_by_points(self):
        self.players.sort(key=lambda p: p.points, reverse=True)

    def set_bwq(self):
        for p in self.players:
            if p.color_num < 0:
                self.w += 1
            elif p.color_num == 0 and p.colors[:-1] == "b":
                self.w += 1
            else:
                self.b += 1
        self.q = math.ceil(len(self.players) / 2)
        if self.b > self.w:
            self.x = self.b - self.q
        else:
            self.x = self.w - self.q

    def set_colors(self, pairing):
        p0 = pairing[0]
        p1 = pairing[1]
        if p0 not in p1.opponents:
            if p0.color_num == p1.color_num:
                if abs(p0.color_num) == 2:
                    return False
                else:
                    self.pairings += [[p1, p0]]
                    return True
            elif p0.color_num < p1.color_num:
                self.pairings += [[p0, p1]]
                return True
            elif p0.color_num > p1.color_num:
                self.pairings += [[p1, p0]]
                return True
        else:
            return False

    def create_pairings(self):
        #self.set_bwq()
        self.unpaired_players = self.players.copy()
        for p in range(len(self.sub0.players)):
            print("p"+str(p))
            success = self.set_colors([self.sub0.players[p], self.sub1.players[p]])
            if not success:
                if self.trials < 20:
                    print("t"+str(self.trials))
                    self.trials += 1
                    self.change_order(p)
            else:
                print(self.unpaired_players)
                print(self.players)
                print(self.pairings)
                print(self.sub0.players[p])
                print(p)
                self.unpaired_players.remove(self.sub0.players[p])
                self.unpaired_players.remove(self.sub1.players[p])
        if len(self.unpaired_players) > 1 and self.trials < 20:
            self.players = self.unpaired_players.copy()
            self.floaters = []
            self.sub0.players = []
            self.sub1.players = []
            self.create_subs()
            self.create_pairings()
        else:
            self.set_floaters()

    def change_order(self, p):
        self.unpaired_players = self.players.copy()
        self.pairings = []
        if len(self.sub1.players) > p+1:
            self.sub1.players[p], self.sub1.players[p + 1] = self.sub1.players[p + 1], self.sub1.players[p]
        elif len(self.sub1.players) < p+1:
            self.sub1.players[p], self.sub1.players[p - 1] = self.sub1.players[p - 1], self.sub1.players[p]
        self.create_pairings()

        """
        self.order_by_points()
        self.unpaired_players = self.players.copy()
        self.npairings = int(len(self.players)/2)
        self.create_subs()
        for k in range(self.npairings):
            self.pairings += [[self.players[k], self.players[k+self.npairings]]]
            self.unpaired_players.remove(self.players[k])
            self.unpaired_players.remove(self.players[k+self.npairings])
        """
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
            points -= 0.5

    def create_pairings(self):
        for group in self.groups:
            group.add_from_above(self.leftovers)
            group.create_subs()
            group.create_pairings()
            self.leftovers = group.unpaired_players
            for p in self.leftovers:
                group.players.remove(p)
            self.pairings += group.pairings
        if not len(self.leftovers) == 0:
            self.groups += [Group(self.leftovers)]
            self.pairings += [self.groups[-1].players]
        self.set_player_colors()
        self.set_player_opponents()

    def set_player_opponents(self):
        for pairing in self.pairings:
            if len(pairing) > 1:
                p0 = pairing[0]
                p1 = pairing[1]
                p0.opponents += [p1]
                p1.opponents += [p0]

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

