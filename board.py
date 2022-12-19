from player import Player
from cpu import CPU
from ship import Ship
import pygame
class Board:
    # def __init__ (self, size: int, player: Player, cpu: CPU):
    def __init__ (self, size: int):
        self.size = size
        self.player_fleet = pygame.sprite.Group()
        self.cpu_fleet = pygame.sprite.Group()
        # these will work as the previous version's memories
        self.__board_test(self.player_fleet)

    def __board_test (self, fleet: pygame.sprite.Group):
        for i in range(self.size):
            for j in range (self.size):
                fleet.add(Ship("N", (i,j)))