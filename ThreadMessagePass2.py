import tkinter
from tkinter import *
import time
import threading
import random
import queue
global root
global msg
class GuiPart:
    def com(self, c):
        #c = "message 12345"
        labl2 = Label(text=c, font=20).pack()


    def func(self, args):
        print(args)

    def __init__(self, master, queue, endCommand):
        def func(args):
            print(args)

        self.queue = queue
        # Set up the GUI
        # Button to quit
        console = tkinter.Button(master, text='Done', command=endCommand)
        console.pack(  )
        button1 = tkinter.Button(root, text='Press to print', command = lambda: self.com("See this worked!"))
        button1.pack(  )
        btn = tkinter.Button(root, text="Press", command=lambda: com("See this worked!"))
        btn.pack()

        button2 = tkinter.Button(root, text='print thread msg', command = lambda: self.com(self.processIncoming()))
        button2.pack(  )


        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        # def stable_button(btn_msg):
        #     btn = tkinter.Button(root, text="Press2", command=lambda: com(msg))
        #     btn.pack()
        # def com(c):
        #     # c = "message 12345"
        #     labl2 = Label(text=c, font=20).pack()

        global root
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)

                #makes a button print over and over
                #btn = tkinter.Button(root, text="Press2", command=lambda: com(msg))
                #btn.pack()

                #printText = Label(root, text=msg)
                #printText.place(relx=.4, rely=.2)
                #this returns the current message- it doesn't stop listening though
                return msg
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master): #master is already in the params
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def periodicCall(self): #adding master to the params
        """
        Check every 200 ms if there is something new in the queue.
        """

        self.gui.processIncoming()
        #self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            #time.sleep(rand.random(  ) * 1.5)
            msg = rand.random(  )
            #msg = "The process is running"
            #this is where we would ADD the logic if button is clicked, pass a message that button is clicked
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random(  )
root = tkinter.Tk(  )
root.geometry('700x700+300+100')

client = ThreadedClient(root)
root.mainloop(  )