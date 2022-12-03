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
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("ENTERED")
    while True:
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source=source, duration=1)
                audio = r.listen(source, timeout=5)
                msg = r.recognize_google(audio, language='en')
                print(msg)
            except:
                msg = "-"
        if msg == "yes":
            start_21()
            return


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


audioListenerThread = threading.Thread(target=audioListener)
audioListenerThread.start()
print("thread created")
#audioSpeakerThread = threading.Thread(target=outPutAudio)
#audioSpeakerThread.start()
submit = Button(root, text ="PLAY 21", command=lambda: start_21())
submit.place(relx = .42, rely = .5)
root.mainloop()

#speak("Welcome to Popcard Games! Say one for twenty one and two for war")