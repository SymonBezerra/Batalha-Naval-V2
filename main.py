import pygame
from ship import Ship
from player import Player
from cpu import CPU
from board import Board

BOARD_SIZE = 10 
game_screen = pygame.display.set_mode([1080, 720])
# clock = pygame.time.Clock()

# game loop functions 
def board_blit(board: Board, screen: pygame.Surface):
    # for printing the board
    ship_entity: Ship
    for ship_entity in board.fleet_sprites:
        ship_entity.update_sprite()
        screen.blit(ship_entity.image,
        (board.init_pos[0] + (40 * ship_entity.coordinate[0]),
        board.init_pos[1] + (40 * ship_entity.coordinate[1])),
        ship_entity.rect)

def place_ship(board: Board, ship_tag: str, init_coordinate: tuple, direction: int) -> None:
    # set ship on place
    valid_placement = board.check_avaliable_placement(init_coordinate, ship_tag, direction)
    if valid_placement:
        ship_coordinates = board.adjacent_coordinates(init_coordinate, ship_tag, direction)
        for coordinate in ship_coordinates:
            ship: Ship = board.fleet_objects[coordinate[0]][coordinate[1]]
            ship.tag = "M"

            # debug
            ship.hit = True



# game objects 

game_player = Player(BOARD_SIZE)
game_cpu = CPU(BOARD_SIZE)

place_ship(game_player.board, "C", (0,0), 1)

if __name__ == "__main__":
    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
         
        game_screen.fill((8, 143, 143))
        pygame.draw.rect(game_screen, (0, 0, 0), (540, 0, 20, 720))
        board_blit(game_player.board, game_screen)
        board_blit(game_cpu.board, game_screen)
        pygame.display.update()
    
    pygame.quit()