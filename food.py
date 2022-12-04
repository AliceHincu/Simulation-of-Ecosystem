from PVector import PVector


class Food:
    def __init__(self, x, y, canvas):
        self.location = PVector(x, y)
        self.canvas = canvas
        self.rectangle = self.canvas.create_rectangle(x, y, x+10, y+10, fill='gray')