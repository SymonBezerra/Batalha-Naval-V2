from player import Player
from cpu import CPU
from ship import Ship
import pygame
class Board:

    def __init__ (self, size: int, player_name: str):
        self.size = size
        self.fleet = pygame.sprite.Group()
        # these will work as the previous version's memories
        
        # self.__board_test(self.fleet)

        self.init_pos = (0,0)
        if player_name == "player": self.init_pos = (50, 160)
        else: self.init_pos = (630, 160)

    # def __board_test (self, fleet: pygame.sprite.Group):
    #     for i in range(self.size):
    #         for j in range (self.size):
    #             fleet.add(Ship("N", (i,j)))