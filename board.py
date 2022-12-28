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
        self.fleet_ships = []
        # for hits
        self.rotation = 0

        # for player\CPU stats
        self.last_hit_tag = "-"
        self.last_hit_coord = (10,10)

        self.init_pos = (0,0)
        if player_name == "Player": 
            self.init_pos = (200, 200)
        else: 
            self.init_pos = (700, 200)

    # def __board_test (self, fleet: pygame.sprite.Group):
    #     for i in range(self.size):
    #         for j in range (self.size):
    #             fleet.add(Ship("N", (i,j)))

    def check_destroyed_ships(self) -> tuple: # (bool, list of ship coords)
        ship: tuple
        # ship[0] = ship coordinates; ship[1] = collision blocks' coordinates;
        for ship in self.fleet_ships:
            ship_tags = []
            for cell in ship[0]:
                ship_tags.append(self.fleet_objects[cell[0]][cell[1]].tag)
            if ship_tags.count("H") == len(ship_tags):
                return (True, ship[1])
        
        return (False, [])

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

    def hide_all_ships (self) -> None:
        ship: Ship
        for ship in self.fleet_sprites:
            ship.hit = False
            ship.show_collision_block = False
    
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
    
        cblocks_coordinates = []
        # 0 = left, 1 = right, 2 = up, 3 = down
        if direction == 0:
            if first_ship and coordinate[0] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0] + 1, coordinate[1]))
            elif last_ship and coordinate[0] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0] - 1, coordinate[1]))
            if coordinate[1] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0], coordinate[1] - 1))
            if coordinate[1] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0], coordinate[1] + 1))
        elif direction == 1:
            if first_ship and coordinate[0] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0] - 1, coordinate[1]))
            elif last_ship and coordinate[0] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0] + 1, coordinate[1]))
            if coordinate[1] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0], coordinate[1] - 1))
            if coordinate[1] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0], coordinate[1] + 1))
        elif direction == 2:
            if first_ship and coordinate[1] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0], coordinate[1] + 1))
            elif last_ship and coordinate[1] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0], coordinate[1] - 1))
            if coordinate[0] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0] - 1, coordinate[1]))
            if coordinate[0] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0] + 1, coordinate[1]))
        elif direction == 3:
            if first_ship and coordinate[1] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0], coordinate[1] - 1))
            if last_ship and coordinate[1] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0], coordinate[1] + 1))
            if coordinate[0] - 1 >= 0:
                cblocks_coordinates.append((coordinate[0] - 1, coordinate[1]))
            if coordinate[0] + 1 < self.size:
                cblocks_coordinates.append((coordinate[0] + 1, coordinate[1]))
        return cblocks_coordinates