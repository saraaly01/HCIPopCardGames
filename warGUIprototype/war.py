# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 13:38:29 2022

@author: Yehuda
"""

from flask import Flask, render_template, request
import pretendDeck
app = Flask(__name__)

userDeck = pretendDeck.PretendDeck()

@app.route('/', methods = ['POST', 'GET'])
def war():
    if request.method == 'POST':
        userDeck.removeFromTop()
    value = userDeck.getDeckState()


    return render_template('pretendDeckResult.html', userDeck = value)


if __name__ == '__main__':
   app.run(debug = True)