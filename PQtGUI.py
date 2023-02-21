import sys
from swiss_t import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTableWidget, QTableWidgetItem, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Swiss Tournament Administration")
        self.setGeometry(0, 0, width, height)
        self.width = width
        self.height = height

        self.pairings = []
        self.players = []
        self.pairing_table = None
        self.player_table = None

        self.playersHeading = QLabel("<h2>Players</h2>", self)
        self.playersHeading.move(int(width*2/10), 15)

        self.roundsHeading = QLabel("<h2>Rounds</h2>", self)
        self.roundsHeading.move(int(width*6/10), 15)

        self.create_player_table()
        self.create_pairing_table()

    def set_players(self, players):
        self.players = players
        self.create_player_table()

    def set_pairings(self, pairings):
        self.pairings = pairings
        self.create_pairing_table()

    def create_player_table(self):
        self.player_table = QTableWidget(self)

        self.player_table.setColumnCount(2)
        self.player_table.setColumnWidth(0, 200)
        self.player_table.setColumnWidth(1, 50)

        self.player_table.setRowCount(len(self.players)+1)
        for row in range(len(self.players)+1):
            self.player_table.setRowHeight(row, 50)

        self.player_table.setGeometry(int(self.width*2/10), 80, 250+25, 50*(len(self.players)+1)+25)

        row = 0
        for player in self.players:
            self.player_table.setItem(row, 0, QTableWidgetItem(str(player)))
            row += 1

    def create_pairing_table(self):
        # create Pairing Table
        self.pairing_table = QTableWidget(self)

        self.pairing_table.setColumnCount(2)
        self.pairing_table.setColumnWidth(0, 200)
        self.pairing_table.setColumnWidth(1, 200)

        self.pairing_table.setRowCount(len(self.pairings)+1)
        for row in range(len(self.pairings)+1):
            self.pairing_table.setRowHeight(row, 50)

        self.pairing_table.setGeometry(int(self.width*6/10), 80, 400+25, 50*(len(self.pairings)+1)+25)


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
    window.set_players([1, 2, 3]) # set players
    window.set_pairings([[1, 2], [3, 4]])# add Pairings
    window.show()

    sys.exit(app.exec())
