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
        self.color = (0, 0, 139)

        @property
        def color (self) -> tuple:
            if not self.hit:
                return (255,255,255)
            elif self.hit and self.tag == "N":
                return (0,0,139)
            else:
                return (255,69,0)
        
        self.surface = pygame.Surface((20,20))
        self.surface.fill(self.color) # white as placeholder
        self.rect = self.surface.get_rect()