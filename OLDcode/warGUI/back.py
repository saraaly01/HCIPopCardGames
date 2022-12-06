from tkinter import *
from PIL import Image, ImageTk
from GUIwar import *
import pydealer, sys

def start():
    root.destroy()
    intialize()
    return    




root = Tk()
root.title('PLAY')
root['background']='#8B0000'

root.geometry("200x200")
submit = Button(root, text ="PLAY WAR", command = start)
submit.place(relx = .42, rely = .5)
root.mainloop()
os._exit(0)