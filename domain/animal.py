from domain.bloop import Bloop


class Prey(Bloop):
    def __init__(self, x, y, dna, window_width, window_height, graph_win, canvas):
        Bloop.__init__(self, x, y, dna, window_width, window_height, graph_win, canvas)
        self.canvas.itemconfig(self.shape_drawn, fill='yellow')