import pydealer
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading
from instructions21 import instructions21
from audioListener import getInput

global root, hitButton, standButton, flippedCard, end21, outPut, playAgainButton, standCalled, audioChoice
output = queue.Queue()  # output queue will hold messages that a thread will output with voice
deck = pydealer.Deck()  # card deck



# outPutAudio is one of the worker functions
def outPutAudio():
    while True:  # thread is constantly checking if there is a message on the queue it has to output
        while output.empty() == False:  # if the queue is not empty the thread will get ready to output the message
            msg = output.get(0)
            hitButton['state'] = DISABLED  # while the computer is talking the user can not press the stand or hit button
            standButton['state'] = DISABLED
            # next three lines uses google's package for text to speech
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            os.system("mpg123 test.mp3")
        if end21:  # if the game has been end21ed the thread can be terminated
            playAgainButton['state'] = NORMAL
            return
        else:  # else allow the hit and stand buttons to be used again
            hitButton['state'] = NORMAL
            standButton['state'] = NORMAL


# audioListener is the other worker function
def audioListener():
    global standCalled
    standCalled = 0
    while True:  # constantly using the microphone to check if the user is saying something
        msg = getInput(("yes", "no", "quit", "instructions", "help", "instruction", "again"))
        msg = msg.lower()
        if msg == "yes" and standCalled == 0:  # user picked hit and calls hit function
            output.put("You picked hit.")
            hitAction()
        if msg == "no" and standCalled == 0:  # user picked stand and calls stand function
            output.put("You picked stand.")
            standCalled = 1
            standAction()
        if msg == "quit":
            quit()
            return
        if msg == "instructions" or msg == "help" or msg == "instruction":
            instructions21(root)
        if msg == "again" and standCalled:
            playAgain()
            return


def playAgain():
    # this does not work
    root.destroy()
    main21(audioChoice)


# function when user wants to hit
def hitAction():
    global root, xPlayer, player_hand, deck
    tempCard = deck.deal(1)  # deals one card
    output.put("You got a " + str(tempCard))  # computer outputs that they got this card
    tempCardimg = insertImage(str(tempCard))
    tempCardimg.place(relx=.12 + xPlayer, rely=.3)  # card is added to the GUI
    player_hand += tempCard  # card is added to the players hand
    xPlayer += .05  # variable represents where to place the card x wise, is incremented for the next card to be placed
    currPlayerScore = str(hand_score(player_hand))  # the players current score
    playerScore = Label(root, text=currPlayerScore, font=("Comic Sans MS", 20))
    playerScore.place(relx=.3, rely=.1)  # the current score is placed/updated
    output.put("Your hand score is now " + str(currPlayerScore))  # computer outputs their current score
    if hand_score(player_hand) >= 21:  # if the computer hits 21 or busts stand is automatically called
        standAction()


# function if user chooses stand or stand is called
def standAction():
    global dealer_hand, deck, xDealer, flippedCard, root, standCalled
    standCalled = 1
    # disables hit and stand as they can no longer play
    hitButton['state'] = DISABLED
    standButton['state'] = DISABLED
    # next three lines of code destroys the flipped card image on the GUI of the Dealer's hand and puts the front facing version
    flippedCard.destroy()
    flippedCard = insertImage(str(dealer_hand[1]))
    flippedCard.place(relx=.58, rely=.3)
    output.put(
        "The dealer's hidden card was a" + str(dealer_hand[1]) + "Their score is now" + str(hand_score(dealer_hand)))
    while hand_score(dealer_hand) < 17 and hand_score(player_hand) < 21:
        # if the dealer's hand is less than 17, they have to continue to get more cards
        # but this is only if the player did not win/bust
        tempCard = deck.deal(1)
        dealer_hand += tempCard
        output.put("Dealer receives a " + str(tempCard) + "there score is now" + str(hand_score(dealer_hand)))
        dealerScore = Label(root, text=str(hand_score(dealer_hand)), font=("Comic Sans MS", 20))
        dealerScore.place(relx=.8, rely=.1)
        tempCardimg = insertImage(str(tempCard))
        tempCardimg.place(relx=.7 + xDealer, rely=.3)
        xDealer += .05
    dealerScore = Label(root, text=str(hand_score(dealer_hand)), font=("Comic Sans MS", 20))
    dealerScore.place(relx=.8, rely=.1)
    finish()  # calls finish function for results and score
    return


def insertImage(cardPlayed):
    # function avoids redundant code by taking in the card and getting the label ready to place on the GUI
    global root
    width = int(
        250 / 2.5)  # the width and height of the cards are resized because the actual jpeg file is too big for the screen
    height = int(363 / 2.5)
    cardOutput = Image.open("cards\\" + str(cardPlayed) + ".png")
    test = cardOutput.resize((width, height))
    test = ImageTk.PhotoImage(test)
    imglabel = Label(root, image=test)
    imglabel.image = test
    return imglabel

def quit():
    global end21 
    end21 = 1
    root.destroy()
    os._exit(0)


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
    if score > 21:
        if 11 in mylist:  # deals with ACE (21 rules allows ACE to be either 1 or 21)
            mylist.remove(11)
            mylist.append(1)
            score = 0
            for i in mylist:
                score += i
    return score


