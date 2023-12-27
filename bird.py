import math
import random
import pygame

from neuralnet.neural_network import NeuralNetwork

import constants as const
from pipe import Pipe


class Bird:

    def __init__(self, y: float, is_ai: bool) -> None:
        self.x = const.WIDTH / 4
        self.y = y  # vertical position
        self.dy = 0  # vertical speed
        self.flap_speed = -10
        self.flapping = False
        self.radius = 20
        self.color = "white"
        self.is_ai = is_ai
        self.score = 0.0
        self.fitness = 0.0

        if self.is_ai:
            self.brain = NeuralNetwork(6, 16, 2)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.color = pygame.Color(r, g, b)

    def flap(self) -> None:
        self.flapping = True

    def decide_action(self, pipes: list[Pipe]) -> None:
        """
        inputs: [
                    vertical position,
                    distance from pipe upper,
                    distance from pipe lower,
                    velocity
                ]
        """
        closest = pipes[0]

        for pipe in pipes:
            diff = pipe.x - self.x
            if diff > 0 and diff > closest.x:
                closest = pipe

        dy_min = -100
        dy_max = 100
        pipe_back = closest.x + Pipe.WIDTH
        bird_front = self.x + self.radius
        bird_back = self.x - self.radius
        bird_top = self.y - self.radius
        bird_bottom = self.y + self.radius

        # normalize inputs
        norm_y = self.y / const.HEIGHT
        norm_dy = (self.dy - (dy_min)) / (dy_max - dy_min)
        norm_dist_upper_front = math.pow((closest.x - bird_front), 2) + math.pow((closest.upper_y - bird_top), 2)
        norm_dist_lower_front = math.pow((closest.x - bird_front), 2) + math.pow((closest.lower_y - bird_bottom), 2)
        norm_dist_upper_back = math.pow((pipe_back - bird_back), 2) + math.pow((closest.upper_y - bird_top), 2)
        norm_dist_lower_back = math.pow((pipe_back - bird_back), 2) + math.pow((closest.lower_y - bird_bottom), 2)
        norm_dist_upper_front = math.sqrt(norm_dist_upper_front) / const.HEIGHT
        norm_dist_lower_front = math.sqrt(norm_dist_lower_front) / const.HEIGHT
        norm_dist_upper_back = math.sqrt(norm_dist_upper_back) / const.HEIGHT
        norm_dist_lower_back = math.sqrt(norm_dist_lower_back) / const.HEIGHT

        inputs = [
            norm_y,
            norm_dy,
            norm_dist_upper_front,
            norm_dist_lower_front,
            norm_dist_upper_back,
            norm_dist_lower_back,
        ]

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
        if self.is_ai:
            pygame.draw.circle(const.SCREEN, "white", (self.x, self.y), self.radius + 1)
        pygame.draw.circle(const.SCREEN, self.color, (self.x, self.y), self.radius)
