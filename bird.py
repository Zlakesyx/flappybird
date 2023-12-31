import random
import pygame

from neuralnet.neural_network import NeuralNetwork

import constants as const
from pipe import Pipe


class Bird:

    def __init__(self, is_ai: bool) -> None:
        self.x = const.WIDTH / 4
        self.y = random.randint(100, const.HEIGHT - 100)
        self.dy = 0  # vertical speed
        self.flap_speed = -10
        self.flapping = False
        self.radius = 20
        self.color = "white"
        self.is_ai = is_ai
        self.score = 0.0
        self.fitness = 0.0

        if self.is_ai:
            self.brain = NeuralNetwork(5, 16, 2)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.color = pygame.Color(r, g, b)

    def flap(self) -> None:
        self.flapping = True

    def decide_action(self, pipes: list[Pipe]) -> None:
        closest = pipes[0]
        record = const.WIDTH

        # Closest back of pipe
        for pipe in pipes:
            diff = (pipe.x + Pipe.WIDTH) - (self.x - self.radius)
            if diff > 0 and diff < record:
                closest = pipe
                record = diff

        # normalize inputs
        norm_y = self.y / const.HEIGHT
        norm_dy = self.dy / 10
        norm_pipe_front = closest.x / const.WIDTH
        norm_pipe_top = closest.upper_y / const.HEIGHT
        norm_pipe_bottom = closest.lower_y / const.HEIGHT

        inputs = [
            norm_y,
            norm_dy,
            norm_pipe_front,
            norm_pipe_top,
            norm_pipe_bottom,
        ]

        # TODO outputs are both + 0.9. Why?
        output = self.brain.feed_forward(inputs)
        if output[0] > output[1]:
            self.flap()

    def update(self) -> None:
        self.score += 1

        if self.flapping:
            self.dy += self.flap_speed
            self.flapping = False

        if self.y - self.radius <= 0:
            self.dy = 0
            self.y = self.radius

        self.dy += const.GRAVITY
        self.y += self.dy

    def draw(self) -> None:
        pygame.draw.circle(const.SCREEN, self.color, (self.x, self.y), self.radius)
