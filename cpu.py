from player import Player
from random import randint
import pygame
class CPU(Player):
    def __init__ (self, size: int, name: str):
        super().__init__(size, name)

    def randomshot (self):
        return (randint(0,8), randint(0,8))