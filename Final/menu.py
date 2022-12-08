from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
from GUI21 import main21
from warGUI import intialize
from globalFunctions import *
import subprocess
#rootMenu is the root windo of the menu
#outPutMenu is the queue to share messages with the thread
# endMenu signals when the thread should be over
# warning is the warning label that will appear if they try to hit 21 or war without picking an audio
# warningOut is determines if the warning has been posted on the screen or not so we can delete it
#menuProcess is the audio process for output
global rootMenu,  outPutMenu, endMenu, btnWar, btn21, warning, warningOut, menuProcess
menuProcess = ""
warningOut = 0
endMenu = 0 #when the menu is gonna be quit so we can end the threads
outPutMenu = queue.Queue()  # output queue will hold messages that a thread will output with voice

#audio output function
def outPutAudioMenu():
    global outPutMenu, endMenu, var, menuProcess
    while True:
        if var.get() != 0 and warningOut:
            warning.destroy() 
        if endMenu:
            return
        while outPutMenu.empty() == False:
            msg = outPutMenu.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")

            #uses subprocesss.Popen() instead of os.system() to allow for killing of the audio process when needed
            menuProcess = subprocess.Popen(["mpg123", "test.mp3"])
            menuProcess.wait()

         

#Thread function- changes the audio setting and chooses game based on user voice input
def audioListenerMenu():
    global endMenu, warning, menuProcess
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        #msg is loaded with audio input from the user. 
        msg = getInput(("audio", "silent", "silence", "first", "second", "quit"))
        #print(msg)
        
        #logic to be performed based on user input
        if endMenu:
            return
        if msg == "quit":
            menuProcess.terminate()
            quitMenu()
            return
        if msg == "audio":
            var.set(1)
            if warningOut:
                warning.destroy()
            outPutMenu.put("Audio Selected")
        elif msg == "silent" or msg == "silence":
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

#function that closes up the menu
def quitMenu():
    global rootMenu
    global endMenu
    menuProcess.terminate()
    endMenu = 1
    rootMenu.destroy()

# function that is executed when the user choses to play the game '21',
# whether through audio or button input
def choose_21():
    global outputMenu, endMenu, rootMenu, warning, warningOut, menuProcess
    # ends any currently running audio processes
    if menuProcess != "":
        menuProcess.terminate()
    value = var.get()
    # if the user has not selected a game-mode (audio or silent), the application logic prevents the game from beginning
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. \nSay 'audio' or 'silent' or click the radio buttons", font=("Tahoma", 15), bg='#8B0000', foreground="white")
        warning.place(relx= 0, rely= .435)
        warningOut = 1
    # Destroys the menu, and calls the function main21() which starts the game '21'
    else:  
        rootMenu.destroy()
        endMenu = 1
        main21(value) # main function in the GUI21 file/game
    return

# function that is executed when the user choses to play the game 'War',
# whether through audio or button input
def choose_war():
    global outPutMenu, endMenu, warning, warningOut, menuProcess
    if menuProcess != "":
        menuProcess.terminate()    
    value = var.get()
    # if the user has not selected a game-mode (audio or silent), the application logic prevents the game from beginning
    if value == 0:
        outPutMenu.put("No audio choice selected. Say 'audio' or 'silent' or click the radio buttons")
        warning = Label(rootMenu, text= "No audio choice selected. \nSay 'audio' or 'silent' or click the radio buttons", font=("Tahoma", 15), bg='#8B0000', foreground="white")
        warning.place(relx= 0, rely= .435)
        warningOut = 1
    # Destroys the menu, and calls the function initialize() which starts the game 'war'
    else:
        rootMenu.destroy()
        endMenu = 1
        intialize(value) # first function that needs to be called to initialize everythin in the warGUI file/game
    return

# main function, contains central flow for the menu
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
    gameTitle = Label(rootMenu, text= "PopCard Games", font=("Cooper Black", 80),  bg='#8B0000', foreground="white")
    gameTitle.place(relx = .5, rely = .13, anchor=CENTER)
    var = IntVar() #tkinter variable to keep track of which radio button is selected
    var.set(0)
    audioSpeakerThread = threading.Thread(target=outPutAudioMenu) #speaker thread
    audioSpeakerThread.start()
    #adds to output queue for text to speech for audio feedback
    outPutMenu.put("Welcome to PopCard Games.\n At anytime say 'silent' or 'audio' to choose game play mode or click the respective button.\
    \nTHEN say 'first' to choose 21 and 'second' to choose war or click the respective button. \nSay 'quit' anytime to quit.")
    #adds to gui for visual feedback

    #radio buttons for the options of audio and silent
    audioButton = Radiobutton(rootMenu, text ="Audio", font=("Tahoma", 50), variable=var, value=1)
    audioButton.place(relx = 0.25, rely = .35, anchor=W)
    slientButton = Radiobutton(rootMenu, text ="Silent",  font=("Tahoma", 50), variable=var, value=2)
    slientButton.place(relx = .25, rely = .6,  anchor=W)
    #actual buttons for the options 21 and war
    btn21 = Button(rootMenu, text ="  21  ", font=("Tahoma", 45), relief=RIDGE, command=lambda: choose_21())
    btn21.place(relx = .75, rely = .35, anchor=E)
    btnWar = Button(rootMenu, text =" WAR ", font=("Tahoma", 45), relief=RIDGE, command=lambda: choose_war())
    btnWar.place(relx = .75, rely = .6, anchor=E)

    menuInstruction = Label(rootMenu, text= "Welcome to PopCard Games.\n At anytime say 'silent' or 'audio' to choose game play mode or click the respective button.\
    \nTHEN say 'first' to choose 21 and 'second' to choose war or click the respective button. \nSay 'quit' anytime to quit.", font=("Tahoma", 20),  bg='#8B0000', foreground="white")
    menuInstruction.place(relx= .5, rely= .84, anchor=CENTER)

    rootMenu.mainloop() 
    # this code will only be reached if user clicks the 'x' button to close the window
    if menuProcess != "":
        menuProcess.terminate()
    menuProcess.terminate()
    endMenu = 1 
    return
if __name__ == "__main__":
    main()
    os._exit(0)