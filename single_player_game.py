import random
import pygame

import constants as const
from pipe import Pipe
from bird import Bird


class SinglePlayerGame:

    def __init__(self):
        pygame.init()

        self.running = True
        self.pause = False
        self.game_over = False
        self.pipes = None
        self.bird = None

        self.new_game()

    def update(self) -> None:
        self.bird.update()

        for pipe in self.pipes:

            pipe.update()
            self.check_collision(self.bird, pipe)

            if pipe.x + Pipe.WIDTH <= -10:
                self.pipes.remove(pipe)

            if pipe.x == const.WIDTH / 2:
                upper_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH * 2)
                lower_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH)
                self.pipes.append(Pipe(const.WIDTH, upper_y, lower_y))

    def render(self) -> None:
        const.SCREEN.fill((20, 10, 20))

        self.bird.draw()

        for pipe in self.pipes:
            pipe.draw()

    def check_collision(self, bird: Bird, pipe: Pipe) -> None:
        # Collide with pipe
        if (
            pipe.x <= bird.x + bird.radius <= pipe.x + Pipe.WIDTH
            or pipe.x <= bird.x - bird.radius <= pipe.x + Pipe.WIDTH
        ):
            if (
                bird.y - bird.radius <= pipe.upper_y
                or bird.y + bird.radius >= pipe.lower_y
            ):
                pipe.color = "red"
                self.game_over = True

        # Collide with bottom
        if bird.y + bird.radius >= const.HEIGHT:
            self.game_over = True

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()
                elif event.key == pygame.K_r:
                    self.new_game()
                elif event.key == pygame.K_q:
                    print("Exiting game...")
                    self.running = False

    def new_game(self) -> None:
        self.bird = Bird(False)

        self.pipes = []
        self.pipes.append(Pipe(const.WIDTH, 100, 200))
        self.game_over = False

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.check_events()
            if not self.game_over:
                self.update()
                self.render()

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
