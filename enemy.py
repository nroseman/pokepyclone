import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, path, layer, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = layer
