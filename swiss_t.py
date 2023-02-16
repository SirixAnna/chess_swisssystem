# import time
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
        self.opponents = []
        self.floater = None  # None, Up or Down


class Group:
    def __init__(self, players):
        self.players = players
        self.unpaired_players = None
        self.npairings = None
        self.pairings = []

    def order_by_points(self):
        self.players.sort(key=lambda p: p.points, reverse=True)

    def create_pairings(self):
        self.order_by_points()
        self.unpaired_players = self.players.copy()
        self.npairings = int(len(self.players)/2)
        for k in range(self.npairings):
            self.pairings += [[self.players[k], self.players[k+self.npairings]]]
            self.unpaired_players.remove(self.players[k])
            self.unpaired_players.remove(self.players[k+self.npairings])


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
                players += pl.name
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
            for player in self.players:
                if player.points == points:
                    group += [player]
                    ungrouped_players.remove(player)
            self.groups += [Group(group)]
            points -= 1

    def create_pairings(self):
        for group in self.groups:
            group.players += self.leftovers
            group.create_pairings()
            self.leftovers = group.unpaired_players
            for player in self.leftovers:
                group.players.remove(player)
            self.pairings += group.pairings
        if not len(self.leftovers) == 0:
            self.groups += [Group(self.leftovers)]
            self.pairings += [self.groups[-1].players]


class Tournament:
    def __init__(self, players, nrounds):
        self.players = players
        self.nrounds = nrounds
        self.round = None
        self.standing = []

    def start_round(self, cround):
        self.round = Round(self.players)
        self.round.cround = cround
        self.round.order_by_points()
        self.round.create_groups()
        self.round.create_pairings()
        print(self.round.get_pairings())


if __name__ == '__main__':
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
    tournament = Tournament(playerNames, numRounds)

    for i in range(int(numRounds)):
        tournament.start_round(i)
        for player in tournament.players:
            player.points += float(input("result player "+player.name))

