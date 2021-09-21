import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        # Player status
        self.status = 'idle'
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 1
        self.jump_speed = -22

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def jump(self):
        self.direction.y += self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
