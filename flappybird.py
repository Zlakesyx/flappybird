import pygame
import random


pygame.init()

WIDTH = 800
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
GRAVITY = 0.3


class Bird:

    def __init__(self, y: float) -> None:
        self.x = WIDTH / 4
        self.y = y  # vertical position
        self.dy = 0  # vertical speed
        self.flap_speed = -10
        self.flapping = False
        self.radius = 20

    def flap(self) -> None:
        self.flapping = True

    def update(self) -> None:
        if self.flapping:
            self.dy += self.flap_speed
            self.flapping = False

        if self.y - self.radius <= 0:
            self.dy = 0
            self.y = self.radius

        self.dy += GRAVITY
        self.y += self.dy

    def draw(self) -> None:
        pygame.draw.circle(SCREEN, "white", (self.x, self.y), self.radius)


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
        pygame.draw.rect(SCREEN, self.color, (self.x, 0, self.width, self.upper_y))
        pygame.draw.rect(SCREEN, self.color, (self.x, self.lower_y, self.width, HEIGHT))


class Game:

    def __init__(self):
        self.running = True
        self.pause = False
        self.game_over = False

        self.bird = Bird(HEIGHT / 2)
        self.pipes = []
        self.pipes.append(Pipe(WIDTH, 100, 200))

    def update(self) -> None:
        self.bird.update()

        for pipe in self.pipes:

            pipe.update()
            self.check_collision(self.bird, pipe)

            if pipe.x + pipe.width <= -10:
                self.pipes.remove(pipe)

            if pipe.x == WIDTH / 2:
                upper_y = random.randint(pipe.width, HEIGHT - pipe.width * 2)
                lower_y = random.randint(pipe.width, HEIGHT - pipe.width)
                self.pipes.append(Pipe(WIDTH, upper_y, lower_y))

    def render(self) -> None:
        SCREEN.fill((20, 10, 20))
        self.bird.draw()

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
        if bird.y + bird.radius >= HEIGHT:
            self.game_over = True

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()
                elif event.key == pygame.K_r:
                    self.restart()

    def restart(self) -> None:
        self.bird = Bird(HEIGHT / 2)
        self.pipes = []
        self.pipes.append(Pipe(WIDTH, 100, 200))
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


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
