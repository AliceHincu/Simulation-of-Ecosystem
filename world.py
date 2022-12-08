from bloop import Bloop
from DNA import DNA
import random

from food import Food
from natural_selection import GeneticAlgorithm2


class Bloop_World:
    def __init__(self, population_size, food_quantity, graph_win, canvas, width=600, height=800):
        self.population_size = population_size
        self.food_quantity = food_quantity
        self.bloops = []
        self.food = []
        self.width = width
        self.height = height
        self.win = graph_win
        self.canvas = canvas
        self.SECONDS = 10
        self.ITERATIONS = 1
        self.current_iteration = 1
        self.time_passed_ms = 0

    def init_population(self):
        # if it's first iteration: Place random bloops. Else you reproduce the bloops and enter a new iteration
        if self.current_iteration == 1:
            # Place random bloops
            for i in range(self.population_size):
                bloop = Bloop(random.randint(0, self.width), random.randint(0, self.height), DNA(), self.width, self.height, self.win, self.canvas)
                self.bloops.append(bloop)

            # Place random food particles
            for i in range(self.food_quantity):
                food = Food(random.randint(0, self.width), random.randint(0, self.height), self.canvas)
                self.food.append(food)
        else:
            # delete current items on screen
            for b in self.bloops:
                self.canvas.delete(b.circle)
            for f in self.food:
                self.canvas.delete(f.rectangle)

            bloops = list(filter(lambda bloop_elem: bloop_elem.nr_food_eaten >= 1, self.bloops))

            # delete old ones from list:
            self.bloops = []
            self.food = []

            # --- reproduce
            GeneticAlgorithm2().start_reproduction_iteration(bloops)

    def start(self):
        self.init_population()
        self.update()

    def update(self):
        # update time
        self.time_passed_ms += 40

        # update bloops
        for b in self.bloops:
            if b.is_dead():
                self.food.append(Food(b.location.x, b.location.y, self.canvas))
                self.bloops.remove(b)
                continue

            b.update()
            b.edge_collision()
            b.eat(self.food)

        # update iterations and population based on time.
        if self.time_passed_ms >= self.SECONDS * 1000:
            self.current_iteration += 1

            # start the new bloop population and reset iteration clock
            self.init_population()
            self.time_passed_ms = 0

            if self.current_iteration > self.ITERATIONS:
                print("done!")
                return

        self.draw()
        self.win.after(40, self.update)

    def draw(self):
        for b in self.bloops:
            b.draw()
