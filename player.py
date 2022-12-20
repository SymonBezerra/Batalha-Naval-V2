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
            fleet_coords_line = []
            fleet_sprites_line = []
            for j in range(self.size):
                ship = Ship("N", (i,j))
                self.board.fleet_sprites.add(ship)
                fleet_coords_line.append((i,j))
                fleet_sprites_line.append(ship)
            self.fleet.ships.append(fleet_coords_line)
            self.board.fleet_coordinates.append(fleet_sprites_line)