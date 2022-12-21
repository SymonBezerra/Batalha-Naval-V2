from fleet import Fleet
from board import Board
from ship import Ship
class Player:
    def __init__ (self, size: int, name: str):
        self.name = name
        self.size = size
        self.board = Board(self.size, self.name)
        self.__initialize_game()

    def __initialize_game(self):
        for i in range(self.size):
            fleet_objects = []
            for j in range(self.size):
                ship = Ship("N", (i,j))
                fleet_objects.append(ship)
                self.board.fleet_sprites.add(ship)

            self.board.fleet_objects.append(fleet_objects)