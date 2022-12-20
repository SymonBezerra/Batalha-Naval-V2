from fleet import Fleet
from board import Board
from ship import Ship
class Player:
    def __init__ (self, size: int):
        self.name = "Player"
        self.size = size
        self.board = Board(self.size, self.name)
        self.fleet = Fleet(self.size)

    def initialize_game(self):
        for i in range(self.size):
            fleet_line = []
            for j in range(self.size):
                ship = Ship("N", (i,j))
                fleet_line.append((i,j))
            self.fleet.ships.append(fleet_line)