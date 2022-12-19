from player import Player
from cpu import CPU
class Board:
    def __init__ (self, size: int, player: Player, cpu: CPU):
        self.player_fleet = []
        self.cpu_fleet = []
        # these will work as the previous version's memories

