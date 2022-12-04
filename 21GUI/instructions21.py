
from tkinter import *
import os

def instructions(rootIN):
    root = Toplevel(rootIN)
    root.title('Instructions 21')
    root['background']='#8B0000'
    root.geometry("1000x1000")
    instructionsGeneral = "Rules of 21:\n \
    Cards values of 2-9 are worth 2pts-9pts, respectively.\n\
    King, Jack, and Queen are each worth 10pts.\n \
    Aces are worth 1pt or 11pts, depending on the player score (whatever is more beneficial to the player)\n\n\
    \
    The player is dealt two cards face up.\n\
    The dealer is dealt 1 card face up.\n\n\
    \
    The player can choose to hit (take another card) or stand (defer to the dealer) to try to get as \nclose to the value 21 as possible but not over.\n \
    \
    Once the player stands, the dealer has to hit to get as close to 21 as possible but not over.\n\
    Once the dealer's hand value is over 16, the dealer has to stand.\n\n\
    \
    If the player or dealer hand goes over 21, that defines a bust which is a loss.\n\
    If the player has a higher score than the dealer and less than 21, then the player wins (and vice versa)\n\
    If the player or dealer hits exactly 21, that defines an automatic win\n\
    If the player or dealer have the same score, that defines a push, which is a tie.\n"

    instructionsApplication = "Press the hit button to receive a card. Press the stand button to stand.\n\
    If playing with audio, At any time say 'yes' to hit and say 'no' to stand. To quit say 'quit' or close out window."
    placeGeneral = Label(root, text = instructionsGeneral, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeGeneral.place(relx= 0, rely=0)
    placeApplication = Label(root, text = instructionsApplication, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeApplication.place(relx= 0, rely=.6)
