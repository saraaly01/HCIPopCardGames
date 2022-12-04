from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
from GUI21 import main21
from warGUI import intialize
from audioListener import *
global rootMenu,  outPutMenu, var, endMenu, btnWar, btn21
endMenu = 0
outPutMenu = queue.Queue()  # output queue will hold messages that a thread will output with voice
def outPutAudioMenu():
    global outPutMenu, endMenu
    while True:
        if endMenu:
            return
        while outPutMenu.empty() == False:
            msg = outPutMenu.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            os.system("mpg123 test.mp3")


#Thread function- changes the audio setting and chooses game based on user voice input
def audioListenerMenu():
    global endMenu
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        msg = getInput(("audio", "silent", "silence", "first", "second", "quit"))
        print(msg)
        if msg == "quit":
            quit()
            return
        if msg == "audio":
            #audioChoice = "Vaudio" #!!differentiate audio from button and audio from voice
            var.set(1)
            #outputCurSetting()
        elif msg == "silent" or msg == "silence":
            #audioChoice = "Vsilent" #!!differentiate audio from button and audio from voice
            var.set(2)
        if msg == "first":
            btn21.invoke()
            return
        if msg == "second":
            btnWar.invoke()
            return
        if endMenu:
            return
    
def quit():
    global rootMenu
    global endMenu
    endMenu = 1
    rootMenu.destroy()


def choose_21():
    global outputMenu, endMenu
    print(var.get())
    if var.get() == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
    else:
        rootMenu.destroy()
        endMenu = 1
        main21(var.get())
    return

def choose_war():
    global outPutMenu, endMenu
    if var.get() == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
    else:
        rootMenu.destroy()
        endMenu = 1
        intialize(var.get())
    return

def main():
    global outPutMenu, endMenu, var, rootMenu, btnWar, btn21
    listenerThread = threading.Thread(target=audioListenerMenu)
    listenerThread.start()
    audioSpeakerThread = threading.Thread(target=outPutAudioMenu)
    audioSpeakerThread.start()
    outPutMenu.put("Welcome to PopCard Games. Say silent or audio to choose game play mode. Then say first to choose 21 and second to choose war")
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
    gameTitle = Label(rootMenu, text= "POPCARD GAMES", font=("Comic Sans MS", 30))
    gameTitle.place(relx = 0.3, rely = 0)
    var = IntVar()
    audioButton = Radiobutton(rootMenu, text ="Audio", variable=var, value=1)
    audioButton.place(relx = .2, rely = .3)
    slientButton = Radiobutton(rootMenu, text ="Slient", variable=var, value=2)
    slientButton.place(relx = .2, rely = .35)
    btn21 = Button(rootMenu, text ="21", font=("Comic Sans MS", 30), command=lambda: choose_21())
    btn21.place(relx = .2, rely = .55)
    btnWar = Button(rootMenu, text ="WAR", font=("Comic Sans MS", 30), command=lambda: choose_war())
    btnWar.place(relx = .75, rely = .55)
    rootMenu.mainloop()
    endMenu = 1
    return
if __name__ == "__main__":
    main()
    os._exit(0)