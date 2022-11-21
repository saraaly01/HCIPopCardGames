import pydealer
import numpy as np
from enum import Enum
from tkinter import *
from PIL import Image, ImageTk
import time
global root, hitButton, flippedCard
xPlayer = 0
xDealer = .05
width = int(250/2.5)
height = int(363/2.5)    
deck = pydealer.Deck()
deck.shuffle()
player_hand = pydealer.Stack()
dealer_hand = pydealer.Stack()

    
def hitAction(root):
    global xPlayer
    global player_hand
    global deck
    tempCard = deck.deal(1)
    tempCardimg = insertImage(str(tempCard), root)
    tempCardimg.place(relx=.12+ xPlayer, rely=.3)
    player_hand += tempCard
    xPlayer +=.05
    playerScore = Label(root, text= str(hand_score(player_hand)), font=("Comic Sans MS", 20))
    playerScore.place(relx=.3, rely = .1)
    if hand_score(player_hand) >21:
        standAction(hitButton, root, flippedCard)
    
def standAction(hitButton, root, flippedCard):
    global dealer_hand, deck, xDealer
    hitButton['state'] = DISABLED
    flippedCard.destroy()
    flippedCard= insertImage(str(dealer_hand[1]), root)
    flippedCard.place(relx=.58, rely=.3)

    while hand_score(dealer_hand) < 17:
        tempCard = deck.deal(1)
        dealer_hand += tempCard
        tempCardimg = insertImage(str(tempCard), root)
        tempCardimg.place(relx=.67+ xDealer, rely=.3)
        xDealer += .05

    dealerScore = Label(root, text= str(hand_score(dealer_hand)), font=("Comic Sans MS", 20))
    dealerScore.place(relx=.8, rely = .1)
    finish()
def insertImage(cardPlayed,root):
    cardOutput = Image.open("cards\\" + str(cardPlayed) + ".png")
    test = cardOutput.resize((width, height))
    test = ImageTk.PhotoImage(test)
    imglabel = Label(root, image=test)
    imglabel.image = test
    return imglabel

# given a hand, returns hand score
def hand_score(x):
    mylist = []
    for i in x:
        try:
            int(i.value)
            mylist.append(int(i.value))
        except:
            if i.value == "Ace":
                temp_score = 0
                for i in mylist:
                    temp_score += i
                if temp_score + 11 > 21:
                    mylist.append(1)
                else:
                    mylist.append(11)
            else:
                mylist.append(10)
    score = 0
    for i in mylist:
        score += i
    return score


def finish():
    playerScore = hand_score(player_hand) 
    dealerScore = hand_score(dealer_hand) 
    result = ""
    if playerScore  >21 and dealerScore >21:
        result = "Both Lose"
    elif playerScore > 21  or (dealerScore <=21 and dealerScore > playerScore):
        result = "Dealer Wins"
    elif dealerScore > 21  or ( playerScore <= 21 and playerScore > dealerScore):
        result = "Player Wins"
    else:
        result = "Tie"
    resultLabel = Label(root, text= result, font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    resultLabel.place(relx =.4, rely = .8)
    

def main(rootIN):
    global root, dealer_hand, player_hand, deck, xDealer, xPlayer, hitButton, flippedCard
    deck.shuffle()

    keepPlaying = True
    root = Toplevel(rootIN)
    root.title('PopCardGames')
    root['background']='#8B0000'
    # window width of screen
    window_width= rootIN.winfo_screenwidth()
    # window height of screen              
    window_height= rootIN.winfo_screenheight()

    # set root winow to screen size           
    root.geometry("%dx%d" % (window_width,  window_height))
    gameTitle = Label(root, text= "21", font=("Comic Sans MS", 30))
    gameTitle.place(relx = 0.45, rely = 0)

    player = Label(root, text= "PLAYER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    player.place(relx =.2, rely = .1)
    dealer = Label(root, text= "DEALER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    dealer.place(relx =.7, rely = .1)
    cardBack = insertImage("card", root)
    cardBack.place(relx=.43, rely=.15)

 

    dealer_hand += deck.deal(1)
    player_hand += deck.deal(2)

    for card in player_hand:
        imgPlayed = insertImage(card,root)
        imgPlayed.place(relx=0.12 + xPlayer, rely=.3) 
        xPlayer += .05

    dealerScore = Label(root, text= str(hand_score(dealer_hand)), font=("Comic Sans MS", 20))
    dealerScore.place(relx=.8, rely = .1)

    dealer_hand += deck.deal(1) #second card 
    playerScore = Label(root, text= str(hand_score(player_hand)), font=("Comic Sans MS", 20))
    playerScore.place(relx=.3, rely = .1)

    imgPlayed = insertImage(dealer_hand[0],root)
    imgPlayed.place(relx=0.67, rely=.3) 
    
    hitButton = Button(root, text = "HIT", font=("Comic Sans MS", 15), command=lambda: hitAction(root))
    hitButton.place(relx= .3, rely=.7)

   
    flippedCard= insertImage("card", root)
    flippedCard.place(relx=.58, rely=.3)

    standButton = Button(root, text = "STAND", font=("Comic Sans MS", 15),  command=lambda: standAction(hitButton, root, flippedCard))
    standButton.place(relx= .6, rely=.7)




if __name__ == '__main__':
    main()