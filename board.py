from ship import Ship, SHIP_SIZES
import pygame
class Board:

    def __init__ (self, size: int, player_name: str):
        self.size = size
        self.fleet_sprites = pygame.sprite.Group()
        # for drawing
        self.fleet_objects = []
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

    def set_ships_tag(self, coordinates: list, tag: str) -> None:
        for coordinate in coordinates:
            ship = self.fleet_objects[coordinate[0]][coordinate[1]]
            ship.tag = tag
            ship.update()

    def check_avaliable_placement (self, init_coordinate: tuple, ship_tag: str,
                                    direction: int) -> bool:
        # 0 = up, 1 = down, 2 = left, 3 = right
        coordinates = self.adjacent_coordinates(init_coordinate, ship_tag, direction)
        if direction == 0:
            if init_coordinate[0] - SHIP_SIZES[ship_tag] < 0:
                return False
            else:
                for coordinate in coordinates:
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 1:
            if init_coordinate[0] + SHIP_SIZES[ship_tag] > self.size:
                return False
            else:
                for coordinate in coordinates:
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 2:
            if init_coordinate[1] - SHIP_SIZES[ship_tag] < 0:
                return False
            else:
                for coordinate in coordinates:
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 3:
            if init_coordinate[1] + SHIP_SIZES[ship_tag] > self.size:
                return False
            else:
                for coordinate in coordinates:
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True

    def adjacent_coordinates (self, init_coordinate: tuple, ship_tag: str, 
                                direction: int) -> list:
        coordinates = [(init_coordinate)]
        if direction == 0:
            for i in range (1, SHIP_SIZES[ship_tag]):
                coordinates.append((init_coordinate[0] - i, init_coordinate[1]))
        elif direction == 1:
            for i in range (1, SHIP_SIZES[ship_tag]):
                coordinates.append((init_coordinate[0] + i, init_coordinate[1]))
        elif direction == 2:
            for i in range (1, SHIP_SIZES[ship_tag]):
                coordinates.append((init_coordinate[0], init_coordinate[1] - i))
        elif direction == 3:
            for i in range (1, SHIP_SIZES[ship_tag]):
                coordinates.append((init_coordinate[0], init_coordinate[1] + i))

        return coordinates