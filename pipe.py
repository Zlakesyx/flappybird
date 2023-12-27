import pygame

import constants as const


class Pipe:

    WIDTH = 100

    def __init__(self, x: float, upper_y: float, lower_y: float) -> None:
        self.x = x
        self.upper_y = upper_y
        self.lower_y = lower_y
        self.min_gap = 175
        self.dx = -4  # increments of 2 or pipes will not spawn
        self.color = "teal"

        if lower_y - upper_y < self.min_gap:
            self.lower_y = self.upper_y + self.min_gap

    def update(self) -> None:
        self.x += self.dx

    def draw(self) -> None:
        pygame.draw.rect(const.SCREEN, self.color, (self.x, 0, Pipe.WIDTH, self.upper_y))
        pygame.draw.rect(const.SCREEN, self.color, (self.x, self.lower_y, Pipe.WIDTH, const.HEIGHT))
