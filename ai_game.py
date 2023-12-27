import random
import pygame

import constants as const
from pipe import Pipe
from bird import Bird
from generation import get_next_generation


class AiGame:

    def __init__(self):
        pygame.init()

        self.running = True
        self.pause = False
        self.game_over = False
        self.pipes = []
        self.birds = []
        self.dead_birds = []

        self.new_game(True)

    def update(self) -> None:
        for bird in self.birds:
            bird.update()
            bird.decide_action(self.pipes)

        for pipe in self.pipes:
            pipe.update()
            for bird in self.birds:
                self.check_collision(bird, pipe)

            if pipe.x + Pipe.WIDTH <= -10:
                self.pipes.remove(pipe)

            if pipe.x == const.WIDTH / 2:
                upper_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH * 2)
                lower_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH)
                self.pipes.append(Pipe(const.WIDTH, upper_y, lower_y))

    def render(self) -> None:
        const.SCREEN.fill((20, 10, 20))

        for bird in self.birds:
            bird.draw()

        for pipe in self.pipes:
            pipe.draw()

    def check_collision(self, bird: Bird, pipe: Pipe) -> None:
        # Collide with pipe
        collided = False
        if (
            pipe.x <= bird.x + bird.radius <= pipe.x + Pipe.WIDTH
            or pipe.x <= bird.x - bird.radius <= pipe.x + Pipe.WIDTH
        ):
            if (
                bird.y - bird.radius <= pipe.upper_y
                or bird.y + bird.radius >= pipe.lower_y
            ):
                pipe.color = "red"
                collided = True
        elif bird.y + bird.radius >= const.HEIGHT:
            # Collide with bottom
            collided = True

        if collided:
            self.birds.remove(bird)
            self.dead_birds.append(bird)
            if not self.birds:
                self.game_over = True

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Restarting game...")
                    self.new_game(True)
                elif event.key == pygame.K_q:
                    print("Exiting game...")
                    self.running = False

    def new_game(self, first_gen: bool) -> None:
        if first_gen:
            self.birds = []
            for _ in range(const.POP_SIZE):
                self.birds.append(Bird(random.randint(100, const.HEIGHT - 100), True))
        else:
            self.birds = get_next_generation(self.dead_birds)
            self.dead_birds = []

        self.pipes = []
        upper_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH * 2)
        lower_y = random.randint(Pipe.WIDTH, const.HEIGHT - Pipe.WIDTH)
        self.pipes.append(Pipe(const.WIDTH, upper_y, lower_y))
        self.game_over = False

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            self.check_events()
            self.update()
            self.render()
            if self.game_over:
                self.new_game(False)

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
