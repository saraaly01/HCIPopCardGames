import pydealer
from enum import Enum
from tkinter import *
from PIL import Image, ImageTk
import time
import numpy as np
import speech_recognition as sr
import os
import sys
from gtts import gTTS
import queue
import time
from playsound import playsound
import threading

global root, hitButton, flippedCard, end, outPut, k
output = queue.Queue()
k = 0
end = 0
xPlayer = 0
xDealer = .05
width = int(250/2.5)
height = int(363/2.5)    
deck = pydealer.Deck()
deck.shuffle()
player_hand = pydealer.Stack()
dealer_hand = pydealer.Stack()

r = sr.Recognizer()
mic = sr.Microphone()
def outPutAudio():
    global end
    while True:
        while output.empty() == False:
            msg = output.get(0)
            speak(msg)
        if end:
            return

           
def speak(x):
    global k
    k += 1

    myobj = gTTS(text=x, lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")

def audioListener(root, hitButton, flippedCard):
    global end
    """
    This is where we handle the asynchronous I/O. For example, it may be
    a 'select(  )'. One important thing to remember is that the thread has
    to yield control pretty regularly, by select or otherwise.
    """
    msg = ''
    while True:
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
        if msg == "yes":
            output.put("You picked hit.")
            hitAction(root)
          
        if msg == "no":
            output.put("You picked stand.")
            standAction(hitButton, root, flippedCard)
            end = 1
        if end:
            finish(root)
            return

           
            

    
def hitAction(root):
    global end, xPlayer, player_hand, deck

    tempCard = deck.deal(1)
    output.put("You got a " + str(tempCard))
    tempCardimg = insertImage(str(tempCard), root)
    tempCardimg.place(relx=.12+ xPlayer, rely=.3)
    player_hand += tempCard
    xPlayer +=.05
    currPlayerScore = str(hand_score(player_hand))
    playerScore = Label(root, text= currPlayerScore, font=("Comic Sans MS", 20))
    playerScore.place(relx=.3, rely = .1)
    output.put("Your hand score is now " + str(currPlayerScore))
    if hand_score(player_hand) >21:
        standAction(hitButton, root, flippedCard)
        end = 1
    else:
        end = 0
    
def standAction(hitButton, root, flippedCard):
    global dealer_hand, deck, xDealer
    hitButton['state'] = DISABLED
    flippedCard.destroy()
    flippedCard= insertImage(str(dealer_hand[1]), root)
    flippedCard.place(relx=.58, rely=.3)
    output.put("The dealer's hidden card was a" + str(dealer_hand[1]) + "There score is" + str(hand_score(dealer_hand)))
    while hand_score(dealer_hand) < 17:
        tempCard = deck.deal(1)
        dealer_hand += tempCard

        output.put("Dealer receives a " + str(tempCard) + "their score is now " + str(hand_score(dealer_hand)))
        tempCardimg = insertImage(str(tempCard), root)
        tempCardimg.place(relx=.67+ xDealer, rely=.3)
        xDealer += .05

    dealerScore = Label(root, text= str(hand_score(dealer_hand)), font=("Comic Sans MS", 20))
    dealerScore.place(relx=.8, rely = .1)
    return
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


def finish(root):
    playerScore = hand_score(player_hand) 
    dealerScore = hand_score(dealer_hand) 
    output.put("Your final score is " + str(playerScore) + "The dealer's final score is" + str(dealerScore))
    gameResult = ""
    if dealerScore == playerScore:  # if tie
        gameResult = "Push"
    elif  dealerScore >21 and playerScore > 21:
        gameResult = "Both the player and dealer bust"
    elif dealerScore > 21:  # if dealer bust
        gameResult = "Dealer Bust"
    elif dealerScore > playerScore:  # if dealer > player
        gameResult = "Dealer Won"
    elif playerScore == 21:  # if player got 21
        gameResult = "Player hits 21. Player Wins."
    elif playerScore > 21:  # if player bust
        gameResult = "Player Bust"
    else:  # if player > dealer
        gameResult = "Player Wins"
    resultLabel = Label(root, text= gameResult, font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    resultLabel.place(relx =.4, rely = .8)
    output.put("The result of the game is " + gameResult)

    

def main(rootIN):
    global root, dealer_hand, player_hand, deck, xDealer, xPlayer, hitButton, flippedCard, k
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


    currDealerScore = str(hand_score(dealer_hand))
    dealerScore = Label(root, text= currDealerScore, font=("Comic Sans MS", 20))
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
    
    audioListenerThread = threading.Thread(target=audioListener, args=(root,hitButton, flippedCard))
    audioListenerThread.start()
    audioSpeakerThread = threading.Thread(target=outPutAudio)
    audioSpeakerThread.start()
    
    for card in player_hand:
        imgPlayed = insertImage(card,root)
        imgPlayed.place(relx=0.12 + xPlayer, rely=.3) 
        xPlayer += .05
        output.put("You have a " + str(card))
    output.put("Your hand score is " + str(hand_score(player_hand)))
    output.put("Dealer card showing is a " + str(dealer_hand[0]))
    output.put("Say yes anytime to hit and say no anytime to stand")




if __name__ == '__main__':
    main()