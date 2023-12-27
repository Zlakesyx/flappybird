import copy
import random

import constants as const
from bird import Bird


def calculate_fitness(population: list[Bird]) -> None:
    # TODO how and when to calculate fitness against current population (alive and dead)
    total = 0

    for bird in population:
        total += bird.score

    for bird in population:
        bird.fitness = float(bird.score) / total


def pick_one(population: list[Bird], ) -> Bird:
    # TODO review algorithm for better understanding
    index = 0
    random_num = random.random()  # random num 0 - 1

    while random_num > 0:
        random_num = random_num - population[index].fitness
        index += 1

    index -= 1

    child = copy.deepcopy(population[index])
    child.brain.mutate(mutate)
    return child


def mutate(x: any) -> None:
    rate = 0.10
    if random.random() < rate:
        new_val = x + random.gauss(0, 0.1)
        return new_val
    else:
        return x


def get_next_generation(population: list[Bird]) -> list[Bird]:
    calculate_fitness(population)

    next_gen = []

    for _ in range(const.POP_SIZE):
        next_gen.append(pick_one(population))
    return next_gen
