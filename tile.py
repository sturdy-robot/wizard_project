import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, color=None, image=None):
        super().__init__()
        if color is not None:
            self.image = pygame.Surface((size, size))
            self.image.fill(color)
        if image is not None:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
