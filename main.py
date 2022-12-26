import pygame
from pygame.locals import MOUSEBUTTONDOWN, K_SPACE, KEYDOWN
from ship import Ship
from player import Player
from cpu import CPU
from board import Board
from random import randint

BOARD_SIZE = 10
game_screen = pygame.display.set_mode([1200, 800])
pygame.display.set_caption("Batalha Naval")
BACKGROUND = pygame.image.load("gfx/background.png").convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (1200, 800))
COL_COORDS = pygame.image.load("gfx/col_coords.png").convert_alpha()
LINE_COORDS = pygame.image.load("gfx/line_coords.png").convert_alpha()
GAME_TITLE =  pygame.image.load("gfx/game_title.png").convert_alpha()

START_BUTTON = pygame.image.load("gfx/button_start.png")
START_BUTTON = pygame.transform.scale(START_BUTTON, (150, 150))

HOWTO_BUTTON = pygame.image.load("gfx/button_howtoplay.png")
HOWTO_BUTTON = pygame.transform.scale(HOWTO_BUTTON, (150, 150))

EXIT_BUTTON = pygame.image.load("gfx/button_exit.png")
EXIT_BUTTON = pygame.transform.scale(EXIT_BUTTON, (150, 150))

# loading and rescaling arrow sprites (for board positioning)
arrow_up = pygame.image.load("gfx/arrow_up.png").convert_alpha()
arrow_up = pygame.transform.scale(arrow_up, (75,75))

arrow_down = pygame.image.load("gfx/arrow_down.png").convert_alpha()
arrow_down = pygame.transform.scale(arrow_down, (75,75))

arrow_left = pygame.image.load("gfx/arrow_left.png").convert_alpha()
arrow_left = pygame.transform.scale(arrow_left, (75,75))

arrow_right = pygame.image.load("gfx/arrow_right.png").convert_alpha()
arrow_right = pygame.transform.scale(arrow_right, (75,75))

ARROW_DIRECTIONS = (arrow_left, arrow_right, arrow_up, arrow_down)

# button sprites (and different scales)
next_ship_button = pygame.image.load("gfx/button_sprite.png")
next_ship_button = pygame.transform.scale(next_ship_button, (250, 100))
next_ship_button_rect = next_ship_button.get_rect(center=(310,620))
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

def place_ship(board: Board, ship_tag: str, init_coordinate: tuple, direction: int) -> True:
    # set ship on place
    valid_placement = board.check_avaliable_placement(init_coordinate, ship_tag, direction)
    if valid_placement:
        ship_coordinates = board.adjacent_coordinates(init_coordinate, ship_tag, direction)
        for coordinate in ship_coordinates:
            ship: Ship = board.fleet_objects[coordinate[0]][coordinate[1]]
            ship.tag = ship_tag
            ship.update_sprite()

            ship_collision_blocks: list
            if coordinate == ship_coordinates[0]:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                ship_tag, direction, True, False)
            elif coordinate == ship_coordinates[len(ship_coordinates) - 1]:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                ship_tag, direction, False, True)
            else:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                ship_tag, direction, False, False)
            
            for collision_block in ship_collision_blocks:
                ship_cblock: Ship = board.fleet_objects[collision_block[0]][collision_block[1]]
                ship_cblock.tag = "O" # collision block tag
                # ship_cblock.show_collision_block = True # debug
                ship_cblock.update_sprite()

            # if manual_input: ship.hit = True # debug
        
        return True

    else: return False

def auto_place_ships(board: Board, ships: list) -> None:
    ship_in_place = 0
    while ship_in_place < len(ships):
        valid_place = place_ship(board, ships[ship_in_place], 
                                (randint(0,8), randint(0,8)), (randint(0,3)))
        if valid_place: ship_in_place += 1

# game objects 

game_player = Player(BOARD_SIZE, "Player")
game_cpu = CPU(BOARD_SIZE, "CPU")

