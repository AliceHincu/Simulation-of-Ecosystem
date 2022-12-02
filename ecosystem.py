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

if __name__ == '__main__':
    win = GraphWin("My Window", 600, 800)
    win.setBackground(color_rgb(255, 255, 255))

    world = world.Bloop_World(1, 1, win)
    world.draw()
    # while True:
    #     world.update()
    #     world.draw()

    win.getMouse()
    win.close()