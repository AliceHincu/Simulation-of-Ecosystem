import math
import random

import noise as noise

import DNA
from PVector import PVector
from graphics import *


class Bloop:
    def __init__(self, x, y, dna, window_width, window_height, graph_win, canvas):
        self.location = PVector(x, y)
        self.window = [window_width, window_height]
        self.health = 200
        self.dna = dna
        self.win = graph_win
        self.canvas = canvas

        # DNA will determine size and max_speed
        # The bigger the bloop, the slower it is
        self.size = translate(self.dna.gene, 0, 1, 20, 80)  # the radius
        self.maxSpeed = translate(self.dna.gene, 0, 1, 5, 0)
        self.vx = 1
        self.vy = 1

        # Vars for perlin noise
        self.xOff = random.randint(0, 1000)
        self.yOff = random.randint(0, 1000)

        # Object drawn
        self.circle = self.canvas.create_oval(self.location.x, self.location.y, self.location.x+self.size, self.location.y+self.size, fill='black', outline="")
        self.nr_food_eaten = 0

    def run(self):
        self.update()
        self.edge_collision()
        # self.draw()

    def update(self):
        """
        Simple movement based on perlin noise
        :return:
        """
        self.vx = translate(noise.pnoise1(self.xOff), 0, 1, -self.maxSpeed, self.maxSpeed)
        self.vy = translate(noise.pnoise1(self.yOff), 0, 1, -self.maxSpeed, self.maxSpeed)
        self.xOff += 0.01
        self.yOff += 0.01

        # Add velocity
        velocity = PVector(self.vx, self.vy)
        self.location.add(velocity)

        # Death always looming
        self.canvas.move(self.circle, self.vx, self.vy)
        self.health -= 0.5

    def draw(self):
        gray_rgb = max(0, math.floor(translate(self.health, 200, 0, 0, 255)))
        self.canvas.itemconfig(self.circle, fill=color_rgb(gray_rgb, gray_rgb, gray_rgb))

    def edge_collision(self):
        if self.location.x < -self.size/2:
            self.location.x = self.window[0] + self.size/2
            self.canvas.coords(self.circle, self.location.x, self.location.y, self.location.x+self.size, self.location.y+self.size)
        if self.location.y < -self.size/2:
            self.location.y = self.window[1] + self.size/2
            self.canvas.coords(self.circle, self.location.x, self.location.y, self.location.x+self.size, self.location.y+self.size)
        if self.location.x > self.window[0] + self.size/2:
            self.location.x = -self.size/2
            self.canvas.coords(self.circle, self.location.x, self.location.y, self.location.x+self.size, self.location.y+self.size)
        if self.location.y > self.window[1] + self.size/2:
            self.location.y = -self.size/2
            self.canvas.coords(self.circle, self.location.x, self.location.y, self.location.x+self.size, self.location.y+self.size)

    def is_dead(self):
        if self.health <= 0:
            return True

        return False

    def eat(self, food):
        for f in food:
            if self.location.dist(f.location) < self.size / 2:
                self.health += 100
                food.remove(f)
                self.canvas.delete(f.rectangle)
                self.nr_food_eaten += 1

    # def reproduce(self, bloops):
    #     if random.random() < 0.001:
    #         child_dna = DNA.DNA()
    #         child = Bloop(self.location.x, self.location.y, child_dna, self.window[0], self.window[1], self.win, self.canvas)
    #
    #         return child
    #
    #     return None


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)