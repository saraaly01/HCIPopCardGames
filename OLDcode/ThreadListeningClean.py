import tkinter
from tkinter import *
import time
import threading
import random
import queue
import speech_recognition as sr

global root
global msg

#!!!!!BUGS:
#Things print weird- as in over eachother- this might make the UI hard to work with
#Sometimes the listening will just freeze- it might be a thread problem

#Copied from Nik's 21 code- for the recognizer function
r = sr.Recognizer()
# r.adjust_for_ambient_noise(source, duration=1)
mic = sr.Microphone()

#GuiPart Class- two functions (init and processIncoming).
# __init__ sets up the GUI (put initial visuals and buttons there)
# processIncoming loops through the queue (the communication between the GUI and the thread listening for input)
class GuiPart:
    # __init__ sets up the GUI (put initial visuals and buttons there)
    def __init__(self, main, queue, endCommand):
        def func(args):
            print(args)

        self.queue = queue
        # Set up the GUI
        # Button to quit
        console = tkinter.Button(main, text='Done', command=endCommand)
        console.pack()
        # IDEA: we could add Hit and Stand Buttons. It wouldn't really matter if the user says the word or hits the button, it would call the same command


    # processIncoming loops through the queue (the communication between the GUI and the thread listening for input)
    def processIncoming(self):

        #global root
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)

                #This print hit or not hit- BUG: it prints hit multiple times overlaying each other
                printText = Label(root, text=msg, font=20)
                printText.place(relx=.4, rely=.2)

                # this returns the current message- it doesn't stop listening though
                return msg
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

#ThreadCreator Class- three functions (init, periodicCall, getInput, audioListener)
class ThreadCreator:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    #init- sets up the queue (this communicates with the GUI/main code)
    def __init__(self, main):  # main is already in the params
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.main = main

        # Create the queue
        self.inputQueue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(main, self.inputQueue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.audioListenerThread = threading.Thread(target=self.audioListener)
        self.audioListenerThread.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    #periodicCall- loops through, calling processIncoming in the GUI class
    def periodicCall(self):  # adding main to the params
        """
        Check every 200 ms if there is something new in the queue.
        """

        self.gui.processIncoming()
        # self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.main.after(200, self.periodicCall)

    #Calls getInput function- tells if the user says hit or stand (lil buggy)
    #It will also quit if you tell it to quit
    def audioListener(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        msg = ''
        while self.running:

            print("Taking in speaking input")

            with mic as source:
                try:
                    r.adjust_for_ambient_noise(source=source, duration=1)
                    audio = r.listen(source, timeout=5)
                    msg = r.recognize_google(audio, language='en')
                    print(msg)
                except:
                    print("cant recognise speech")
                    msg = "-"

            self.inputQueue.put(msg)
        print("Have a nice day")

    def endApplication(self):
        self.running = 0


root = tkinter.Tk()
root.geometry('700x700+300+100')

client = ThreadCreator(root)
root.mainloop()
client.endApplication()