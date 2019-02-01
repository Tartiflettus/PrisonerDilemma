# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:29:50 2019

@author: perso
"""

import tkinter as tk
import PrisonerDilemma as pd


class UI:
    def __init__(self, width=16, height=10, rect_size=15):
        self._win = tk.Tk()
        self._win.configure(background="black")
        # self._win.pack(fill=tk.BOTH, expand=True)
        # paned windows
        self._pantop = tk.Frame(self._win)
        self._pantop.pack(side=tk.TOP)
        self._panbot = tk.Frame(self._win)
        self._panbot.pack(side=tk.BOTTOM)
        
        # next configuration button
        btn_next_config = tk.Button(self._pantop, text="NEXT", command=self.next_config)
        btn_next_config.pack()
        
        # simple label
        lab = tk.Label(self._pantop, text="Most recent configuration is at the top")
        lab.pack()
        
        # init the grid
        self._width = width
        self._height = height
        self._rect_size = rect_size
        self._grid = [[0 for i in range(width)] for j in range(height)]

        # draw the canvas
        self._can = tk.Canvas(self._panbot, width=width*rect_size, height=height*rect_size)
        self._can.pack()
        self._can.bind("<B1-Motion>", self.paint)
        self.repaint()

        self._win.mainloop()

    def paint(self, event):
        x = event.x // self._rect_size
        y = event.y // self._rect_size
        x_norm = x * self._rect_size
        y_norm = y * self._rect_size

        if self._grid[y][x] == 0:
            self._grid[y][x] = 1
            self._can.create_rectangle(x_norm, y_norm, x_norm+self._rect_size, y_norm+self._rect_size, fill="yellow")
        else:
            self._grid[y][x] = 0
            self._can.create_rectangle(x_norm, y_norm, x_norm + self._rect_size, y_norm + self._rect_size, fill="red")

    def repaint(self):
        for y in range(self._height):
            for x in range(self._width):
                x_top = x * self._rect_size
                y_top = y * self._rect_size
                x_bot = x_top + self._rect_size
                y_bot = y_top + self._rect_size
                if self._grid[y][x] == 0:
                    self._can.create_rectangle(x_top, y_top, x_bot, y_bot, fill="red")
                else:
                    self._can.create_rectangle(x_top, y_top, x_bot, y_bot, fill="yellow")

    def retrieve_config(self, y):
        config = pd.Configuration(self._width, 2, 1.1)
        for x in range(self._width):
            config.set_cell(x, self._grid[y][x])
        return config
    
    def set_config(self, config):
        line = config.get_line()
        for i in range(len(line)):
            self._grid[0][i] = line[i]

    def next_config(self):

        print("next config")
        
        future_config = self.retrieve_config(0).next()
        # shift configs towards the bottom
        for y in range(self._height-1, 0, -1):
            for x in range(0, self._width):
                self._grid[y][x] = self._grid[y-1][x]
        # update the most recent config
        self.set_config(future_config)
        self.repaint()


if __name__ == "__main__":
    ui = UI()
        

