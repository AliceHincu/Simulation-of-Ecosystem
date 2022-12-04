from PVector import PVector
from bloop import Bloop
from DNA import DNA
import random

from food import Food
from graphics import *

class Bloop_World:
    def __init__(self, population_size, food_quantity, graph_win, canvas, width=600, height=800):
        self.bloops = []
        self.food = []
        self.width = width
        self.height = height
        self.win = graph_win
        self.canvas = canvas

        # Place random bloops
        for i in range(population_size):
            bloop = Bloop(random.randint(0, self.width), random.randint(0, self.height), DNA(), self.width, self.height, self.win, self.canvas)
            self.bloops.append(bloop)

        # Place random food particles
        for i in range(food_quantity):
            food = Food(random.randint(0, self.width), random.randint(0, self.height), self.canvas)
            self.food.append(food)

    def update(self):
        if len(self.bloops) == 0:
            print("done!")
            return

        for b in self.bloops:
            if b.is_dead():
                self.food.append(Food(b.location.x, b.location.y, self.canvas))
                self.bloops.remove(b)
                continue

            # b.run()
            b.update()
            b.edge_collision()
            b.eat(self.food)

            # child = b.reproduce()
            # if child != None:
            #     self.bloops.append(child)

        self.draw()
        self.win.after(40, self.update)

    def draw(self):
        for b in self.bloops:
            b.draw()
