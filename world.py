from bloop import Bloop
from DNA import DNA
import random
from graphics import *

class Bloop_World:
    def __init__(self, population_size, food_quantity, graph_win, width=600, height=800):
        self.bloops = []
        # self.food = []
        self.width = width
        self.height = height
        self.win = graph_win

        for i in range(population_size):
            bloop = Bloop(random.randint(0, self.width), random.randint(0, self.height), DNA(), self.width, self.height, self.win)
            self.bloops.append(bloop)

        # for i in range(food_quantity):
        #     self.food.append(PVector(random(0, width), random(0, height)))  # Place random food particles

    def update(self):
        for b in self.bloops:
            if b.isDead():
                # self.food.append(b.location)
                self.bloops.remove(b)
                continue

            b.update()
            b.edgeCollision()
            # b.eat(self.food)

            # child = b.reproduce()
            # if child != None:
            #     self.bloops.append(child)

    def draw(self):
        for b in self.bloops:
            b.draw()
        #
        # for f in self.food:
        #     noStroke()
        #     fill(0, 255, 0)
        #     ellipse(f.x, f.y, 10, 10)