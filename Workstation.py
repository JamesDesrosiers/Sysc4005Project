# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:35:58 2022

@author: amire
"""
import numpy as np
import queue.PriorityQueue

"c1: idle if c1q buffer is empty"
"c2: idle if c1q or c2q is empty"
"c3: idle if c1q or c3q is empty"

class workstation1:
    
 def __init__(self,logger,simulationVar,state):
        self.logger = logger
        self.simulationVar = simulationVar
        self.state = state 
        self._c1Queue = []
    
    def activate(self,time):
    
    def state(self):
       