def finish():
    # function wraps up game by determing result and outputing the result
    global end21
    playerScore = hand_score(player_hand)
    dealerScore = hand_score(dealer_hand)
    output.put("Your final score is " + str(playerScore) + "The dealer's final score is" + str(dealerScore))
    result = ""
    if playerScore == 21:
        result = "Player hit 21. Player Wins"
    elif playerScore > 21:
        result = "Player Bust"
    elif dealerScore > 21:
        result = "Dealer Bust"
    elif playerScore <= 21 and playerScore > dealerScore:
        result = "Player Wins"
    elif dealerScore <= 21 and dealerScore > playerScore:
        result = "Dealer Wins"
    elif playerScore == dealerScore:
        result = "Push. The game is a tie."
    resultLabel = Label(root, text=result, font=("Comic Sans MS", 20), bg='#8B0000', relief="solid")
    resultLabel.place(relx=.4, rely=.55)
    output.put("The result of the game is " + result)
    output.put("Say again to play again or say quit to quit.")
    end21 = 1  # global end21 variable is assigned so that playagin button can pop up
    if audioChoice == 2:
        playAgainButton['state'] = NORMAL



def main21(audioFromMenu):
    
    global root, dealer_hand, player_hand, deck, xDealer, xPlayer, hitButton, standButton, flippedCard, playAgainButton, end21
    global standCalled, audioChoice
    audioChoice = audioFromMenu
    end21 = 0
    standCalled = 0
    # many global variables to use threads seamlessly
    xPlayer = 0  # this is the x value that will be used (and changed) to place the cards on the GUI on the players side
    xDealer = .05  # this is the y value that will be used (and changed) to place the cards on the GUI on the dealers sie

    deck.shuffle()  # shuffling one more time as it seems to help vary the cards more
    #creates window
    root = Tk()
    root.title('21')
    root['background']='#8B0000'
    # window width of screen
    window_width= root.winfo_screenwidth()
    # window height of screen              
    window_height= root.winfo_screenheight()
    # set root winow to screen size           
    root.geometry("%dx%d" % (window_width,  window_height))
    root.state("zoomed")
    # segment puts text on the screen
    gameTitle = Label(root, text="21", font=("Comic Sans MS", 30))
    gameTitle.place(relx=0.45, rely=0)
    player = Label(root, text="PLAYER", font=("Comic Sans MS", 20), bg='#8B0000', relief="solid")
    player.place(relx=.2, rely=.1)
    dealer = Label(root, text="DEALER", font=("Comic Sans MS", 20), bg='#8B0000', relief="solid")
    dealer.place(relx=.7, rely=.1)

    # inserts the flipped card (backside) of the dealer's on the dealers side of the GUI
    cardBack = insertImage("card")
    cardBack.place(relx=.43, rely=.15)


    deck.shuffle()  # shuffle the deck
    player_hand = pydealer.Stack()  # player's cards
    dealer_hand = pydealer.Stack()  # dealer's cards

    dealer_hand += deck.deal(1)  # deals the dealer one card for now (the one that is showing)
    player_hand += deck.deal(2)  # deals the player their two cards

    currDealerScore = str(hand_score(dealer_hand))
    dealerScore = Label(root, text=currDealerScore, font=("Comic Sans MS", 20))
    dealerScore.place(relx=.8,
                      rely=.1)  # adds the dealers score on the GUI and then deals their second card so that the user doesn't know it
    dealer_hand += deck.deal(1)  # second card

    playerScore = Label(root, text=str(hand_score(player_hand)), font=("Comic Sans MS", 20))
    playerScore.place(relx=.3, rely=.1)  # places the player score on the screen

    imgPlayed = insertImage(dealer_hand[0])  # inserts the showing card of the Dealer's on the screen
    imgPlayed.place(relx=0.67, rely=.3)
    flippedCard = insertImage("card")  # inserts the flipped card (backside)on the Dealer's side
    flippedCard.place(relx=.58, rely=.3)

    # buttons on the screen to press to hit, stand with the functions to call if the buttons are pressed
    hitButton = Button(root, text="HIT", font=("Comic Sans MS", 15), command=lambda: hitAction())
    hitButton.place(relx=.3, rely=.7)
    standButton = Button(root, text="STAND", font=("Comic Sans MS", 15), command=lambda: standAction())
    standButton.place(relx=.6, rely=.7)

    playAgainButton = Button(root, text="Play Again", font=("Comic Sans MS", 15), command=lambda: playAgain(),
                             state=DISABLED)
    playAgainButton.place(relx=.45, rely=.7)

    instructionButton = Button(root, text="?", font=("Comic Sans MS",30), command=lambda: instructions21(root))
    instructionButton.place(relx = .8,rely = .8)

    # creates two threads. Listener and Speaker. Listener's worker function continuosuly listens for output.
    # Speaker's work function continuously looks if they need to output something
    if audioChoice == 1:
        audioListenerThread = threading.Thread(target=audioListener)
        audioListenerThread.start()
        audioSpeakerThread = threading.Thread(target=outPutAudio)
        audioSpeakerThread.start()
    output.put("Welcome to 21.")
    # displays the players card
    for card in player_hand:
        imgPlayed = insertImage(card)
        imgPlayed.place(relx=0.12 + xPlayer, rely=.3)
        xPlayer += .05  # increments the x value to space out the cards on GUI
        output.put("You have a " + str(card))
    
    output.put("Your hand score is " + str(hand_score(player_hand)))
    output.put("Dealer card showing is a " + str(dealer_hand[0]))

    if hand_score(player_hand) == 21:  # if player gets 21 off the bat stand is called
        standAction()
    else:
        output.put("Say yes anytime to hit and say no anytime to stand")
    root.mainloop()
    end21 = 1
    os._exit(0)