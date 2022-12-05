from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
from GUI21 import main21
from warGUI import intialize
from globalFunctions import *

global rootMenu,  outPutMenu, endMenu, btnWar, btn21, warning
endMenu = 0
outPutMenu = queue.Queue()  # output queue will hold messages that a thread will output with voice
def outPutAudioMenu():
    global outPutMenu, endMenu, var
    while True:
        if var.get() != 0:
            warning.destroy()
        if endMenu:
            return
        while outPutMenu.empty() == False:
            msg = outPutMenu.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            btn21['state'] = DISABLED
            btnWar['state'] = DISABLED
            os.system("mpg123 test.mp3")
            btn21['state'] = NORMAL
            btnWar['state'] = NORMAL


#Thread function- changes the audio setting and chooses game based on user voice input
def audioListenerMenu():
    global endMenu, warning
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        msg = getInput(("audio", "silent", "silence", "first", "second", "quit"))
        print(msg)
        if msg == "quit":
            quitMenu()
            return
        if msg == "audio":
            #audioChoice = "Vaudio" #!!differentiate audio from button and audio from voice
            var.set(1)
            warning.destroy()
            outPutMenu.put("Audio Selected")
        elif msg == "silent" or msg == "silence":
            #audioChoice = "Vsilent" #!!differentiate audio from button and audio from voice
            var.set(2)
            warning.destroy()
            outPutMenu.put("Silent Selected")
        if msg == "first":
            btn21.invoke()
            return
        if msg == "second":
            btnWar.invoke()
            return
        if endMenu:
            return
    
def quitMenu():
    global rootMenu
    global endMenu
    endMenu = 1
    rootMenu.destroy()


def choose_21():
    global outputMenu, endMenu, rootMenu, warning
    value = var.get()
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. Say 'audio' or 'silent' or click the radio buttons", font=("Arial", 10))
        warning.place(relx= .1, rely= .25)
    else:
        rootMenu.destroy()
        endMenu = 1
        main21(value)
    return

def choose_war():
    global outPutMenu, endMenu, warning
    value = var.get()
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. Say 'audio' or 'silent' or click the radio buttons", font=("Arial", 10))
        warning.place(relx= .1, rely= .25)
    else:
        rootMenu.destroy()
        endMenu = 1
        intialize(value)
    return

def main():
    global outPutMenu, endMenu, var, rootMenu, btnWar, btn21
    listenerThread = threading.Thread(target=audioListenerMenu)
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
    var = IntVar()
    var.set(0)
    audioSpeakerThread = threading.Thread(target=outPutAudioMenu)
    audioSpeakerThread.start()
    outPutMenu.put("Welcome to PopCard Games. At anytime say silent or audio to choose game play mode. Then say first to choose 21 and second to choose war")
    menuInstruction = Label(rootMenu, text= "Welcome to PopCard Games. At anytime say silent or audio to choose game play mode or click the respective button.\
    THEN say first to choose 21 and second to choose war.", font=("Arial", 10))
    menuInstruction.place(relx= .1, rely= .2)
    audioButton = Radiobutton(rootMenu, text ="Audio", font=("Helvetica", 50), variable=var, value=1)
    audioButton.place(relx = 0.05, rely = .3)
    slientButton = Radiobutton(rootMenu, text ="Silent",  font=("Helvetica", 50), variable=var, value=2)
    slientButton.place(relx = .55, rely = .3)
    btn21 = Button(rootMenu, text =" 21 ", font=("Helvetica", 50), command=lambda: choose_21(), state=DISABLED)
    btn21.place(relx = .05, rely = .55)
    btnWar = Button(rootMenu, text ="WAR", font=("Helvetica", 50), command=lambda: choose_war(), state=DISABLED)
    btnWar.place(relx = .55, rely = .55)
    rootMenu.mainloop()
    endMenu = 1
    return
if __name__ == "__main__":
    main()
    os._exit(0)