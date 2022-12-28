import pygame
from pygame.locals import MOUSEBUTTONDOWN, K_SPACE, KEYDOWN
from ship import Ship
from player import Player
from cpu import CPU
from board import Board
from random import randint

# framerate and sfx
mixer = pygame.mixer.init()
clock = pygame.time.Clock()

BOARD_SIZE = 10
game_screen = pygame.display.set_mode([1200, 800])
pygame.display.set_caption("Batalha Naval")
BACKGROUND = pygame.image.load("gfx/background.png").convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (1200, 800))
COL_COORDS = pygame.image.load("gfx/col_coords.png").convert_alpha()
LINE_COORDS = pygame.image.load("gfx/line_coords.png").convert_alpha()
GAME_TITLE =  pygame.image.load("gfx/game_title.png").convert_alpha()
INSTRUCTIONS_TEXT = pygame.image.load("gfx/instructions_text.png").convert_alpha()

START_BUTTON = pygame.image.load("gfx/button_start.png")
START_BUTTON = pygame.transform.scale(START_BUTTON, (150, 150))

HOWTO_BUTTON = pygame.image.load("gfx/button_howtoplay.png")
HOWTO_BUTTON = pygame.transform.scale(HOWTO_BUTTON, (150, 150))

EXIT_BUTTON = pygame.image.load("gfx/button_exit.png")
EXIT_BUTTON = pygame.transform.scale(EXIT_BUTTON, (150, 150))

RETURNTOTITLE_BUTTON = pygame.image.load("gfx/button_returntotitle.png")
RETURNTOTITLE_BUTTON = pygame.transform.scale(RETURNTOTITLE_BUTTON, (150, 150))

TITLE_SONG = pygame.mixer.music.load("sfx/sound_track/TITLE_SONG.wav")

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

