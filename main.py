import pygame
from ship import Ship
screen = pygame.display.set_mode([800, 600])
# clock = pygame.time.Clock()


# game objects 
ship = Ship("R")
if __name__ == "__main__":
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 128))

        screen.blit(ship.surface, (400,300))

        pygame.display.flip()
    
    pygame.quit()