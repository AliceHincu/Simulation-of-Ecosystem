import bloop
import world
from graphics import *
from tkinter import *

# java -jar processing_py/processing-py.jar bloop/ecosystem.py
#
# World = None
#
# def setup() :
#     global World;
#     size(600, 600)
#
#     World = world.World(20, 50)
#
# def draw() :
#     background(51)
#
#     World.update()
#     World.draw()

W, H = 600, 800
# class Ball:
#     def __init__(self, size, color, win):
#         self.win = win
#         self.ball = win.create_oval(0,0,size,size,fill=color)
#         self.speedx = 4
#         self.speedy = 4
#         self.movement()
#
#     def movement(self):
#         win.move(self.ball, self.speedx, self.speedy)
#         pos = win.coords(self.ball)
#         if pos[2] >= W or pos[0] <= 0:
#             self.speedx *= -1
#         if pos[3]>=H or pos[1]<=0:
#             self.speedy *= -1
#         # tk.after(40, self.movement)
#         win.after(40, self.movement)
if __name__ == '__main__':
    W, H = 1200, 600
    win = Tk()
    win.geometry(str(W) + "x" + str(H))
    canvas = Canvas(win, width=W, height=H)
    canvas.configure(bg='white')

    canvas.pack()

    world = world.Bloop_World(1, 15, win, canvas, width=W, height=H)
    world.start()

    win.mainloop()
