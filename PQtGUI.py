from swiss_2 import *
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, \
    QTableWidgetItem, QMainWindow, QPushButton, QComboBox, QMessageBox


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
        self.cRound = -1
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

        self.roundSelectCombo = QComboBox(self)
        self.roundSelectCombo.setGeometry(int(self.width * 8 / 10), 160, 200, 30)
        self.roundSelectCombo.setHidden(True)
        self.roundSelectCombo.currentIndexChanged.connect(self.change_round)

        self.create_player_table()

        # swiss_t
        self.tournament = None

    def click_end_tournament(self):
        """
        for table in self.pairingTables:
            table.setHidden(True)
        for heading in self.roundHeadings:
            heading.setHidden(True)
        self.playerTable.setGeometry(int(
            self.width * 4 / 10), 80, 250 + 25, self.height-200)
        """
        self.close()

    def click_start_tournament(self):
        self.tournament = Tournament(self.players)

        self.addPlayerButton.setHidden(True)
        self.removePlayerButton.setHidden(True)
        self.startTournamentButton.setHidden(True)
        self.nextRoundButton.setHidden(False)
        self.endTournamentButton.setHidden(False)
        self.roundSelectCombo.setHidden(False)
        self.playerTable.setCurrentCell(0, 1)
        self.playerTable.clearSelection()
        self.set_players()
        self.click_next_round()

    def sonneborn_order(self):
        for player in self.players:
            player.set_sonneborn()
        p = None
        p_list = []
        p_current = []
        for player in self.players:
            if p == player.points:
                p_current += [player]
            else:
                p_current.sort(key=lambda p: p.sonneborn, reverse=True)
                p_current = self.buchholz_order(p_current)
                p_list += p_current
                p_current = []
                p_current += [player]
                p = player.points
        p_list += p_current
        self.players = p_list

    def buchholz_order(self, players):
        for player in self.players:
            player.set_buchholz()
        p = None
        p_list = []
        p_current = []
        for player in players:
            if p == player.sonneborn:
                p_current += [player]
            else:
                p_current.sort(key=lambda p: p.buchholz, reverse=True)
                p_list += p_current
                p_current = []
                p_current += [player]
                p = player.sonneborn
        p_list += p_current
        players = p_list
        return players

    def update_player_table(self):
        self.players.sort(key=lambda p: p.name)
        self.players.sort(key=lambda p: p.points, reverse=True)
        self.sonneborn_order()
        for row in range(len(self.players)):
            self.playerTable.setItem(row, 0, QTableWidgetItem(str(self.players[row].name)))
            self.playerTable.setItem(row, 1, QTableWidgetItem(str(self.players[row].points)))

    def click_next_round(self):
        try:
            self.set_round_results()
            self.update_player_table()

            self.cRound += 1
            self.tournament.start_round(self.cRound)
            self.set_pairings(self.tournament.round.get_pairings())

        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please select all game results, before starting next round!")
            msg.setWindowTitle("Warning")
            msg.exec_()

    def set_round_results(self):
        for row in range(self.pairingTables[self.cRound].rowCount()):
            p0 = self.tournament.round.pairings[row][0]
            result = self.pairingTables[self.cRound].cellWidget(row, 1).currentText()
            result = result.split(":")
            p0.points += float(result[0])
            p0.stats += [float(result[0])]
            if len(self.pairings[row]) > 1:
                p1 = self.tournament.round.pairings[row][1]
                p1.points += float(result[1])
                p1.stats += [float(result[1])]

    def click_add_player(self):
        row_position = self.playerTable.rowCount()
        self.playerTable.insertRow(row_position)
        self.playerTable.setRowHeight(row_position, 50)

    def click_remove_player(self):
        self.playerTable.removeRow(self.playerTable.currentRow())

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
        for heading in self.roundHeadings:
            heading.setHidden(True)
        self.roundHeadings[self.cRound].setHidden(False)
        self.roundHeadings[self.cRound].setText("Round " + str(self.cRound + 1))
        self.roundHeadings[self.cRound].move(int(self.width * 4 / 10), 50)

        if not self.cRound < len(self.roundSelectCombo):
            self.roundSelectCombo.addItem("Round " + str(self.cRound + 1))
        self.roundSelectCombo.setCurrentIndex(self.cRound)

        for table in self.pairingTables:
            table.setHidden(True)
        self.pairingTables[self.cRound].setHidden(False)
        self.pairingTables[self.cRound].setColumnCount(3)
        self.pairingTables[self.cRound].setColumnWidth(0, 200)
        self.pairingTables[self.cRound].setColumnWidth(1, 100)
        self.pairingTables[self.cRound].setColumnWidth(2, 200)

        self.pairingTables[self.cRound].setRowCount(len(self.pairings))
        for row in range(len(self.pairings)):
            self.pairingTables[self.cRound].setRowHeight(row, 50)
            self.pairingTables[self.cRound].setItem(row, 0, QTableWidgetItem(str(self.pairings[row][0])))
            combo = QComboBox()
            combo.addItems(["", "0:1", "0.5:0.5", "1:0"])
            self.pairingTables[self.cRound].setCellWidget(row, 1, combo)
            if len(self.pairings[row]) > 1:
                self.pairingTables[self.cRound].setItem(row, 2, QTableWidgetItem(str(self.pairings[row][1])))

        self.pairingTables[self.cRound].setGeometry(
            int(self.width * 4 / 10), 80, 500 + 25, 50 * len(self.pairings) + 25)

        self.pairingTables[self.cRound].setHorizontalHeaderLabels(["White", "Result", "Black"])

    def change_round(self):
        if not self.roundSelectCombo.currentIndex() == self.cRound:
            self.cRound = self.roundSelectCombo.currentIndex()
            for table in self.pairingTables:
                table.setHidden(True)
            self.pairingTables[self.cRound].setHidden(False)
            self.pairingTables[self.cRound].clearSelection()
            for heading in self.roundHeadings:
                heading.setHidden(True)
            self.roundHeadings[self.cRound].setHidden(False)


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
    # window.set_players()  # set players
    window.show()

    sys.exit(app.exec())
