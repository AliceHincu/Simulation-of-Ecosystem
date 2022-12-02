import math


class PVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_vector):
        self.x += other_vector.x
        self.y += other_vector.y

    def dist(self, other_vector):
        return math.dist([self.x, self.y], [other_vector.x, other_vector.y])
