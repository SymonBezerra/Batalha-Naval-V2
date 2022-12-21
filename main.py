import pygame
from pygame.locals import MOUSEBUTTONDOWN, K_SPACE, KEYDOWN
from ship import Ship
from player import Player
from cpu import CPU
from board import Board

BOARD_SIZE = 10
game_screen = pygame.display.set_mode([1080, 720])
pygame.display.set_caption("Batalha Naval")
BACKGROUND = pygame.image.load("gfx/background.png").convert()
COL_COORDS = pygame.image.load("gfx/col_coords.png").convert_alpha()
LINE_COORDS = pygame.image.load("gfx/line_coords.png").convert_alpha()
# not used for this version
clock = pygame.time.Clock()

# game loop functions 
def board_blit(board: Board, screen: pygame.Surface):
    # for printing the board
    ship_entity: Ship
    for ship_entity in board.fleet_sprites:
        ship_pos = (board.init_pos[0] + (40 * ship_entity.coordinate[0]),
        board.init_pos[1] + (40 * ship_entity.coordinate[1]))
        ship_entity.update_sprite()
        ship_entity.rect = ship_entity.image.get_rect(center=ship_pos)
        screen.blit(ship_entity.image, ship_entity.rect)
    
    screen.blit(COL_COORDS, (board.init_pos[0] - 20, board.init_pos[1] - 60))
    screen.blit(LINE_COORDS, (board.init_pos[0] - 65, board.init_pos[1] - 20))

def place_ship(board: Board, ship_tag: str, init_coordinate: tuple, direction: int) -> None:
    # set ship on place
    valid_placement = board.check_avaliable_placement(init_coordinate, ship_tag, direction)
    if valid_placement:
        ship_coordinates = board.adjacent_coordinates(init_coordinate, ship_tag, direction)
        for coordinate in ship_coordinates:
            ship: Ship = board.fleet_objects[coordinate[0]][coordinate[1]]
            ship.tag = ship_tag

            # ship.hit = True # debug


# game objects 

game_player = Player(BOARD_SIZE, "Player")
game_cpu = CPU(BOARD_SIZE, "CPU")

if __name__ == "__main__":
    pygame.init()
    GAME_FONT = pygame.font.Font("gfx/Cascadia.ttf", 25)

    running = True
    player_turn = False
    placing_ships = True

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and player_turn:
                pos = pygame.mouse.get_pos()
                ship_entity: Ship
                for ship_entity in [entity for entity
                                    in game_cpu.board.fleet_sprites
                                    if entity.rect.collidepoint(pos)]:
                        ship_entity.set_hit()
                        # print("HIT")
            
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_player.board.rotate()
            
            elif event.type == MOUSEBUTTONDOWN and placing_ships:
                pos = pygame.mouse.get_pos()
                for ship_entity in [entity for entity
                                    in game_player.board.fleet_sprites
                                    if entity.rect.collidepoint(pos)]:
                    place_ship(game_player.board, "C", 
                    ship_entity.coordinate,
                    game_player.board.rotation)
                    ship_entity.update_sprite()
         
        game_screen.blit(BACKGROUND, (0,0))
        # pygame.draw.rect(game_screen, (0, 0, 0), (540, 0, 20, 720))
        board_blit(game_player.board, game_screen)
        
        player_stats = GAME_FONT.render(game_player.board.stats, False, (0,0,0))
        game_screen.blit(player_stats, (game_player.board.init_pos[0] - 20,
                                        game_player.board.init_pos[1] - 100))
        board_blit(game_cpu.board, game_screen)

        cpu_stats = GAME_FONT.render(game_cpu.board.stats, False, (0,0,0))
        game_screen.blit(cpu_stats, (game_cpu.board.init_pos[0] - 20,
                                        game_cpu.board.init_pos[1] - 100))
        pygame.display.flip()
    
    pygame.quit()