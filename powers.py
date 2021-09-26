import pygame


class Power(pygame.sprite.Sprite):
    def __init__(self, pos, damage, color=(189, 76, 91)):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

        self.damage = damage
        self.speed = 10
        self.direction = pygame.math.Vector2(0, 0)

    def shoot_power(self, direction: pygame.math.Vector2):
        self.direction.x = direction.x
        self.direction.y = direction.y

