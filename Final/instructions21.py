from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading, subprocess

global instructionProcess
instructionProcess = ""
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

#prints and/or speaks the instructions for the game '21'
def instructions21(audioChoice):
    global instructionProcess
    root21I = Tk()
    root21I.title('Instructions 21')
    root21I['background']='#8B0000'
    root21I.geometry("1000x1000")
    root21I.state("zoomed")
    instructionsGeneral = "Rules of 21:\n \
    Cards values of 2-9 are worth 2points-9points respectively.\n\
    King, Jack, and Queen are each worth 10 points.\n \
    Aces are worth 1 point or 11 points, depending what is most benefical to the player\n\n\
    \
    The player is dealt two cards face up.\n\
    The dealer is dealt one card face up and one face down.\n\n\
    \
    The player can choose to hit (take another card) or stand (defer to the dealer) to try to get as \nclose to the value 21 as possible without going over.\n \
    \
    Once the player stands, the dealer has to hit to get as close to 21 as possible without going over.\n\
    Once the dealer's hand value is over 16, the dealer has to stand.\n\n\
    \
    If the player or dealer hand goes over 21, that defines a player or dealer bust respectively.\n\
    If the player has a higher score than the dealer without going bust, then the player wins (and vice versa)\n\
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
    If playing with audio, at any time say 'yes' to hit, say 'no' to stand,say 'score' for the score and 'quit' to quit. You can also close out the window."
    placeGeneral = Label(root21I, text = instructionsGeneral, font=("Tahoma", 18), bg='#8B0000', foreground="white")
    placeGeneral.place(relx= 0, rely=0)
    placeApplication = Label(root21I, text = instructionsApplication, font=("Tahoma", 18), bg='#8B0000', foreground="white")
    placeApplication.place(relx= 0, rely=.8)
    if audioChoice == 1:
        outputInstruct21.put(instructionString)
        audioSpeakerThread = threading.Thread(target=outPutAudioWarInstruct21)
        audioSpeakerThread.start()
    root21I.mainloop()
    if instructionProcess != "":
        instructionProcess.terminate()
         