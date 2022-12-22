from ship import Ship, SHIP_SIZES, SHIP_TAGS
import pygame

TOP_COORDINATES = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E",
                    5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
class Board:

    def __init__ (self, size: int, player_name: str):
        self.player_name = player_name
        self.size = size
        self.fleet_sprites = pygame.sprite.Group()
        # for drawing
        self.fleet_objects = []
        # for hits
        self.rotation = 0

        # for player\CPU stats
        self.last_hit_tag = "-"
        self.last_hit_coord = (10,10)

        self.init_pos = (0,0)
        if player_name == "Player": 
            self.init_pos = (100, 200)
        else: 
            self.init_pos = (630, 200)

    # def __board_test (self, fleet: pygame.sprite.Group):
    #     for i in range(self.size):
    #         for j in range (self.size):
    #             fleet.add(Ship("N", (i,j)))

    @property
    def stats (self) -> str:
        tag: str
        if self.last_hit_tag == "-":
            tag = self.last_hit_tag
        else:
            tag = SHIP_TAGS[self.last_hit_tag]
        
        coordinate: str
        if self.last_hit_coord == (10,10):
            coordinate = f"--"
        else:
            coordinate = f"{TOP_COORDINATES[self.last_hit_coord[0]]}{self.last_hit_coord[1] + 1}"
        
        return f"{self.player_name} Last shot: {coordinate}, {tag}"

    def set_ships_tag(self, coordinates: list, tag: str) -> None:
        for coordinate in coordinates:
            ship: Ship = self.fleet_objects[coordinate[0]][coordinate[1]]
            ship.tag = tag
            ship.update()
    
    def rotate (self) -> None:
        if self.rotation < 3: self.rotation += 1
        else: self.rotation = 0
        # print(self.rotation)

    def check_avaliable_placement (self, init_coordinate: tuple, ship_tag: str,
                                    direction: int) -> bool:
        # 0 =left, 1 = right, 2 = up, 3 = down
        coordinates = self.adjacent_coordinates(init_coordinate, ship_tag, direction)
        if direction == 0:
            if init_coordinate[0] + 1 - SHIP_SIZES[ship_tag] < 0:
                return False
            else:
                for coordinate in coordinates:
                    ship: Ship
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 1:
            if init_coordinate[0] + 1 + SHIP_SIZES[ship_tag] > self.size + 1:
                return False
            else:
                for coordinate in coordinates:
                    ship: Ship
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 2:
            if init_coordinate[1] + 1 - SHIP_SIZES[ship_tag] < 0:
                return False
            else:
                for coordinate in coordinates:
                    ship: Ship
                    ship = self.fleet_objects[coordinate[0]][coordinate[1]]
                    if ship.tag != "N":
                        return False
            return True
        
        elif direction == 3:
            if init_coordinate[1] + 1 + SHIP_SIZES[ship_tag] > self.size + 1:
                return False
            else:
                for coordinate in coordinates:
                    ship: Ship
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

    
    def check_collision_blocks (self, coordinate, ship_tag: str, 
                                direction: int, first_ship: bool, 
                                last_ship: bool) -> list:
        
        # 0 = left, 1 = right, 2 = up, 3 = down
        if direction == 0:
            if first_ship and coordinate[0] + 1 <= self.size:
                return [(coordinate[0] + 1, coordinate[1]),
                        (coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
            elif last_ship and coordinate[0] - 1 >= 0:
                return [(coordinate[0] - 1, coordinate[1]),
                        (coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
            else:
                return [(coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
        elif direction == 1:
            if first_ship and coordinate[0] - 1 >= 0:
                return [(coordinate[0] - 1, coordinate[1]),
                        (coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
            elif last_ship and coordinate[0] + 1 <= self.size:
                return [(coordinate[0] + 1, coordinate[1]),
                        (coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
            else:
                return [(coordinate[0], coordinate[1] - 1),
                        (coordinate[0], coordinate[1] + 1)]
        elif direction == 2:
            if first_ship and coordinate[1] + 1 <= self.size:
                return [(coordinate[0], coordinate[1] - 1),
                        (coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]
            elif last_ship and coordinate[1] - 1 >= 0:
                return [(coordinate[0], coordinate[1] + 1),
                        (coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]
            else:
                return [(coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]
        elif direction == 3:
            if first_ship and coordinate[1] - 1 >= 0:
                return [(coordinate[0], coordinate[1] - 1),
                        (coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]
            elif last_ship and coordinate[1] + 1 <= self.size:
                return [(coordinate[0], coordinate[1] + 1),
                        (coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]
            else:
                return [(coordinate[0] - 1, coordinate[1]),
                        (coordinate[0] + 1, coordinate[1])]