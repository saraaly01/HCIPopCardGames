from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading, subprocess

global instructionProcess
outputInstruct21 =  queue.Queue() 
def outPutAudioWarInstruct21():
    global outputInstruct21, instructionProcess
    while True:
        while outputInstruct21.empty() == False:
            msg = outputInstruct21.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)  
            myobj.save("test.mp3")
            instructionProcess = subprocess.Popen(["mpg123", "test.mp3"])
            return

def instructions21(audioChoice):
    global instructionProcess
    root21I = Tk()
    root21I.title('Instructions 21')
    root21I['background']='#8B0000'
    root21I.geometry("1000x1000")
    instructionsGeneral = "Rules of 21:\n \
    Cards values of 2-9 are worth 2points-9pointts, respectively.\n\
    King, Jack, and Queen are each worth 10points.\n \
    Aces are worth 1point or 11points, depending what is most benefical to the player\n\n\
    \
    The player is dealt two cards face up.\n\
    The dealer is dealt 1 card face up and one face down..\n\n\
    \
    The player can choose to hit (take another card) or stand (defer to the dealer) to try to get as \nclose to the value 21 as possible but not over.\n \
    \
    Once the player stands, the dealer has to hit to get as close to 21 as possible but not over.\n\
    Once the dealer's hand value is over 16, the dealer has to stand.\n\n\
    \
    If the player or dealer hand goes over 21, that defines a bust which is a loss.\n\
    If the player has a higher score than the dealer and less than 21, then the player wins (and vice versa)\n\
    If the player or dealer hits exactly 21, that defines an automatic win\n\
    If the player or dealer have the same score, that defines a push, which is a tie.\n"
    
    instructionsApplication = "Press the hit button to receive a card. Press the stand button to stand.\n\
    If playing with audio, At any time say 'yes' to hit and say 'no' to stand. To quit say 'quit' or close out window."

    instructionString =  "Rules of 21:\
    Cards values of 2-9 are worth 2points-9points, respectively.\
    King, Jack, and Queen are each worth 10pts. \
    Aces are worth 1point or 11points, depending what is most benefical to the player\n\n\
    \
    The player is dealt two cards face up.\
    The dealer is dealt 1 card face up and one face down..\
    \
    The player can choose to hit (take another card) or stand (defer to the dealer) to try to get as \nclose to the value 21 as possible but not over.\n \
    \
    Once the player stands, the dealer has to hit to get as close to 21 as possible but not over.\n\
    Once the dealer's hand value is over 16, the dealer has to stand.\
    \
    If the player or dealer hand goes over 21, that defines a bust which is a loss.\
    If the player has a higher score than the dealer and less than 21, then the player wins (and vice versa)\
    If the player or dealer hits exactly 21, that defines an automatic win\
    If the player or dealer have the same score, that defines a push, which is a tie.\n \
    Press the hit button to receive a card. Press the stand button to stand.\n\
    If playing with audio, at any time say 'yes' to hit, say 'no' to stand, and say 'score' for the score. To quit say 'quit' or close out window."
    placeGeneral = Label(root21I, text = instructionsGeneral, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeGeneral.place(relx= 0, rely=0)
    placeApplication = Label(root21I, text = instructionsApplication, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeApplication.place(relx= 0, rely=.6)
    if audioChoice:
        outputInstruct21.put(instructionString)
        audioSpeakerThread = threading.Thread(target=outPutAudioWarInstruct21)
        audioSpeakerThread.start()
    root21I.mainloop()
    instructionProcess.terminate()
         