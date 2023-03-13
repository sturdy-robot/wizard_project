import pygame
from settings import screen_width, screen_height
from powers import Power


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        super().__init__()
        # self.image = pygame.Surface((32, 64))
        # self.image.fill((255, 0, 0))

        self.original_image = pygame.image.load('assets/character_sprite.png').convert_alpha()
        # size_x, size_y = self.original_image.get_size()
        # self.original_image = pygame.transform.scale(self.original_image, (size_x*3, size_y*2))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

        # Player attributes
        self.hp = 100
        self.mana = 100

        # Get level data
        self.level = level

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = 6
        self.speed = self.player_speed
        self.gravity = 1
        self.jump_speed = -22

        # Player shooting powers
        self.shoot_small_beam = False
        self.shoot_medium_beam = False
        self.shoot_big_beam = False
        self.shoot_enormous_beam = False
        self.shoot_absurd_beam = False
        # self.collision_rect = pygame.Rect(self.rect.topleft, (10, self.rect.height))

    def animate(self):
        if self.facing_right:
            self.image = self.original_image
            # self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.image = flipped_image
            # self.rect.bottomright = self.collision_rect.bottomright

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def vertical_movement_collision(self, dt):
        self.apply_gravity(dt)

        for sprite in self.level.tiles.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True

        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0.1:
            self.on_ceiling = False

    def horizontal_movement_collision(self):
        self.rect.x += self.direction.x * self.speed

        for sprite in self.level.tiles.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = self.rect.left
                elif self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = self.rect.right

        if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
            self.on_left = False
        if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
            self.on_right = False

    def get_input(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump(dt)

        if keys[pygame.K_z]:
            self.shoot_small_beam = True
        elif keys[pygame.K_x]:
            self.shoot_medium_beam = True
        elif keys[pygame.K_c]:
            self.shoot_big_beam = True
        elif keys[pygame.K_v]:
            self.shoot_enormous_beam = True
        elif keys[pygame.K_b]:
            self.shoot_absurd_beam = True

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y * dt

    def get_player_on_ground(self):
        self.level.player_on_ground = bool(self.on_ground)

    def scroll_x(self, dt):
        player = self
        player_x = player.rect.centerx
        direction_x = player.direction.x
        self.level.world_shift_speed = self.player_speed * dt

        if player_x < screen_width / 2.8 and direction_x < 0:
            self.level.world_shift = self.level.world_shift_speed
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2.8) and direction_x > 0:
            self.level.world_shift = -self.level.world_shift_speed
            player.speed = 0
        else:
            self.level.world_shift = 0
            player.speed = self.level.world_shift_speed

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            self.status = 'run' if self.direction.x != 0 else 'idle'

    def jump(self, dt):
        self.direction.y += self.jump_speed

    def update(self, dt):
        self.scroll_x(dt)
        self.get_input(dt)
        self.get_status()
        self.horizontal_movement_collision()
        self.vertical_movement_collision(dt)
        self.animate()
        self.rect.x += self.direction.x * self.speed * dt
