import time
import sys
import pygame
from settings import screen_width, screen_height
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height),
            pygame.SCALED
        )
        pygame.display.set_caption("Project WIZARD")
        self.prev_time = time.time()
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.level = Level('map_level.txt', self.screen)
        self.running = True

    def calculate_dt(self):
        now = time.time()
        self.dt = (now - self.prev_time)
        self.dt += self.FPS
        self.prev_time = time.time()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.calculate_dt()
            self.level.run()
            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.start()
