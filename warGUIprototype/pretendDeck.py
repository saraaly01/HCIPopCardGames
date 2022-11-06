# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 13:27:35 2022

@author: Yehuda
"""

import random

#PretendDeck object- creates a list of 26 random numbers. Call the removeFromTop function to pop off the list.
class PretendDeck:
    def __init__(self):
        self.deck = []
        for i in range(0,26):
            n = random.randint(1,30)
            self.deck.append(n)
    
    #adds a card to the bottom of the deck
    def addToBottom(self, card):
        self.deck.append(card)
    
    #removes a card from the bottom of the deck
    def removeFromTop(self):
        return self.deck.pop(0)
    
    #gets the state of the deck
    def getDeckState(self):
        return self.deck