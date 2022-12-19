import pygame
screen = pygame.display.set_mode([1080, 720])
# clock = pygame.time.Clock()

if __name__ == "__main__":
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255,255,255))

        pygame.draw.circle(screen, (0,0,0), (250, 250), 50)

        pygame.display.flip()
    
    pygame.quit()