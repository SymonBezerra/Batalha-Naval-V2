import pygame

SHIP_TAGS = {"R": "Carrier", "B": "Battleship",
            "C": "Cruiser", "D": "Destroyer", "N": "Miss"}
SHIP_SIZES = {"R": 5, "B": 4, "C": 3, "D": 2, "N": 0}
class Ship(pygame.sprite.Sprite):
    def __init__(self, type: str, coordinate: tuple):
        super(Ship, self).__init__()
        self.tag = SHIP_TAGS[type]
        self.size = SHIP_SIZES[type]
        self.coordinate = coordinate

        self.hit = False
        self.color = (255, 255, 255) # default white
        
        def update_color (self) -> tuple:
            if self.hit and self.tag == "N":
                self.color (0, 0, 139)
            else:
                self.color (255, 69, 0)
        
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(self.color) # white as placeholder
        self.rect = self.surface.get_rect()
        self.image = pygame.image.load("sprites/miss_square.png")
        self.image = pygame.transform.scale(self.image, (35, 35))