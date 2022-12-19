import pygame

SHIP_TAGS = {"R": "Carrier", "B": "Battleship",
            "C": "Cruiser", "D": "Destroyer", "N": "Miss"}
SHIP_SIZES = {"R": 5, "B": 4, "C": 3, "D": 2, "N": 0}
class Ship(pygame.sprite.Sprite):
    def __init__(self, type: str, coordinate: tuple):
        super.__init__()
        self.name = SHIP_TAGS[type]
        self.size = SHIP_SIZES[type]
        self.coordinate = coordinate

        self.hit = False
        self.color = (255,255,255)

        # each ship will have its own surface
        self.surface = pygame.Surface((40,40))
        self.surface.fill(self.color) # white as placeholder
        self.rect = self.surface.get_rect()