import pygame

import constants as const


class Pipe:

    def __init__(self, x: float, upper_y: float, lower_y: float) -> None:
        self.x = x
        self.upper_y = upper_y
        self.lower_y = lower_y
        self.width = 100
        self.min_gap = 125
        self.dx = -2
        self.color = "teal"

        if lower_y - upper_y < self.min_gap:
            self.lower_y = self.upper_y + self.min_gap

    def update(self) -> None:
        self.x += self.dx

    def draw(self) -> None:
        pygame.draw.rect(const.SCREEN, self.color, (self.x, 0, self.width, self.upper_y))
        pygame.draw.rect(const.SCREEN, self.color, (self.x, self.lower_y, self.width, const.HEIGHT))
