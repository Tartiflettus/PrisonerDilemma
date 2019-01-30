# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:29:50 2019

@author: perso
"""

import tkinter as tk
import PrisonerDilemma as pd

class UI:
    def __init__(self, width=16, height=10):
        self._win = tk.Tk()
        #self._win.pack(fill=tk.BOTH, expand=True)
        #paned windows
        self._pantop = tk.Frame(self._win)
        self._pantop.pack(side=tk.TOP)
        self._panbot = tk.Frame(self._win)
        self._panbot.pack(side=tk.BOTTOM)
        
        #next configuration button
        btnNextConfig = tk.Button(self._pantop, text="NEXT", command=self.nextConfig)
        btnNextConfig.pack()
        
        #simple label
        lab = tk.Label(self._pantop, text="Most recent configuration")
        lab.pack()
        
        #init the grid
        self._width = width
        self._height = height
        self._grid = [[None for i in range(width)] for j in range(height)]
        self._values = [[None for i in range(width)] for j in range(height)]
        for y in range(height):
            for x in range(width):
                self._values[y][x] = tk.IntVar()
                self._grid[y][x] = tk.Checkbutton(self._panbot, variable=self._values[y][x])
                self._grid[y][x].grid(row=y, column=x)
                
        self._win.mainloop()
    
    
    
    def retrieveConfig(self, y):
        config = pd.Configuration(self._width, 2, 1.1)
        for x in range(self._width):
            config.setCell(x, self._values[y][x].get())
        return config
    
    
    def setConfig(self, config):
        line = config.getLine()
        for i in range(len(line)):
            self._values[0][i].set(line[i])
            
            
    def nextConfig(self):
        
        futureConfig = self.retrieveConfig(0).next()
        #shift configs towards the bottom
        for y in range(self._height-1, 0, -1):
            for x in range(0, self._width):
                self._values[y][x].set(self._values[y-1][x].get())
        #update the most recent config
        self.setConfig(futureConfig)
        #print(futureConfig.getLine())
        
        
        
        
if __name__ == "__main__":
    ui = UI()
        

