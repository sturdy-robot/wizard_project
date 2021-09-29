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
                    tile = Tile((x, y), tile_size, image='assets/sprite_1.png')
                    self.tiles.add(tile)
                elif cell == 'P':
                    pl = Player((x, y), self)
                    self.player.add(pl)
                elif cell == 'G':
                    tile = Tile((x, y), tile_size, image='assets/sprite_0.png')
                    self.tiles.add(tile)

    @staticmethod
    def read_map_data(layout):
        with open(layout, 'r', encoding='utf-8') as fp:
            data = fp.read().splitlines()
        return data

    def create_player_powers(self, damage, scale):
        return Power(
            (self.player.sprite.rect.centerx,
             self.player.sprite.rect.centery - 8),
            damage=damage,
            direction=self.player.sprite.direction,
            player_facing_right=self.player.sprite.facing_right,
            image='assets/beam.png',
            scale=scale
        )

    def check_player_powers(self):
        if self.player.sprite.shoot_small_beam:
            power = self.create_player_powers(10, 1)
            self.power.add(power)
            self.player.sprite.shoot_small_beam = False

        if self.player.sprite.shoot_medium_beam:
            power = self.create_player_powers(50, 2)
            self.power.add(power)
            self.player.sprite.shoot_medium_beam = False

        if self.player.sprite.shoot_big_beam:
            power = self.create_player_powers(100, 4)
            self.power.add(power)
            self.player.sprite.shoot_big_beam = False

        if self.player.sprite.shoot_enormous_beam:
            power = self.create_player_powers(250, 6)
            self.power.add(power)
            self.player.sprite.shoot_enormous_beam = False

        if self.player.sprite.shoot_absurd_beam:
            power = self.create_player_powers(500, 10)
            self.power.add(power)
            self.player.sprite.shoot_absurd_beam = False

    def run(self, dt):
        self.background.draw(self.display_surface)

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.update(dt)
        self.player.draw(self.display_surface)
        self.check_player_powers()
        self.power.update(self.world_shift, dt)
        self.power.draw(self.display_surface)

