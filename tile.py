import pygame
from settings import *
from pygame.math import Vector2 as vector


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, layer, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = layer

class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, LAYERS['Collision'], groups)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Collision']
