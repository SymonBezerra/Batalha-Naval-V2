import pygame

SHIP_TAGS = {"R": "Carrier", "B": "Battleship",
            "C": "Cruiser", "D": "Destroyer", "N": "Miss", "O": "Miss"}
SHIP_SIZES = {"R": 5, "B": 4, "C": 3, "D": 2, "N": 0, "O": 0}
class Ship(pygame.sprite.Sprite):
    def __init__(self, tag: str, coordinate: tuple):
        super(Ship, self).__init__()
        self.tag = tag
        self.name = SHIP_TAGS[tag] 
        self.coordinate = coordinate

        self.hit = False
        self.show_collision_block = False

        # self.surface = pygame.Surface((20,20))
        self.image = pygame.image.load("sprites/closed_square.png").convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (35, 35))
        
    def update_sprite (self) -> None:

        if self.hit and self.tag in ("M", "O"):
            self.image = pygame.image.load("sprites/miss_square.png").convert()
        elif self.hit and self.tag in ("R", "C", "B", "D"):
            self.image = pygame.image.load("sprites/hit_square.png").convert()
        elif self.show_collision_block and self.tag == "O":
            self.image = pygame.image.load("sprites/collision_block_square.png").convert()
        
        self.image = pygame.transform.scale(self.image, (35, 35))