from PVector import PVector


class Food:
    def __init__(self, x, y, canvas):
        self.location = PVector(x, y)
        self.canvas = canvas
        self.shape_drawn = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='gray')


class CustomFood:
    def __init__(self, x, y, canvas, color, size):
        self.location = PVector(x, y)
        self.canvas = canvas
        self.shape_drawn = self.canvas.create_rectangle(x, y, x + size, y + size, fill=color)
