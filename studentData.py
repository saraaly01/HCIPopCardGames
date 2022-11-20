# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 10:40:58 2022

@author: Yehuda
"""

from flask import Flask, render_template, request
import counter
app = Flask(__name__)
counter1 = counter.Counter()

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    
    if request.method == 'POST':
        counter1.incrementValue()
    value = counter1.getValue()
    return render_template("result.html", result = value)


if __name__ == '__main__':
   app.run(debug = True)