if __name__ == "__main__":
    pygame.init()
    
    GAME_FONT = pygame.font.Font("gfx/Cascadia.ttf", 25)

    GAME_SHIPS = ["D", "D", "C", "C", "B", "R"]
    next_ship = 0

    game_tick = 0

    running = True
    start_menu = True
    game_on = False
    player_turn, cpu_turn = True, False # alternated = sea battle!
    placing_ships = True

    # placing_ships arrow sprite
    rotation_arrow = pygame.sprite.Sprite()
    rotation_arrow.image = ARROW_DIRECTIONS[game_player.board.rotation]

    # pygame.Sprite's for buttons
    start_button_sprite = pygame.sprite.Sprite()
    start_button_sprite.image = START_BUTTON
    start_button_sprite.rect = START_BUTTON.get_rect(center=(600,450))

    auto_place_ships(game_cpu.board, GAME_SHIPS)
    while running:
        # main menu will STUCK instead of switch loops
        while start_menu:
            game_screen.blit(BACKGROUND, (0,0))
            # game title
            game_screen.blit(GAME_TITLE, GAME_TITLE.get_rect(center=(600,250)))

            # buttons
            game_screen.blit(start_button_sprite.image, 
            start_button_sprite.rect)

            game_screen.blit(HOWTO_BUTTON, HOWTO_BUTTON.get_rect(center=(600,550)))

            game_screen.blit(EXIT_BUTTON, EXIT_BUTTON.get_rect(center=(600,650)))

            for event in pygame.event.get():
                if event == pygame.quit:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_sprite.rect.collidepoint(mouse_pos):
                        start_menu = False
            pygame.display.flip()
        
        # if not duplicated, the rotation arrow
        # will not update its image
        game_screen.blit(BACKGROUND, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN and game_on:
                pos = pygame.mouse.get_pos()
                ship_entity: Ship
                for ship_entity in [entity for entity
                                    in game_cpu.board.fleet_sprites
                                    if entity.rect.collidepoint(pos)]:
                        ship_entity.set_hit()
                        game_player.board.last_hit_coord = ship_entity.coordinate
                        game_player.board.last_hit_tag = ship_entity.tag
                        if ship_entity.tag in ("N", "O"):
                            player_turn, cpu_turn = False, True
                        else:
                            game_cpu.lives -= 1
            
            elif event.type == KEYDOWN and placing_ships:
                if event.key == K_SPACE:
                    game_player.board.rotate()
                    rotation_arrow.image = ARROW_DIRECTIONS[game_player.board.rotation]
            
            elif event.type == MOUSEBUTTONDOWN and placing_ships:
                pos = pygame.mouse.get_pos()
                for ship_entity in [entity for entity
                                    in game_player.board.fleet_sprites
                                    if entity.rect.collidepoint(pos)]:
                    valid_place = place_ship(game_player.board, GAME_SHIPS[next_ship], 
                                ship_entity.coordinate, game_player.board.rotation)
                    if valid_place: next_ship += 1
                    if next_ship == 6: placing_ships, game_on = False, True
        
        if cpu_turn and game_on:
            if game_tick != 0:
                pygame.time.delay(1000)
                cpu_aim = game_cpu.randomshot()
                cpu_target: Ship = game_player.board.fleet_objects[cpu_aim[0]][cpu_aim[1]]
                cpu_target.set_hit()
                if cpu_target.tag in ("N", "O"):
                    player_turn, cpu_turn = True, False
                else:
                    game_player.lives -= 1
                game_cpu.board.last_hit_coord = cpu_target.coordinate
                game_cpu.board.last_hit_tag = cpu_target.tag
                game_tick = 0
            else:
                game_tick += 1
            

        board_blit(game_player.board, game_screen)
        
        player_stats = GAME_FONT.render(game_player.board.stats, True, (0,0,0))
        game_screen.blit(player_stats, (game_player.board.init_pos[0] - 20,
                                        game_player.board.init_pos[1] - 100))
        board_blit(game_cpu.board, game_screen)

        cpu_stats = GAME_FONT.render(game_cpu.board.stats, True, (0,0,0))
        game_screen.blit(cpu_stats, (game_cpu.board.init_pos[0] - 20,
                                        game_cpu.board.init_pos[1] - 100))

        # board_rotation = GAME_FONT.render(str(game_player.board.rotation), True, (0,0,0))
        # game_screen.blit(board_rotation, (540, 500))

        if placing_ships:
            game_screen.blit(next_ship_button, next_ship_button_rect)
            game_screen.blit(GAME_FONT.render(f"Next ship is: {GAME_SHIPS[next_ship]}",
                            True, (0,0,0)), (200, 600))
            game_screen.blit(rotation_arrow.image,
            rotation_arrow.image.get_rect(center=(475,620)))

        if game_cpu.lives == 0 or game_player.lives == 0:
            game_on = False # game loop can be stopped
        
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()