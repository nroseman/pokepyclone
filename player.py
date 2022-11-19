import pygame
from support import import_file_dict
from pygame.math import Vector2 as vector
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, path, layer, collision_sprites, groups):
        super().__init__(groups)
        self.animations = import_file_dict(path)
        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Entity']
        self.hitbox = self.rect.copy().inflate(-126, -70)

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 300

        # collisions
        self.collision_sprites = collision_sprites

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_DOWN]:
            self.status = 'down'
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.status = 'up'
            self.direction.y = -1
        else:
            self.direction.y = 0

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':

            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.rect.right
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.rect.left
                    self.pos.x = self.hitbox.centerx
                    self.rect.centerx = self.hitbox.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.rect.top
                    self.pos.y = self.hitbox.centery
                    self.rect.centery = self.hitbox.centery

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_status()

        self.animate(dt)
