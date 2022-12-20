import pygame
from ship import Ship
from board import Board
game_screen = pygame.display.set_mode([1080, 720])
# clock = pygame.time.Clock()

def board_blit(board: Board, screen: pygame.Surface, placement: str):
    # 630 + 400 = 1030 => 50 
    if placement == "cpu":
        init_pos = (630, 160)
    if placement == "player":
        init_pos = (50, 160)
    for ship_entity in board.player_fleet:
            screen.blit(ship_entity.image,
            (init_pos[0] + (40 * ship_entity.coordinate[0]),
            init_pos[1] + (40 * ship_entity.coordinate[1])))
    

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
        
        # black line in the middle of the screen
        pygame.draw.rect(game_screen, (0, 0, 0), (540, 0, 20, 720))
        
        board_blit(board, game_screen, "cpu")
        board_blit(board, game_screen, "player")

        pygame.display.flip()
    
    pygame.quit()