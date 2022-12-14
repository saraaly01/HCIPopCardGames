
import pydealer
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
import re

# If the function is acting up. Uncomment lines 29 and 30 in order to see more of whats happening.

# given a list of desired words, getInput will get audio input from the user and 
# parse the input to determine whether the input contains one or more of the desired words
# ex: the getInput(('yes', 'no')) function is run on various audio input.

# "Yes" -> getInput('yes', 'no') == 'yes'
# "Yes yes yes" -> getInput('yes', 'no') == 'yes'
# "Yes push the button" -> getInput('yes', 'no') == 'yes'
# "yes no push the button" -> getInput('yes', 'no') == 'More than one desired word was found.'
# "hello, my name is Bob" -> getInput('yes', 'no') == 'No desired word was found.'

# Note: getInput function will not work if a word in desiredWords is a contraction such as don't, isn't or mustn't
# I can make this function work with contractions in the future, but I'll do it once there is no other work to do.
def getInput(desiredWords):    
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:   
        try:
            audio = r.listen(source)
            rawAudioInput = r.recognize_google(audio, language="en")
            #print("raw output " + rawAudioInput) prints raw output
            #splits the audio into a list of words
            splitInput = re.split("[\W]+", rawAudioInput)
            # keeps track of all the words from desiredWords that were found in the audio input
            foundWord = ""
            for inputWord in splitInput:
                for desiredWord in desiredWords:
                    # if the current word from the input is a match:
                    if inputWord.lower() == desiredWord.lower():
                        foundWord = inputWord

            if foundWord == "":
                myobj = gTTS(text="Sorry, I did'nt quite get that.", lang='en', tld='us', slow=False)
                myobj.save("test.mp3")
                os.system("mpg123 test.mp3")
                return "No desired word was found."
            else:
                return foundWord
        
        #implements error handling in case the audio parser throws an error
        except sr.RequestError:
            return "-"
        except sr.UnknownValueError:
            return "-"

#prepares image for label to placed on GUI
def insertImage(cardPlayed,rootType):
    width = int(250/2.5)
    height = int(363/2.5)
    cardOutput = Image.open("cards\\" + str(cardPlayed) + ".png")
    test = cardOutput.resize((width, height))
    test = ImageTk.PhotoImage(test)
    imglabel = Label(rootType, image=test, borderwidth=0, highlightthickness=0)
    imglabel.image = test
    return imglabel


