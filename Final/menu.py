from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
from GUI21 import main21
from warGUI import intialize
from globalFunctions import *
import subprocess
global rootMenu,  outPutMenu, endMenu, btnWar, btn21, warning, warningOut, menuProcess
warningOut = 0
endMenu = 0 #when the menu is gonna be quit so we can end the threads
outPutMenu = queue.Queue()  # output queue will hold messages that a thread will output with voice
def outPutAudioMenu():
    global outPutMenu, endMenu, var, menuProcess
    while True:
        if var.get() != 0 and warningOut:
            warning.destroy() #warning that no audio choice is selected can be removed
        if endMenu:
            return
        while outPutMenu.empty() == False:
            msg = outPutMenu.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            menuProcess = subprocess.Popen(["mpg123", "test.mp3"])

         

#Thread function- changes the audio setting and chooses game based on user voice input
def audioListenerMenu():
    global endMenu, warning, menuProcess
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        msg = getInput(("audio", "silent", "silence", "first", "second", "quit"))
        print(msg)
        if endMenu:
            return
        if msg == "quit":
            menuProcess.terminate()
            quitMenu()
            return
        if msg == "audio":
            #audioChoice = "Vaudio" #!!differentiate audio from button and audio from voice
            var.set(1)
            if warningOut:
                warning.destroy()
            outPutMenu.put("Audio Selected")
        elif msg == "silent" or msg == "silence":
            #audioChoice = "Vsilent" #!!differentiate audio from button and audio from voice
            var.set(2)
            if warningOut:
                warning.destroy()
            outPutMenu.put("Silent Selected")
        if msg == "first":
            btn21.invoke()
            return
        if msg == "second":
            btnWar.invoke()
            return

def quitMenu():
    global rootMenu
    global endMenu
    menuProcess.terminate()
    endMenu = 1
    rootMenu.destroy()


def choose_21():
    global outputMenu, endMenu, rootMenu, warning, warningOut, menuProcess
    menuProcess.terminate()
    value = var.get()
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. Say 'audio' or 'silent' or click the radio buttons", font=("Arial", 10))
        warning.place(relx= .1, rely= .25)
        warningOut = 1
    else:  
        rootMenu.destroy()
        endMenu = 1
        main21(value)
    return

def choose_war():
    global outPutMenu, endMenu, warning, warningOut, menuProcess
    menuProcess.terminate()
    value = var.get()
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. Say 'audio' or 'silent' or click the radio buttons", font=("Arial", 10))
        warning.place(relx= .1, rely= .25)
        warningOut = 1

    else:
        rootMenu.destroy()
        endMenu = 1
        intialize(value)
    return

def main():
    global outPutMenu, endMenu, var, rootMenu, btnWar, btn21, menuProcess
    listenerThread = threading.Thread(target=audioListenerMenu) #listener thread 
    listenerThread.start()
    rootMenu = Tk()
    rootMenu.title('PLAY')
    rootMenu['background']='#8B0000'
       # window width of screen
    window_width= rootMenu.winfo_screenwidth()
    # window height of screen              
    window_height= rootMenu.winfo_screenheight()
    # set rootWar winow to screen size           
    rootMenu.geometry("%dx%d" % (window_width,  window_height))
    rootMenu.state("zoomed")
    ##THREAD SECTION
    gameTitle = Label(rootMenu, text= "POPCARD GAMES", font=("Cooper Black", 50))
    gameTitle.place(relx= .2, rely= 0)
    var = IntVar() #tkinter variable to keep track of which radio button is selected
    var.set(0)
    audioSpeakerThread = threading.Thread(target=outPutAudioMenu) #speaker thread
    audioSpeakerThread.start()
    #adds to output queue for text to speech for audio feedback
    outPutMenu.put("Welcome to PopCard Games. At anytime say silent or audio to choose game play mode. Then say first to choose 21 and second to choose war")
    #adds to gui for visual feedback
    menuInstruction = Label(rootMenu, text= "Welcome to PopCard Games. At anytime say silent or audio to choose game play mode or click the respective button.\
    THEN say first to choose 21 and second to choose war.", font=("Arial", 10))
    menuInstruction.place(relx= .1, rely= .2)

    #radio buttons for the options of audio and silent
    audioButton = Radiobutton(rootMenu, text ="Audio", font=("Helvetica", 50), variable=var, value=1)
    audioButton.place(relx = 0.05, rely = .3)
    slientButton = Radiobutton(rootMenu, text ="Silent",  font=("Helvetica", 50), variable=var, value=2)
    slientButton.place(relx = .55, rely = .3)
    #actual buttons for the options 21 and war
    btn21 = Button(rootMenu, text =" 21 ", font=("Helvetica", 50), command=lambda: choose_21())
    btn21.place(relx = .05, rely = .55)
    btnWar = Button(rootMenu, text ="WAR", font=("Helvetica", 50), command=lambda: choose_war())
    btnWar.place(relx = .55, rely = .55)
    rootMenu.mainloop()
    menuProcess.terminate()
    endMenu = 1 #this code will only be reached if user uses x to close the window
    return
if __name__ == "__main__":
    main()
    os._exit(0)