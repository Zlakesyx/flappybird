import pygame

import constants as const

# TODO Figure out how to properly import external repo. Do I just move flappy
# bird inside the neuralnet library, publish (pip) library, create makefile?
#from neuralnet.neural_network import NeuralNetwork


class Bird:

    def __init__(self, y: float) -> None:
        self.x = const.WIDTH / 4
        self.y = y  # vertical position
        self.dy = 0  # vertical speed
        self.flap_speed = -10
        self.flapping = False
        self.radius = 20
        #self.brain = NeuralNetwork(4, 4, 1)  # What are the inputs?

    def flap(self) -> None:
        self.flapping = True

    def update(self) -> None:
        if self.flapping:
            self.dy += self.flap_speed
            self.flapping = False

        if self.y - self.radius <= 0:
            self.dy = 0
            self.y = self.radius

        self.dy += const.GRAVITY
        self.y += self.dy

    def draw(self) -> None:
        pygame.draw.circle(const.SCREEN, "white", (self.x, self.y), self.radius)
