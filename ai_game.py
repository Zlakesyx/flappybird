import random
import pygame

import constants as const
from pipe import Pipe
from bird import Bird


class AiGame:

    def __init__(self):
        pygame.init()

        self.running = True
        self.pause = False
        self.game_over = False
        self.pipes = None
        self.birds = None
        self.pop_size = None

        self.new_game()

    def update(self) -> None:
        for bird in self.birds:
            bird.update()

        for pipe in self.pipes:

            pipe.update()
            for bird in self.birds:
                self.check_collision(bird, pipe)

            if pipe.x + pipe.width <= -10:
                self.pipes.remove(pipe)

            if pipe.x == const.WIDTH / 2:
                upper_y = random.randint(pipe.width, const.HEIGHT - pipe.width * 2)
                lower_y = random.randint(pipe.width, const.HEIGHT - pipe.width)
                self.pipes.append(Pipe(const.WIDTH, upper_y, lower_y))

    def render(self) -> None:
        const.SCREEN.fill((20, 10, 20))

        for bird in self.birds:
            bird.draw()

        for pipe in self.pipes:
            pipe.draw()

    def check_collision(self, bird: Bird, pipe: Pipe) -> None:
        # Collide with pipe
        if (
            pipe.x <= bird.x + bird.radius <= pipe.x + pipe.width
            or pipe.x <= bird.x - bird.radius <= pipe.x + pipe.width
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
                    for bird in self.birds:
                        bird.flap()
                elif event.key == pygame.K_r:
                    self.new_game()
                elif event.key == pygame.K_q:
                    print("Exiting game...")
                    self.running = False

    def new_game(self) -> None:
        self.pop_size = 100
        self.birds = []
        for _ in range(self.pop_size):
            self.birds.append(Bird(random.randint(100, const.HEIGHT - 100)))

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

