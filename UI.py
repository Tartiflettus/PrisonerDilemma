# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:29:50 2019

@author: perso
"""

import tkinter as tk

class UI:
    def __init__(self, width=16, height=10):
        self._win = tk.Tk()
        #self._win.pack(fill=tk.BOTH, expand=True)
        #paned windows
        self._pantop = tk.Frame(self._win)
        self._pantop.pack(side=tk.TOP)
        self._panbot = tk.Frame(self._win)
        self._panbot.pack(side=tk.BOTTOM)
        
        #simple label
        lab = tk.Label(self._pantop, text="Most recent configuration")
        lab.pack()
        
        #init the grid
        self._width = width
        self._height = height
        self._grid = [ [None] * width ] * height
        for y in range(height):
            for x in range(width):
                self._grid[y][x] = tk.Checkbutton(self._panbot)
                self._grid[y][x].grid(row=y, column=x)

    
        self._win.mainloop()
        

ui = UI()
        

