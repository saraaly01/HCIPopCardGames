from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading, subprocess

global outPutAudioWarInstructWar, instructionProcess
instructionProcess = ""
outputInstructWar =  queue.Queue() 

def outPutAudioWarInstructWar(rootWarI):
    global outputInstructWar, instructionProcess
    while True:
        while outputInstructWar.empty() == False:
            msg = outputInstructWar.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)  
            myobj.save("test.mp3")
            instructionProcess = subprocess.Popen(["mpg123", "test.mp3"])
            return

#prints and/or speaks the instructions for the game 'war'
def instructionsWar(audioChoice):
    global outputInstructWar,instructionProcess
    rootWarI = Tk()
    rootWarI.title('Instructions War')
    rootWarI['background']='#8B0000'
    rootWarI.geometry("1000x1000")
    rootWarI.state("zoomed")
    instructionString = "Rules of War: \
    The deck is split evenly. The player and computer flips a card and the higher card gets both cards.\
    If there is a tie, the computer and player flip four cards and the fourth card is compared.\
    Whoever has the fourth card gets all the cards played in that round. If there is a tie, everyone gets their cards back.\
    Whoever ends up with no cards first, loses! Press the flip button to flip your card (the computer will flip their card too).\n \
    If playing with audio say flip to do the same. When a war commences, say war or hit the war button to continue. \n\
    At any point, if playing with audio say score to see how many cards the player and computer each have."
    if audioChoice == 1:
        outputInstructWar.put(instructionString)
        audioSpeakerThreadWar = threading.Thread(target=outPutAudioWarInstructWar, args=(rootWarI, ))
        audioSpeakerThreadWar.start()

    instructionsGeneral = "Rules of War:\n \
    The deck is split evenly. The player and computer flips a card and the higher card gets both cards.\n\
    If there is a tie, the computer and player flip four cards and the fourth card is compared. \n\
    Whoever has the fourth card gets all the cards played in that round If there is a tie, everyone gets their cards back.\n\
    Whoever ends up with no cards first, loses!\n"
    instructionsApplication = "With Press the flip button to flip your card (the computer will flip their card too).\n \
    If playing with audio say flip to do the same. When a war commences, say war to continue or hit the war button. \n\
    At any point, if playing with audio say score to see how many cards the player and computer have each."
    placeGeneral = Label(rootWarI, text = instructionsGeneral,font=("Tahoma", 18), bg='#8B0000', foreground="white")
    placeGeneral.place(relx= 0, rely=0)
    placeApplication = Label(rootWarI, text = instructionsApplication,font=("Tahoma", 18), bg='#8B0000', foreground="white")
    placeApplication.place(relx= 0, rely=.6)
    rootWarI.mainloop()
    if instructionProcess != "":
        instructionProcess.terminate()
