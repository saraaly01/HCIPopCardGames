from tkinter import *
from PIL import Image, ImageTk
from saraTestingGUI import *
import pydealer
# width of window

def start():
    intialize(root)


root = Tk()
root.title('INSTRUCTIONS')
root['background']='#8B0000'
window_width = root.winfo_screenwidth()
window_height= root.winfo_screenheight()
root.geometry("%dx%d" % (window_width,  window_height))
submit = Button(root, text ="PLAY WAR", command = start)
submit.grid()
root.mainloop()