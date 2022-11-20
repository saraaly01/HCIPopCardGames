# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 14:28:56 2022

@author: Yehuda
"""

# window generator
# button that makes something happen
# text box that saves the input and displays the input (think input_name)
# change background texture

from flask import Flask, redirect, url_for
from flask import request
#from flask import render_template
import webbrowser
import os

app = Flask(__name__)

@app.route('/hello/<name>')
def hello_world(name):
   return 'Hello %s!' % name

@app.route('/html')
def open_html():
    return webbrowser.open('file://' + os.path.realpath('hello.html'))


@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest = name))
    
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))
        
    


if __name__ == '__main__':
   app.run(debug = True)