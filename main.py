import pygame
from settings import *
from pygame.math import Vector2 as vector
import sys
from player import Player
from enemy import Enemy
from tile import CollisionTile, Tile
from pytmx.util_pygame import load_pygame


# TODO: Get Enemies

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # background

        # draw sprites with offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PokeClone')
        self.running = True
        self.clock = pygame.time.Clock()

        # load assets

        # sprite groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # sprite setup
        self.setup()

    def setup(self):
        tmx_map = load_pygame('./data/map.tmx')

        # collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('Collision').tiles():
            CollisionTile(
                (x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # non-collision tiles
        for layer in ['Ground', 'Ground_deco', 'Ground_hill', 'Fences', 'House_floors', 'House_walls', 'House_deco', 'Interaction']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * TILE_SIZE, y * TILE_SIZE), surf, LAYERS['Ground'],
                     self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Entity'):
            if obj.name == 'Player':
                self.player = Player(
                    (obj.x, obj.y), PATHS['player'], LAYERS['Entity'], self.collision_sprites, self.all_sprites)
            if obj.name == 'Enemy':
                Enemy((obj.x, obj.y), PATHS['enemy'], LAYERS['Entity'], [
                      self.all_sprites, self.collision_sprites])

    def run(self):
        # game loop
        while self.running:
            # event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # make sure program terminates
                    self.running = False
                    pygame.quit()
                    sys.exit()

            # delta time
            dt = self.clock.tick() / 1000
            # updates
            self.display_surface.fill('chartreuse4')
            self.all_sprites.update(dt)
            # draw
            self.all_sprites.custom_draw(self.player)
            # render
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
