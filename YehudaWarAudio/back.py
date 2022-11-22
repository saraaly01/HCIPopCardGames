from tkinter import *
from PIL import Image, ImageTk
from warWITHAUDIO import *
import pydealer

def start():
    intialize(root)


root = Tk()
root.title('PLAY')
root['background']='#8B0000'

root.geometry("200x200")
submit = Button(root, text ="PLAY WAR", command = start)
submit.place(relx = .42, rely = .5)
root.mainloop()