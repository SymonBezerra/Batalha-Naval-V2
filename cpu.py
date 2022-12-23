from player import Player
from random import randint
import pygame
class CPU(Player):
    def __init__ (self, size: int, name: str):
        super().__init__(size, name)
        self.size = size
        self.name = name
        self.remaining_shots = []
        for i in range(self.size):
            for j in range(self.size):
                self.remaining_shots.append((i,j))

    def randomshot (self):
        return self.remaining_shots.pop(randint(0, len(self.remaining_shots) - 1))