from tkinter import *
from PIL import Image, ImageTk
from GUI21 import *
import pydealer
from gtts import gTTS
import os
import speech_recognition as sr




def start():
    root.destroy()
    main()
    return    



root = Tk()
root.title('PLAY')
root['background']='#8B0000'
root.geometry("200x200")
submit = Button(root, text ="PLAY 21", command = start)
submit.place(relx = .42, rely = .5)
root.mainloop()
os._exit(0)