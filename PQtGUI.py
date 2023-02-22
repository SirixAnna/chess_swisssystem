import sys
from swiss_t import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTableWidget, \
    QTableWidgetItem, QMainWindow, QPushButton, QComboBox


class MainWindow(QMainWindow):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Swiss Tournament Administration")
        self.setGeometry(0, 0, width, height)
        self.width = width
        self.height = height

        self.pairings = []
        self.players = []
        self.numRounds = 40
        self.cround = -1
        self.roundHeadings = []
        self.pairingTables = []
        for r in range(self.numRounds):
            self.roundHeadings += [QLabel(self)]
            self.roundHeadings[r].setHidden(True)
            self.pairingTables += [QTableWidget(self)]
            self.pairingTables[r].setHidden(True)
        self.playerTable = None

        self.playersHeading = QLabel("<h2>Players</h2>", self)
        self.playersHeading.move(int(self.width*1/10), 15)

        self.roundsHeading = QLabel("<h2>Rounds</h2>", self)
        self.roundsHeading.move(int(self.width*4/10), 15)

        self.startTournamentButton = QPushButton("start Tournament", self)
        self.startTournamentButton.setGeometry(int(self.width * 8 / 10), 40, 200, 30)
        self.startTournamentButton.clicked.connect(self.click_start_tournament)

        self.nextRoundButton = QPushButton("+ next Round", self)
        self.nextRoundButton.setGeometry(int(self.width * 8 / 10), 80, 200, 30)
        self.nextRoundButton.clicked.connect(self.click_next_round)
        self.nextRoundButton.setHidden(True)

        self.endTournamentButton = QPushButton("end Tournament", self)
        self.endTournamentButton.setGeometry(int(self.width * 8 / 10), 120, 200, 30)
        self.endTournamentButton.clicked.connect(self.click_end_tournament)
        self.endTournamentButton.setHidden(True)

        self.addPlayerButton = QPushButton("add Player", self)
        self.addPlayerButton.setGeometry(int(width * 1 / 10), self.height - 100,
                                         200, 30)
        self.addPlayerButton.clicked.connect(self.click_add_player)

        self.removePlayerButton = QPushButton("remove Player", self)
        self.removePlayerButton.setGeometry(
            int(width * 1 / 10), self.height - 70, 200, 30)
        self.removePlayerButton.clicked.connect(self.click_remove_player)

        self.create_player_table()

        # swiss_t
        self.tournament = None

    def click_end_tournament(self):
        self.close()

    def click_start_tournament(self):
        self.tournament = Tournament(self.players)

        self.addPlayerButton.setHidden(True)
        self.removePlayerButton.setHidden(True)
        self.startTournamentButton.setHidden(True)
        self.nextRoundButton.setHidden(False)
        self.endTournamentButton.setHidden(False)
        self.playerTable.setCurrentCell(0, 1)
        self.playerTable.clearSelection()
        self.set_players()
        self.click_next_round()

    def click_next_round(self):
        self.cround += 1
        self.tournament.start_round(self.cround)
        self.set_pairings(self.tournament.round.get_pairings())

    def click_add_player(self):
        rowPosition = self.playerTable.rowCount()
        self.playerTable.insertRow(rowPosition)
        self.playerTable.setRowHeight(rowPosition, 50)

    def click_remove_player(self):
        pass

    def set_players(self):
        rows = self.playerTable.rowCount()
        for row in range(rows):
            self.players += [Player(self.playerTable.item(row, 0).text())]
        self.players.sort(key=lambda p: p.name)

    def set_pairings(self, pairings):
        self.pairings = pairings
        self.create_pairing_table()

    def create_player_table(self):
        self.playerTable = QTableWidget(self)

        self.playerTable.setColumnCount(2)
        self.playerTable.setColumnWidth(0, 200)
        self.playerTable.setColumnWidth(1, 50)

        self.playerTable.setRowCount(len(self.players))
        for row in range(len(self.players)):
            self.playerTable.setRowHeight(row, 50)

        self.playerTable.setGeometry(int(
            self.width * 1 / 10), 80, 250 + 25, self.height-200)

        self.playerTable.setHorizontalHeaderLabels(["Player", "Points"])

    def create_pairing_table(self):
        # create Pairing Table
        self.roundHeadings[self.cround].setHidden(False)
        self.roundHeadings[self.cround].setText("Round " + str(self.cround+1))
        self.roundHeadings[self.cround].move(int(self.width*4/10), 50)
        self.roundHeadings[self.cround-1].setHidden(True)

        self.pairingTables[self.cround].setHidden(False)
        self.pairingTables[self.cround].setColumnCount(3)
        self.pairingTables[self.cround].setColumnWidth(0, 200)
        self.pairingTables[self.cround].setColumnWidth(1, 100)
        self.pairingTables[self.cround].setColumnWidth(2, 200)
        self.pairingTables[self.cround-1].setHidden(True)

        self.pairingTables[self.cround].setRowCount(len(self.pairings))
        for row in range(len(self.pairings)):
            self.pairingTables[self.cround].setRowHeight(row, 50)
            self.pairingTables[self.cround].setItem(row, 0, QTableWidgetItem(str(self.pairings[row][0])))
            combo = QComboBox()
            combo.addItems(["", "0:1", "0,5:0,5", "1:0"])
            self.pairingTables[self.cround].setCellWidget(row, 1, combo)
            if len(self.pairings[row]) > 1:
                self.pairingTables[self.cround].setItem(row, 2, QTableWidgetItem(str(self.pairings[row][1])))

        self.pairingTables[self.cround].setGeometry(int(self.width * 4 / 10), 80, 500 + 25, 50 * len(self.pairings) + 25)

        self.pairingTables[self.cround].setHorizontalHeaderLabels(["White", "Result", "Black"])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # get screen geometry
    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    w = rect.width()
    h = rect.height()

    # create window
    window = MainWindow(w, h)
    #window.set_players()  # set players
    window.show()

    sys.exit(app.exec())
