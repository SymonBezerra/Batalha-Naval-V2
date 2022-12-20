import pygame
from ship import Ship
from board import Board
game_screen = pygame.display.set_mode([1080, 720])
# clock = pygame.time.Clock()

def board_blit(board: Board, screen: pygame.Surface):
    for ship_entity in board.fleet:
            screen.blit(ship_entity.image,
            (board.init_pos[0] + (40 * ship_entity.coordinate[0]),
            board.init_pos[1] + (40 * ship_entity.coordinate[1])))
    

# game objects 
# ship = Ship("R")
player_board = Board(10, "player")
cpu_board = Board(10, "cpu")
if __name__ == "__main__":
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game_screen.fill((8, 143, 143))
        
        # black line in the middle of the screen
        pygame.draw.rect(game_screen, (0, 0, 0), (540, 0, 20, 720))
        
        board_blit(player_board, game_screen)
        board_blit(cpu_board, game_screen)

        pygame.display.flip()
    
    pygame.quit()