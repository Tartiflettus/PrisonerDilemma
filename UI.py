# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:29:50 2019

@author: Victor
"""
import tkinter as tk
import PrisonerDilemma as pd
import random


# noinspection PyUnusedLocal
class UI:
    # global var to hold the last painted rectangle
    lastRect = (-1, -1)
    # global var for the number of iterations
    counter = 0
    # global var for the play/pause button
    play = False
    # global var for the number of iterations in a second
    fps = 10

    def __init__(self, width=30, height=10, rect_size=15):
        self._width = width
        self._height = height
        self._rect_size = rect_size
        self._grid = []
        self._gridCanvas = []
        self._can = 0

        self.eca = pd.Configuration(width, 4, 1.1)

        self._win = tk.Tk()
        self._win.title("Prisoner's Dilemma ECA")
        self._win.configure()

        # paned frames
        self._panLeft = tk.Frame(self._win)
        self._panLeft.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

        self._panRight = tk.Frame(self._win)
        self._panRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=10, pady=10)

        # left frame components
        self.controlsGrid = tk.Frame(self._panLeft)
        self.controlsGrid.grid(row=0, column=0, sticky=tk.S + tk.W + tk.E + tk.N, padx=5, pady=5)

        # next configuration button
        btn_next_config = tk.Button(self.controlsGrid, text="NEXT", command=self.next_config, width=7)
        btn_next_config.grid(row=0, column=0, padx=5, pady=2)

        # continuous next configuration button
        self.btn_play_config = tk.Button(self.controlsGrid, text="PLAY", command=self.play_thread, width=7)
        self.btn_play_config.grid(row=0, column=1, padx=5, pady=2)

        # choose iterations per second
        tk.Label(self.controlsGrid, text="Iterations/s").grid(row=1, column=1)
        self.fps_box = tk.Spinbox(self.controlsGrid, from_=1, to_=6000, width=7, command=self.fps_changed,
                                  textvariable=tk.DoubleVar(value=self.fps))
        self.fps_box.grid(row=1, column=0)

        # iteration number
        tk.Label(self.controlsGrid, text="Iterations").grid(row=2, column=1)
        self.iter_label = tk.Label(self.controlsGrid, text=self.counter)
        self.iter_label.grid(row=2, column=0)

        # choose width
        tk.Label(self.controlsGrid, text="Width").grid(row=3, column=0)
        self.chosenWidth = tk.Spinbox(self.controlsGrid, from_=3, to_=1000, width=7, command=self.width_changed,
                                      textvariable=tk.DoubleVar(value=self._width))
        self.chosenWidth.grid(row=3, column=1)

        # choose height
        tk.Label(self.controlsGrid, text="Height").grid(row=4, column=0)
        self.chosenHeight = tk.Spinbox(self.controlsGrid, from_=2, to_=100, width=7, command=self.height_changed,
                                       textvariable=tk.DoubleVar(value=self._height))
        self.chosenHeight.grid(row=4, column=1)

        # choose collaborator percentage
        tk.Label(self.controlsGrid, text="Collaborators %").grid(row=5, column=0)
        self.chosenPercentage = tk.Spinbox(self.controlsGrid, from_=0, to_=100, width=7,
                                           textvariable=tk.DoubleVar(value=50))
        self.chosenPercentage.grid(row=5, column=1)

        # init with the collaborator percentage
        tk.Button(self.controlsGrid, text="INIT", command=self.init).grid(row=5, column=2)

        # temptation slider
        tk.Label(self.controlsGrid, text="Temptation").grid(row=6, column=0)
        self.chosenTemptation = tk.Spinbox(self.controlsGrid, from_=0, to_=100, textvariable=tk.DoubleVar(value=10),
                                           command=self.temptationChanged)
        self.chosenTemptation.grid(row=6, column=1)

        # clear canvas button
        btn_reinit = tk.Button(self.controlsGrid, text="CLEAR", command=self.update, width=7)
        btn_reinit.grid(row=7, columnspan=2, padx=5, pady=2)

        # init the grid and create the canvas
        self._grid = [[0 for i in range(self._width)] for j in range(self._height)]
        self._gridCanvas = [[0 for i in range(self._width)] for j in range(self._height)]
        self._can = tk.Canvas(self._panRight, width=self._width * self._rect_size,
                              height=self._height * self._rect_size)
        self._can.pack()
        self.create_rectangles()
        self.repaint()

        # set mouse click to paint rect
        self._can.bind("<B1-Motion>", self.paint)
        self._can.bind("<Button-1>", self.paint)

        self._win.mainloop()

    def update(self):
        if self.play:
            self.play_thread()
        self._grid = [[0 for i in range(self._width)] for j in range(self._height)]
        self._gridCanvas = [[0 for i in range(self._width)] for j in range(self._height)]
        self._can.configure(width=self._width * self._rect_size, height=self._height * self._rect_size)
        self.create_rectangles()
        self.repaint(0)
        self.eca = pd.Configuration(self._width, 4, 1. + self.chosenTemptation/100.)
        self.counter = 0

    def paint(self, event):
        x = event.x // self._rect_size
        y = event.y // self._rect_size

        # check for index out of range
        if x >= self._width or x < 0 or y >= self._height or y < 0:
            return

        # check for rect change and click event
        if UI.lastRect == (x, y) and event.type == tk.EventType.Motion:
            return

        # set current rect as last changed rect
        UI.lastRect = (x, y)

        self._grid[y][x] ^= 1
        col = "yellow" if self._grid[y][x] else "red"
        self._can.itemconfig(self._gridCanvas[y][x], fill=col)

    def repaint(self, init=1):
        self.counter += 1 * init
        self.iter_label.configure(text=self.counter)
        for y in range(self._height):
            for x in range(self._width):
                col = "yellow" if self._grid[y][x] else "red"
                if self._can.itemcget(self._gridCanvas[y][x], "fill") != col:
                    self._can.itemconfig(self._gridCanvas[y][x], fill=col)

    def create_rectangles(self):
        self._can.delete("all")
        for y in range(self._height):
            for x in range(self._width):
                x_top = x * self._rect_size
                y_top = y * self._rect_size
                x_bot = x_top + self._rect_size
                y_bot = y_top + self._rect_size
                col = "yellow" if self._grid[y][x] else "red"
                self._gridCanvas[y][x] = self._can.create_rectangle(x_top, y_top, x_bot, y_bot, fill=col)

    def fps_changed(self):
        self.fps = int(self.fps_box.get())

    def width_changed(self):
        self._width = int(self.chosenWidth.get())
        self.update()

    def height_changed(self):
        self._height = int(self.chosenHeight.get())
        self.update()

    def retrieve_config(self):
        for x in range(self._width):
            self.eca.set_cell(x, self._grid[0][x])
        return self.eca.next()

    def set_config(self, config):
        line = config.get_line()
        for i in range(len(line)):
            self._grid[0][i] = line[i]

    def shift_grid_down(self):
        for y in range(self._height - 1, 0, -1):
            for x in range(0, self._width):
                self._grid[y][x] = self._grid[y - 1][x]

    def next_config(self):
        self.shift_grid_down()

        # add next config to the grid
        self.set_config(self.retrieve_config())

        self.repaint()
        if self.play:
            self._win.after(1000 // self.fps, self.next_config)

    def init(self):
        for x in range(self._width):
            sample = random.randint(0, 100)
            if sample <= int(self.chosenPercentage.get()):
                self._grid[0][x] = 1
            else:
                self._grid[0][x] = 0
        self.repaint()

    def temptationChanged(self):
        self.update()

    def play_thread(self):
        self.play = not self.play
        self.btn_play_config.configure(text="PAUSE" if self.play else "PLAY")
        if self.play:
            self._win.after_idle(self.next_config)


if __name__ == "__main__":
    ui = UI()
