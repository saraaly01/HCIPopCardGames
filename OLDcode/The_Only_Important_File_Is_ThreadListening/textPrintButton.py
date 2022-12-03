from tkinter import *

## This is code for a widget that takes in text input and prints it on a button click

a=Tk()
a.title('window')
a.geometry('500x500+300+100')
b = StringVar()
        #
def com():
    c=b.get()
    labl2 = Label(text=c, font=20).pack()
        #
labl1 = Label(text='Functionality to a Button', font=30).pack()
        #
button1 = Button(text='Press to print', command= com).pack()
        #
text = Entry(textvariable=b).pack()
        #
a.mainloop()
        ##