from board import Board
from ship import Ship
import pygame
class Player:
    def __init__ (self, size: int, name: str):
        self.name = name
        self.size = size
        self.board = Board(self.size, self.name)
        self.lives = 5
        self.__initialize_game()

    def __initialize_game(self):
        for i in range(self.size):
            fleet_objects = []
            for j in range(self.size):
                ship = Ship("N", (i,j), self.name)
                fleet_objects.append(ship)
                self.board.fleet_sprites.add(ship)

            self.board.fleet_objects.append(fleet_objects)

    def reset_board (self):
        self.board.fleet_sprites.empty()
        self.board.fleet_objects.clear()
        self.__initialize_game()