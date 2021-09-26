import pygame
from tile import Tile
from settings import tile_size, screen_width
from player import Player


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        self.setup(level_data)
        self.world_shift = 0
        self.world_shift_speed = 5

    def setup(self, level_data):
        map_data = self.read_map_data(level_data)
        for i, row in enumerate(map_data):
            for j, cell in enumerate(row):
                x = j * tile_size
                y = i * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size, (229, 229, 229))
                    self.tiles.add(tile)
                if cell == 'P':
                    pl = Player((x, y), self)
                    self.player.add(pl)
                if cell == 'G':
                    tile = Tile((x, y), tile_size, (0, 229, 0))
                    self.tiles.add(tile)

    @staticmethod
    def read_map_data(layout):
        with open(layout, 'r', encoding='utf-8') as fp:
            data = fp.read().splitlines()
        return data

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 2.8 and direction_x < 0:
            self.world_shift = self.world_shift_speed
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2.8) and direction_x > 0:
            self.world_shift = -self.world_shift_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = self.world_shift_speed

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
