import pygame
from settings import screen_width


class Power(pygame.sprite.Sprite):
    def __init__(self, pos, damage, direction, player_facing_right, color=None, image=None):
        super().__init__()
        if color is not None:
            self.image = pygame.Surface((32, 8))
            self.image.fill(color)
        if image is not None:
            self.original_image = pygame.image.load(image).convert_alpha()
            self.image = self.original_image

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.damage = damage
        self.speed = 20
        self.direction = pygame.math.Vector2(0, 0)
        self.direction.x = direction.x
        self.direction.y = direction.y
        self.facing_right = player_facing_right

    def update(self, world_shift):
        if self.facing_right is True:
            self.direction.x = 1
            self.image = self.original_image
        else:
            self.direction.x = -1
            flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.image = flipped_image

        self.rect.x += (self.speed * self.direction.x)

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
