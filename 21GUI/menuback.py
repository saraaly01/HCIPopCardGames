<<<<<<< HEAD
from tkinter import *
from PIL import Image, ImageTk
from GUI21 import *
import pydealer

from enum import Enum
from tkinter import *
from PIL import Image, ImageTk
import time
import numpy as np
import speech_recognition as sr
import os
import sys
from gtts import gTTS
import queue
import time
from playsound import playsound
import threading

global root, end, outPut, k, gameDecision
r = sr.Recognizer()
mic = sr.Microphone()
=======
import pydealer
from enum import Enum
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os
from gtts import gTTS
import time
import queue
import threading


global root, end, outPut, k, gameDecision

>>>>>>> 188a7e7cd9b5d7fc32f9dedaf48e202f89ac6ea6

def outPutAudio():
    global end
    print("The thread has called outPutAudio")
    while True:
        while output.empty() == False:
            msg = output.get(0)
            speak(msg)
        if end:
            return


def speak(x):
    global k
    k += 1

    myobj = gTTS(text=str(x), lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")


def audioListener():
<<<<<<< HEAD
    """
    This is where we handle the asynchronous I/O. For example, it may be
    a 'select(  )'. One important thing to remember is that the thread has
    to yield control pretty regularly, by select or otherwise.
    """
    #print("the thread has called audioListener")
    msg = ''
    while True:
        #print("Taking in speaking input")
=======
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("ENTERED")
    while True:
>>>>>>> 188a7e7cd9b5d7fc32f9dedaf48e202f89ac6ea6
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source=source, duration=1)
                audio = r.listen(source, timeout=5)
                msg = r.recognize_google(audio, language='en')
                print(msg)
            except:
<<<<<<< HEAD
                #print("cant recognise speech")
                msg = "-"
        if msg.lower() == "yes":
            start_war()
            return
            #print("You picked 21")
            #output.put("You picked 21")
            #Call 21 here (default to audio unless the user has changed it)

        if msg == "no":
            pass
            #print("You picked war")
            #output.put("You picked war")
            #Call War here (default to audio unless the user has changed it)

=======
                msg = "-"
        if msg == "yes":
            start_21()
            return
>>>>>>> 188a7e7cd9b5d7fc32f9dedaf48e202f89ac6ea6


def start_21():
    if selected_size.get() == '0':
        print(type(selected_size.get()))
        print("21 with audio")
    elif selected_size.get() == '1':
        print(type(selected_size.get()))
        print("21 withOUT audio")

def start_war():
    if selected_size.get() == '0':
        print("war with audio")
    elif selected_size.get() == '1':
        print("war withOUT audio")

root = Tk()
root.title('PLAY')
root['background']='#8B0000'

root.geometry("600x600")

selected_size = StringVar()
sizes = (('Audio (Voice Input/Output)', '0'),
         ('Silent', '1'))

# radio buttons
for size in sizes:
    r = Radiobutton(
        root,
        text=size[0],
        value=size[1],
        variable=selected_size
    )
    r.pack(fill='x', padx=5, pady=5)

<<<<<<< HEAD
submit = Button(root, text ="PLAY 21", command=lambda: start_21())

audioListenerThread = threading.Thread(target=audioListener, args=())
=======

audioListenerThread = threading.Thread(target=audioListener)
>>>>>>> 188a7e7cd9b5d7fc32f9dedaf48e202f89ac6ea6
audioListenerThread.start()
print("thread created")
#audioSpeakerThread = threading.Thread(target=outPutAudio)
#audioSpeakerThread.start()
<<<<<<< HEAD

=======
submit = Button(root, text ="PLAY 21", command=lambda: start_21())
>>>>>>> 188a7e7cd9b5d7fc32f9dedaf48e202f89ac6ea6
submit.place(relx = .42, rely = .5)
root.mainloop()

#speak("Welcome to Popcard Games! Say one for twenty one and two for war")