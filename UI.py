# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:29:50 2019

@author: Victor
"""
import tkinter as tk
import PrisonerDilemma as pd


class UI:
    # global var to hold the last painted rectangle
    lastRect = (-1, -1)
    # global var for the number of iterations
    counter = 0
    # global var for the play/pause button
    play = False
    # global var for the number of iterations in a second
    fps = 1

    def __init__(self, width=16, height=10, rect_size=15):
        self._width = width
        self._height = height
        self._rect_size = rect_size
        self._grid = []
        self._can = 0

        self.eca = pd.Configuration(width, 2, 1.1)

        self._win = tk.Tk()
        self._win.title("Prisoner's Dilemma ECA")
        self._win.configure()
        # self._win.pack(fill=tk.BOTH, expand=True)

        # paned frames
        self._panLeft = tk.Frame(self._win)
        self._panLeft.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

        self._panRight = tk.Frame(self._win)
        self._panRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=10, pady=10)

        # left frame components
        self.controlsGrid = tk.Frame(self._panLeft)
        self.controlsGrid.grid(row=0, column=0, sticky=tk.S+tk.W+tk.E+tk.N, padx=5, pady=5)

        # next configuration button
        btn_next_config = tk.Button(self.controlsGrid, text="NEXT", command=self.next_config, width=7)
        btn_next_config.grid(row=0, column=0, padx=5, pady=2)

        # continuous next configuration button
        self.btn_play_config = tk.Button(self.controlsGrid, text="PLAY", command=self.play_thread, width=7)
        self.btn_play_config.grid(row=0, column=1, padx=5, pady=2)

        # choose iterations per second
        tk.Label(self.controlsGrid, text="Iterations/s").grid(row=1, column=1)
        self.fps_box = tk.Spinbox(self.controlsGrid, from_=1, to_=100, width=7, command=self.fps_changed)
        self.fps_box.grid(row=1, column=0)

        # iteration number
        tk.Label(self.controlsGrid, text="Iterations").grid(row=2, column=1)
        self.iter_label = tk.Label(self.controlsGrid, text=self.counter)
        self.iter_label.grid(row=2, column=0)

        # choose width
        tk.Label(self.controlsGrid, text="Width").grid(row=3, column=0)
        self.chosenWidth = tk.Spinbox(self.controlsGrid, from_=16, to_=1000, width=7, command=self.width_changed)
        self.chosenWidth.grid(row=3, column=1)

        # choose height
        tk.Label(self.controlsGrid, text="Width").grid(row=4, column=0)
        self.chosenHeight = tk.Spinbox(self.controlsGrid, from_=16, to_=1000, width=7, command=self.height_changed)
        self.chosenHeight.grid(row=4, column=1)

        # init the grid and create the canvas
        self._grid = [[0 for i in range(self._width)] for j in range(self._height)]
        self._can = tk.Canvas(self._panRight, width=self._width*self._rect_size, height=self._height*self._rect_size)
        self._can.pack()
        self.repaint()

        # set mouse click to paint rect
        self._can.bind("<B1-Motion>", self.paint)
        self._can.bind("<Button-1>", self.paint)

        self._win.mainloop()

    def update(self):
        self._grid = [[0 for i in range(self._width)] for j in range(self._height)]
        self._can.configure(width=self._width*self._rect_size, height=self._height*self._rect_size)
        self.repaint(0)
        self.eca = pd.Configuration(self._width, 2, 1.1)

    def paint(self, event):
        x = event.x // self._rect_size
        y = event.y // self._rect_size

        # check for index out of range
        if x >= self._width or y >= self._height:
            return

        # check for rect change and click event
        if UI.lastRect == (x, y) and event.type == tk.EventType.Motion:
            return

        # set current rect as last changed rect
        UI.lastRect = (x, y)

        x_norm = x * self._rect_size
        y_norm = y * self._rect_size
        self._grid[y][x] ^= 1
        col = "yellow" if self._grid[y][x] else "red"
        self._can.create_rectangle(x_norm, y_norm, x_norm + self._rect_size, y_norm + self._rect_size, fill=col)

    def repaint(self, init=1):
        self.counter += 1*init
        self.iter_label.configure(text=self.counter)
        self._can.delete("all")
        for y in range(self._height):
            for x in range(self._width):
                x_top = x * self._rect_size
                y_top = y * self._rect_size
                x_bot = x_top + self._rect_size
                y_bot = y_top + self._rect_size
                col = "yellow" if self._grid[y][x] else "red"
                self._can.create_rectangle(x_top, y_top, x_bot, y_bot, fill=col)

    def fps_changed(self):
        self.fps = int(self.fps_box.get())

    def width_changed(self):
        self._width = int(self.chosenWidth.get())
        self.update()

    def height_changed(self):
        self._height = int(self.chosenHeight.get())
        self.update()

    def retrieve_config(self):
        # config = pd.Configuration(self._width, 2, 1.1)
        for x in range(self._width):
            # config.set_cell(x, self._grid[y][x])
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
        # print("next config")
        self.shift_grid_down()

        # add next config to the grid
        self.set_config(self.retrieve_config())

        self.repaint()
        if self.play:
            self._win.after(1000//self.fps, self.next_config)

    def update_thread(self):
        return

    def play_thread(self):
        self.play = not self.play
        self.btn_play_config.configure(text="PAUSE" if self.play else "PLAY")
        if self.play:
            self._win.after_idle(self.next_config)


if __name__ == "__main__":
    ui = UI()
