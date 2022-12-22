import math

import numpy as np

from domain.animal import Prey
from domain.bloop import Bloop
from domain.DNA import DNA
import random

from domain.food import Food, CustomFood
from natural_selection import GeneticAlgorithm2

INDIVIDUAL_QNT = 30


# get rid of predator
class AnimalWorld:
    def __init__(self, population_size, graph_win, canvas, width=600, height=800):
        self.population_size = population_size
        self.food_quantity = math.ceil((np.random.randint(30, 101) / 100) * INDIVIDUAL_QNT)
        self.predators = []
        self.preys = []
        self.food = []
        self.width = width
        self.height = height
        self.win = graph_win
        self.canvas = canvas
        self.SECONDS = 10
        self.ITERATIONS = 5
        self.current_iteration = 1
        self.time_passed_ms = 0

    def init_population(self):
        # if it's first iteration: Place random bloops. Else you reproduce the bloops and enter a new iteration
        # if self.current_iteration == 1:
        # Place random bloops
        for i in range(self.population_size):
            prey = Prey(random.randint(0, self.width), random.randint(0, self.height), DNA(random.uniform(0, 1)),
                        self.width, self.height, self.win, self.canvas)
            self.preys.append(prey)

        # Place random food particles
        for i in range(self.food_quantity):
            food = CustomFood(random.randint(0, self.width), random.randint(0, self.height), self.canvas, "green", 10)
            self.food.append(food)
        # else:
        #     # delete current items on screen
        #     for b in self.bloops:
        #         self.canvas.delete(b.circle)
        #     for f in self.food:
        #         self.canvas.delete(f.rectangle)
        #
        #     bloops = list(filter(lambda bloop_elem: bloop_elem.nr_food_eaten >= 1, self.bloops))
        #
        #     # delete old ones from list:
        #     self.bloops = []
        #     self.food = []
        #
        #     # --- reproduce
        #     self.bloops = GeneticAlgorithm2().start_reproduction_iteration(bloops)
        #     # Place random food particles
        #     self.food_quantity = self.food_quantity//2
        #     for i in range(self.food_quantity):
        #         food = Food(random.randint(0, self.width), random.randint(0, self.height), self.canvas)
        #         self.food.append(food)
        #     print("Reproduced!")

        # if self.current_iteration == self.ITERATIONS:
        #     GeneticAlgorithm2().plot_result(fitness_values, x, 0, self.current_iteration, len(self.bloops))

    def start(self):
        self.init_population()
        self.update()

    def update(self):
        # update time
        self.time_passed_ms += 40

        # update bloops
        for p in self.preys:
            if p.is_dead():
                self.preys.remove(p)
                continue

            p.update()
            p.edge_collision()
            p.eat(self.food)

        # update iterations and population based on time.
        # if self.time_passed_ms >= self.SECONDS * 1000:
        #     self.current_iteration += 1
        #
        #     # start the new bloop population and reset iteration clock
        #     print("ITERATION " + str(self.current_iteration))
        #     self.init_population()
        #     self.time_passed_ms = 0
        #
        #     if self.current_iteration > self.ITERATIONS:
        #         print("done!")
        #         return

        # self.draw()
        self.win.after(40, self.update)

    # def draw(self):
    #     for b in self.bloops:
    #         b.draw()
