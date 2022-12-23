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

def place_ship(board: Board, ship_tag: str, init_coordinate: tuple, direction: int,
                manual_input: bool) -> True:
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
                                (randint(0,8), randint(0,8)), (randint(0,3)), False)
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
    game_on = False
    player_turn, cpu_turn = True, False # alternated = sea battle!
    placing_ships = True

    auto_place_ships(game_cpu.board, GAME_SHIPS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            
            elif event.type == MOUSEBUTTONDOWN and placing_ships:
                pos = pygame.mouse.get_pos()
                for ship_entity in [entity for entity
                                    in game_player.board.fleet_sprites
                                    if entity.rect.collidepoint(pos)]:
                    valid_place = place_ship(game_player.board, GAME_SHIPS[next_ship], 
                                ship_entity.coordinate, game_player.board.rotation, True)
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
            
         
        game_screen.blit(BACKGROUND, (0,0))

        board_blit(game_player.board, game_screen)
        
        player_stats = GAME_FONT.render(game_player.board.stats, True, (0,0,0))
        game_screen.blit(player_stats, (game_player.board.init_pos[0] - 20,
                                        game_player.board.init_pos[1] - 100))
        board_blit(game_cpu.board, game_screen)

        cpu_stats = GAME_FONT.render(game_cpu.board.stats, True, (0,0,0))
        game_screen.blit(cpu_stats, (game_cpu.board.init_pos[0] - 20,
                                        game_cpu.board.init_pos[1] - 100))

        board_rotation = GAME_FONT.render(str(game_player.board.rotation), True, (0,0,0))

        if placing_ships:
            game_screen.blit(GAME_FONT.render(f"Next ship is: {GAME_SHIPS[next_ship]}",
                            True, (0,0,0)), (540, 600))

        if game_cpu.lives == 0 or game_player.lives == 0:
            game_on = False # game loop can be stopped
        
        game_screen.blit(board_rotation, (540, 500))
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()