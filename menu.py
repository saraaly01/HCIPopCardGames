from tkinter import *
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading

global root,  outPut, var, end
end = 0
output = queue.Queue()  # output queue will hold messages that a thread will output with voice
def outPutAudio():
    global output, end
    while True:
        if end:
            return
        while output.empty() == False:
            msg = output.get(0)
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            os.system("mpg123 test.mp3")

#Thread function- changes the audio setting and chooses game based on user voice input
def audioListener():
    global end
    r = sr.Recognizer()
    mic = sr.Microphone()
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
            var.set(1)
            #outputCurSetting()
        elif msg == "silent" or msg == "silence":
            #audioChoice = "Vsilent" #!!differentiate audio from button and audio from voice
            var.set(2)
        if msg == "first":
            choose_21()
            return
        if msg == "second":
            choose_war()
            return
        if end:
            return
    

def choose_21():
    print(var.get())


  
def choose_war():
    print(var.get())
def main():
    listenerThread = threading.Thread(target=audioListener)
    listenerThread.start()
    global end, var
    root = Tk()
    root.title('PLAY')
    root['background']='#8B0000'
    root.geometry("900x600")
    ##THREAD SECTION
    gameTitle = Label(root, text= "POPCARD GAMES", font=("Comic Sans MS", 30))
    gameTitle.place(relx = 0.3, rely = 0)
    var = IntVar()
    audioButton = Radiobutton(root, text ="Audio", variable=var, value=1)
    audioButton.place(relx = .2, rely = .3)
    slientButton = Radiobutton(root, text ="Slient", variable=var, value=2)
    slientButton.place(relx = .2, rely = .35)
    btn21 = Button(root, text ="21", font=("Comic Sans MS", 30), command=lambda: choose_21())
    btn21.place(relx = .2, rely = .55)
    btnWar = Button(root, text ="WAR", font=("Comic Sans MS", 30), command=lambda: choose_war())
    btnWar.place(relx = .75, rely = .55)
    
    print("ugh")
    root.mainloop()
    end = 1
if __name__ == "__main__":
    main()