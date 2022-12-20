from player import Player
from cpu import CPU
from ship import Ship, SHIP_SIZES
import pygame
class Board:

    def __init__ (self, size: int, player_name: str):
        self.size = size
        self.fleet_sprites = pygame.sprite.Group()
        # for drawing
        self.fleet_coordinates = []
        # for Ship.setTag()
        # these will work as the previous version's memories
        
        # self.__board_test(self.fleet)

        self.init_pos = (0,0)
        if player_name == "player": 
            self.init_pos = (50, 160)
        else: 
            self.init_pos = (630, 160)

    # def __board_test (self, fleet: pygame.sprite.Group):
    #     for i in range(self.size):
    #         for j in range (self.size):
    #             fleet.add(Ship("N", (i,j)))

    def set_tag(self, coordinates: list, tag: str) -> None:
        for coordinate in coordinates:
            ship = self.fleet_coordinates[coordinate[0]][coordinate][1]
            ship.tag = tag

    def check_avaliable_placement (self, coordinates: list, ship_tag: str,
                                    direction: int) -> bool:
        # 0 = up, 1 = down, 2 = left, 3 = right
        if direction == 0:
            if coordinates[0][0] + SHIP_SIZES[ship_tag] <= self.size:
                for coordinate in coordinates:
                    ship = self.fleet_coordinates[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False     
        
        return True