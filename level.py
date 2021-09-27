import pygame
from tile import Tile
from settings import tile_size
from player import Player
from background import Background
from powers import Power


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.background = pygame.sprite.GroupSingle(Background('assets/color_sky.png'))
        self.tiles = pygame.sprite.Group()
        self.power = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        self.setup(level_data)
        self.world_shift = 0
        self.world_shift_speed = 0

    def setup(self, level_data):
        map_data = self.read_map_data(level_data)
        for i, row in enumerate(map_data):
            for j, cell in enumerate(row):
                x = j * tile_size
                y = i * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size, image='assets/rockytile.png')
                    self.tiles.add(tile)
                if cell == 'P':
                    pl = Player((x, y), self)
                    self.player.add(pl)
                if cell == 'G':
                    tile = Tile((x, y), tile_size, image='assets/grasstile.png')
                    self.tiles.add(tile)

    @staticmethod
    def read_map_data(layout):
        with open(layout, 'r', encoding='utf-8') as fp:
            data = fp.read().splitlines()
        return data

    def run(self):
        self.background.draw(self.display_surface)

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.player.draw(self.display_surface)

        if self.player.sprite.shoot:
            power = Power(
                (self.player.sprite.rect.centerx,
                 self.player.sprite.rect.centery - 8),
                damage=10,
                direction=self.player.sprite.direction,
                player_facing_right=self.player.sprite.facing_right,
                image='assets/beam.png'
            )
            self.power.add(power)
            self.player.sprite.shoot = False

        self.power.update(self.world_shift)
        self.power.draw(self.display_surface)

