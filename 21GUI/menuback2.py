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


global root, end, outPut, k, gameDecision, audioChoice, gameChoice
audioChoice = "--"
gameChoice = "--"

#Outputs audio- not used yet (it would probably just output something simple like "Hi!! Welcome to PopCard Games. Select an audio option and a game.")
def outPutAudio():
    global end
    print("The thread has called outPutAudio")
    while True:
        while output.empty() == False:
            msg = output.get(0)
            speak(msg)
        if end:
            return

#speak funct
def speak(x):

    myobj = gTTS(text=str(x), lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")

#Outputs the current audiochoice (submitted by the button or through speaking)
def outputCurSetting():
    global audioChoice
    print("AUDIO CHOICE IS: " + audioChoice)
    audioStringOutput = "Current audio choice is " + audioChoice
    curAudioSetting = Label(root, text=audioChoice, font=("Comic Sans MS", 10))
    curAudioSetting.place(relx=.65, rely=.2)

#Thread function- changes the audio setting and chooses game based on user voice input
def audioListener():
    global audioChoice
    global gameChoice
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
                msg = "--"

        if msg == "audio":
            #audioChoice = "Vaudio" #!!differentiate audio from button and audio from voice
            voiceAudioChoice = "0"
            set_audio_voice(voiceAudioChoice)
            #outputCurSetting()
        elif msg == "silent" or msg == "silence":
            #audioChoice = "Vsilent" #!!differentiate audio from button and audio from voice
            voiceAudioChoice = "1"
            set_audio_voice(voiceAudioChoice)
            #outputCurSetting()
        elif msg == "21":
            choose_21()
            return
        elif msg.lower() == "war":
            choose_war()
            return

#sets the audio choice with the button
def set_audio():
    global audioChoice
    #if selected_audio_setting.get() == '0' or audioChoice == "Vaudio": #!!differentiate audio from button and audio from voice
    if selected_audio_setting.get() == '0':
        #print(type(selected_audio_setting.get()))
        audioChoice = "audio"
        print("With audio")
        outputCurSetting()
    #elif selected_audio_setting.get() == '1' or audioChoice == "Vsilent": #!!differentiate audio from button and audio from voice
    elif selected_audio_setting.get() == '1':
        #print(type(selected_audio_setting.get()))
        audioChoice = "silent"
        print("WithOUT audio")
        outputCurSetting()

def set_audio_voice(x):
    global audioChoice
    if x == "0":
        audioChoice = "audio"
        outputCurSetting()
    elif x == "1":
        audioChoice = "silent"
        outputCurSetting()

#NOTE: refactor choose_21 and choose_war into one - ERROR IS HERE
#Function called when War/21 button is pressed
def choose_21():
    print("TWENTY ONE CHOSEN!!")
    global gameChoice
    gameChoice = "21"
    print("This is what audioChoice is stored as:" + audioChoice)
    print("This is audioChoice's type:" + str(type(audioChoice)))
    if audioChoice == "--":
        print("No audio choice selected, setting to audio by default")
    #if audioChoice == "audio" or "Vaudio": #for some reason, the program treats the audioChoice as a list of options. Switching from audio to no audio stores both
    if audioChoice == "audio":
        print("Audio selected")
    #if audioChoice == "silent" or "Vsilent": #for some reason, the program treats the audioChoice as a list of options. Switching from audio to no audio stores both
    if audioChoice == "silent":
        print("No Audio/Silent selected")

    #Weird bug that may not matter- when you select audio with voice, it executes this else
    #else:
        #print("Something's wrong- there was no selection and the audio default isn't set")

def choose_war():
    print("WAR CHOSEN!!")
    global gameChoice
    gameChoice = "war"
    if audioChoice == "--":
        print("No audio choice selected, setting to audio by default")
    if audioChoice == "audio" or "Vaudio":
        print("Audio selected")
    if audioChoice == "silent" or "Vsilent":
        print("No Audio/Silent selected")
    else:
        print("Something's wrong")


root = Tk()
root.title('PLAY')
root['background']='#8B0000'

root.geometry("900x600")

#NOTE: including root, "0" selects audio from the beginning- the problem is it can't be changed
#selected_size = StringVar(root, "0")

gameTitle = Label(root, text= "POPCARD GAMES", font=("Comic Sans MS", 30))
gameTitle.place(relx = 0.3, rely = 0)

###RADIO BUTTON SECTION
selected_audio_setting = StringVar()
audio_settings = (('Audio (Voice Input/Output)', '0'),
         ('Silent', '1'))

# radio buttons
radio_y_inc = 0
for setting in audio_settings:
    r = Radiobutton(
        root,
        text=setting[0],
        value=setting[1],
        variable=selected_audio_setting
    )
    r.pack(fill='x', padx=1, pady=1)
    r.place(relx = .3, rely = .15 + radio_y_inc)
    radio_y_inc = radio_y_inc + 0.05

##THREAD SECTION
audioListenerThread = threading.Thread(target=audioListener)
audioListenerThread.start()
print("thread created")
#audioSpeakerThread = threading.Thread(target=outPutAudio)
#audioSpeakerThread.start()


defaultAudioSetting = Label(root, text="Current audio choice is:", font=("Comic Sans MS", 10))
defaultAudioSetting.place(relx=.6, rely=.15)

defaultAudioSetting = Label(root, text="audio", font=("Comic Sans MS", 10))
defaultAudioSetting.place(relx=.65, rely=.2)

submit = Button(root, text ="Submit Audio Choice", font=("Comic Sans MS", 20), command=lambda: set_audio())
submit.place(relx = .35, rely = .28)

btn21 = Button(root, text ="21", font=("Comic Sans MS", 30), command=lambda: choose_21())
btn21.place(relx = .2, rely = .55)
btnWar = Button(root, text ="WAR", font=("Comic Sans MS", 30), command=lambda: choose_war())
btnWar.place(relx = .75, rely = .55)

if gameChoice == "21":
    print("Calling 21 game with audio input selected")
elif gameChoice == "war":
    print("Calling war game with audio input selected")

#outputCurSetting() #Doesn't work- problem is it doesn't update to the current audio setting

root.mainloop()

#speak("Welcome to Popcard Games! Say one for twenty one and two for war")