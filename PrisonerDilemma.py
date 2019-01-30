# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 18:47:39 2019

@author: perso
"""

import copy as cp


class Configuration:
    def __init__(self, size, neighbor, T):
        self._line = [0] * size
        self._neighbor = neighbor
        self._T = T
        
    def payoff(self, i, j):
        a = self._line[i]
        b = self._line[j]
        return a*b + self._T*(1 - a*b)*b
    
    def neighborhood(self, i):
        if self._neighbor % 2 != 0: #continuous range
            ans = list(range(i-self._neighbor//2, 1+i+self._neighbor//2))
        else:
            ans = list(range(i-self._neighbor//2, i)) + list(range(1 + i , 1 + i + self._neighbor//2))
        return [x % len(self._line) for x in ans]
        
    
    def totalPayoff(self, i):
        neighborhood = self.neighborhood(i)
        return sum([self.payoff(i, j) for j in neighborhood])
    
    def next(self):
        ans = Configuration(len(self._line), self._neighbor, self._T)
        ans._neighbor = self._neighbor
        ans._T = self._T
        ans._line = cp.copy(self._line)
        
        payoffs = [self.totalPayoff(i) for i in range(len(self._line))]
        #update if payoff > other payoffs
        for i in range(len(self._line)):
            #[payoffs[x] for x in self.neighborhood()]
            #compute max payoff and get its index
            m = -1
            imax = -1
            for j in self.neighborhood(i):
                if payoffs[j] > m:
                    m = payoffs[j]
                    imax = j
            #update cell state if its payoff is not best
            if payoffs[i] < m:
                ans._line[i] = self._line[imax]

        return ans

if __name__ == "__main__":
    #test
    c = Configuration(8, 4, 1.1)
    for i in range(len(c._line)):
        c._line[i] = 1
    c._line[4] = 0
    c._line[2] = 0
    
    print([c.totalPayoff(i) for i in range(len(c._line))])
    print("")
    print(c._line)
    for i in range(4):
        c = c.next()
        print(c._line)
    print("")
    print([c.totalPayoff(i) for i in range(len(c._line))])
