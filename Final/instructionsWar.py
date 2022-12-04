
from tkinter import *

def instructionsWar(rootIN):
    root = Toplevel(rootIN)
    root.title('Instructions War')
    root['background']='#8B0000'
    root.geometry("1000x1000")
    instructionsGeneral = "Rules of War:\n \
    The deck is split evenly. The player and computer flips a card and the higher card gets both cards.\n\
    If there is a tie, the computer and player flip four cards and the fourth card is compared. \n\
    Whoever has the fourth card gets all the cards played in that round If there is a tie, everyone gets their cards back.\n\
    Whoever ends up with no cards first, loses!\n"
    instructionsApplication = "With Press the flip button to flip your card (the computer will flip their card too).\n \
    If playing with audio say flip to do the same. When a war commences, say war to continue or hit the war button. \n\
    At any point, if playing with audio say score to see how many cards the player and computer have each."
    placeGeneral = Label(root, text = instructionsGeneral, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeGeneral.place(relx= 0, rely=0)
    placeApplication = Label(root, text = instructionsApplication, font=("Comic Sans MS", 12),  bg='#8B0000')
    placeApplication.place(relx= 0, rely=.6)
