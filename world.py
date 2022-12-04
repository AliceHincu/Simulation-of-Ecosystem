from bloop import Bloop
from DNA import DNA
import random
from graphics import *

class Bloop_World:
    def __init__(self, population_size, food_quantity, graph_win, canvas, width=600, height=800):
        self.bloops = []
        # self.food = []
        self.width = width
        self.height = height
        self.win = graph_win
        self.canvas = canvas

        for i in range(population_size):
            bloop = Bloop(random.randint(0, self.width), random.randint(0, self.height), DNA(), self.width, self.height, self.win, self.canvas)
            self.bloops.append(bloop)

        # for i in range(food_quantity):
        #     self.food.append(PVector(random(0, width), random(0, height)))  # Place random food particles

    def update(self):
        if len(self.bloops) == 0:
            print("done!")
            return

        for b in self.bloops:
            if b.is_dead():
                # self.food.append(b.location)
                self.bloops.remove(b)
                continue

            # b.run()
            b.update()
            b.edge_collision()
            # b.eat(self.food)

            # child = b.reproduce()
            # if child != None:
            #     self.bloops.append(child)

        self.draw()
        self.win.after(40, self.update)

    def draw(self):
        for b in self.bloops:
            b.draw()

        # self.win.after()
        #
        # for f in self.food:
        #     noStroke()
        #     fill(0, 255, 0)
        #     ellipse(f.x, f.y, 10, 10)