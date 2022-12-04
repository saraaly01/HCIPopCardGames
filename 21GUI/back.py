from tkinter import *
from PIL import Image, ImageTk
from GUI21 import *
import pydealer
from gtts import gTTS
import os
import speech_recognition as sr


def getInput():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    #implements error handling in case the audio parser throws an error
    try:
        return r.recognize_google(audio, language="en")
    except:
        return ""

def playOutput(textInp):
    #function transforms text to speech from the "support specialist"
    myobj = gTTS(text=textInp, lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")

def start():
    main(root)


root = Tk()
root.title('PLAY')
root['background']='#8B0000'
root.geometry("200x200")
submit = Button(root, text ="PLAY 21", command = start)
submit.place(relx = .42, rely = .5)
root.mainloop()