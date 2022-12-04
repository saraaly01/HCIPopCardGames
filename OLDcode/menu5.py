#import theGame21
import theGame21v2

from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('500x200')

def run_21():
    #theGame21.main()
    theGame21v2.main()

def run_war():
    print("Need code for the game War")

btn = Button(window, text="The Game 21", bg="black", fg="white",command=run_21)
btn.grid(column=0, row=0)

btn2 = Button(window, text="War", bg="black", fg="white",command=run_war)
btn2.grid(column=0, row=2)

window.mainloop()