# loading sfx tracks
sfx_button = pygame.mixer.Sound("sfx/button_select.wav")
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

            ship_collision_blocks = []
            if coordinate == ship_coordinates[0]:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                direction, True, False)
            elif coordinate == ship_coordinates[len(ship_coordinates) - 1]:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                direction, False, True)
            else:
                ship_collision_blocks = board.check_collision_blocks(coordinate,
                direction, False, False)
            
            for collision_block in ship_collision_blocks:
                ship_cblock: Ship = board.fleet_objects[collision_block[0]][collision_block[1]]
                ship_cblock.tag = "O" # collision block tag
                # ship_cblock.show_collision_block = True # debug
                ship_cblock.update_sprite()
        
            # ship.hit = True # debug
        # now I need a way to store the ship's COORDINATES into a memory
        # + check its collision blocks
        board.fleet_ships.append(ship_coordinates)

        
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
    instructions_screen = False
    game_on = False
    player_turn, cpu_turn = True, False # alternated = sea battle!
    placing_ships = True

    # destroyed ships
    cpu_destroyed_ships = []
    player_destroyed_ships = []
    destroyed_ship_frame = 0

    # placing_ships arrow sprite
    rotation_arrow = pygame.sprite.Sprite()
    rotation_arrow.image = ARROW_DIRECTIONS[game_player.board.rotation]

    # pygame.Sprite's for buttons
    start_button_sprite = pygame.sprite.Sprite()
    start_button_sprite.image = START_BUTTON
    start_button_sprite.rect = START_BUTTON.get_rect(center=(600,450))

    instructions_button_sprite = pygame.sprite.Sprite()
    instructions_button_sprite.image = HOWTO_BUTTON
    instructions_button_sprite.rect = HOWTO_BUTTON.get_rect(center=(600,550))

    exit_button_sprite = pygame.sprite.Sprite()
    exit_button_sprite.image = EXIT_BUTTON
    exit_button_sprite.rect = EXIT_BUTTON.get_rect(center=(600,650))

    returntotitle_button_sprite = pygame.sprite.Sprite()
    returntotitle_button_sprite.image = RETURNTOTITLE_BUTTON
    returntotitle_button_sprite.rect = RETURNTOTITLE_BUTTON.get_rect(center=(310,620))

    pygame.mixer.music.play(-1)
    auto_place_ships(game_cpu.board, GAME_SHIPS)
    while running:
        pygame.mixer.music.set_volume(0.5)
        # main menu will STUCK instead of switch loops
        while start_menu:
            pygame.mixer.music.set_volume(1.0)
            # title screen
            if not instructions_screen:
                game_screen.blit(BACKGROUND, (0,0))
                # game title
                game_screen.blit(GAME_TITLE, GAME_TITLE.get_rect(center=(600,250)))

                # buttons
                game_screen.blit(start_button_sprite.image, 
                start_button_sprite.rect)

                game_screen.blit(instructions_button_sprite.image, 
                instructions_button_sprite.rect)

                game_screen.blit(exit_button_sprite.image, exit_button_sprite.rect)

            # game instructions
            else:
                game_screen.blit(BACKGROUND, (0,0))
                game_screen.blit(INSTRUCTIONS_TEXT, (0,0))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not instructions_screen and start_button_sprite.rect.collidepoint(mouse_pos):
                        start_menu = False
                        pygame.mixer.Sound.play(sfx_button)
                    elif not instructions_screen and instructions_button_sprite.rect.collidepoint(mouse_pos):
                        instructions_screen = True
                    elif not instructions_screen and exit_button_sprite.rect.collidepoint(mouse_pos):
                        start_menu = False
                        running = False
                    elif instructions_screen:
                        instructions_screen = False
            pygame.display.flip()
        
        # here starts the game loop

        # if not duplicated, the rotation arrow
        # will not update its image
        game_screen.blit(BACKGROUND, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game_on and player_turn:
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
                elif placing_ships:
                    for ship_entity in [entity for entity
                                        in game_player.board.fleet_sprites
                                        if entity.rect.collidepoint(pos)]:
                        valid_place = place_ship(game_player.board, GAME_SHIPS[next_ship], 
                                    ship_entity.coordinate, game_player.board.rotation)
                        if valid_place: next_ship += 1
                        if next_ship == 6: placing_ships, game_on = False, True
                
                elif not game_on:
                    if returntotitle_button_sprite.rect.collidepoint(pos):
                        start_menu = True
                        game_player.reset_board()
                        game_cpu.reset_board()
                        player_turn, cpu_turn = True, False
                        placing_ships = True

            
            elif event.type == KEYDOWN and placing_ships:
                if event.key == K_SPACE:
                    game_player.board.rotate()
                    rotation_arrow.image = ARROW_DIRECTIONS[game_player.board.rotation]
        
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
            

        # displaying the boards 
        board_blit(game_player.board, game_screen)
        board_blit(game_cpu.board, game_screen)

        # text display above the board
        if game_cpu.lives == 0:
            game_on = False
            player_display = "Player wins the game =D"
            cpu_display = "You're the Sea Master!"
        else:
            player_display = game_player.board.stats
        
        if game_player.lives == 0:
            game_on = False
            player_display = "CPU wins the game!"
            cpu_display = "Better luck next time =("
        else:
            cpu_display = game_cpu.board.stats
        
        player_stats = GAME_FONT.render(player_display, True, (0,0,0))
        game_screen.blit(player_stats, (game_player.board.init_pos[0] - 20,
                                        game_player.board.init_pos[1] - 100))

        cpu_stats = GAME_FONT.render(cpu_display, True, (0,0,0))
        game_screen.blit(cpu_stats, (game_cpu.board.init_pos[0] - 20,
                                        game_cpu.board.init_pos[1] - 100))

        if placing_ships:
            game_screen.blit(next_ship_button, next_ship_button_rect)
            game_screen.blit(GAME_FONT.render(f"Next ship is: {GAME_SHIPS[next_ship]}",
                            True, (0,0,0)), (200, 600))
            game_screen.blit(rotation_arrow.image,
            rotation_arrow.image.get_rect(center=(475,620)))
        
        # display return to title button
        if game_on == False and (game_player.lives == 0 or game_cpu.lives == 0):
            game_screen.blit(returntotitle_button_sprite.image,
            returntotitle_button_sprite.rect)
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()