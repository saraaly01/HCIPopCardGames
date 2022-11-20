# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 10:23:33 2022

@author: Yehuda

This is a class to simulate the backend of the application, for testing purooses.
The endgoal is to hook an object of this class up to a button on a website that
when clicked, increments the counter.
"""

class Counter:
    def __init__(self, value = 0):
        self.value = value
    
    def incrementValue(self):
        self.value += 1
        
    def getValue(self):
        return self.value

    