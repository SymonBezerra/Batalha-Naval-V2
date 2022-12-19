import pygame
from ship import Ship
from board import Board
game_screen = pygame.display.set_mode([800, 600])
# clock = pygame.time.Clock()

def board_blit(board: Board, screen: pygame.Surface, init_pos = (400, 300)):
    for ship_line in board.player_fleet:
        for ship_entity in ship_line:
            screen.blit(ship_entity,
            (init_pos[0] + 20 + (20 * ship_entity.coordinate[0]),
            init_pos[1] + 20 + (20 * ship_entity.coordinate[1])))
    

# game objects 
# ship = Ship("R")
board = Board(10)
if __name__ == "__main__":
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game_screen.fill((8, 143, 143))

        board_blit(board, game_screen)

        pygame.display.flip()
    
    pygame.quit()