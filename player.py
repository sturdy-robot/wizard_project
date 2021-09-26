import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, level):
        super().__init__()
        # self.image = pygame.Surface((32, 64))
        # self.image.fill((255, 0, 0))

        self.original_image = pygame.image.load('assets/charactersprite.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

        # Player attributes
        self.hp = 100
        self.mana = 100

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 1
        self.jump_speed = -22
        self.collision_rect = pygame.Rect(self.rect.topleft, (10, self.rect.height))

    def animate(self):
        if self.facing_right:
            self.image = self.original_image
            #self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.image = flipped_image
            #self.rect.bottomright = self.collision_rect.bottomright

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
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
            self.jump()

        if keys[pygame.K_x]:
            self.use_power()

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

    def use_power(self):
        print("Using power")

    def jump(self):
        self.direction.y += self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.rect.x += self.direction.x * self.speed
