from tkinter import *
from PIL import Image, ImageTk
from GUI21 import *
import pydealer

def start():
    main(root)


root = Tk()
root.title('PLAY')
root['background']='#8B0000'

root.geometry("200x200")
submit = Button(root, text ="PLAY 21", command = start)
submit.place(relx = .42, rely = .5)
root.mainloop()