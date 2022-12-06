import pydealer
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading, subprocess
from instructions21 import *
from globalFunctions import *
global root, hitButton, standButton, flippedCard, end21, outPut, playAgainButton, standCalled, audioChoice, process21

process21 = ""

output = queue.Queue()  # output queue will hold messages that a thread will output with voice
deck = pydealer.Deck()  # card deck



# outPutAudio is one of the worker functions.
# its job is to output audio to the speaker
def outPutAudio():
    global output, root, playAgainButton, process21
    while True:  # thread is constantly checking if there is a message on the queue it has to output
        while output.empty() == False:  # if the queue is not empty the thread will get ready to output the message
            msg = output.get(0)
            hitButton['state'] = DISABLED  # while the computer is talking the user can not press the stand or hit button
            standButton['state'] = DISABLED
            # next three lines uses google's package for text to speech
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)
            myobj.save("test.mp3")
            process21 = subprocess.Popen(["mpg123", "test.mp3"], universal_newlines=True)
        if end21:  # if the game has been end21ed the thread can be terminated
            return
        else:  # else allow the hit and stand buttons to be used again
            hitButton['state'] = NORMAL
            standButton['state'] = NORMAL


# audioListener is the other worker function
# its job is to listen for audio input from the user
def audioListener():
    global standCalled, process21
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
            if process21 != "":
                process21.terminate()
            quit()
            return
        if msg == "instructions" or msg == "help" or msg == "instruction":
            if process21 != "":
                process21.terminate()
            instructions21(audioChoice)
        if msg == "again":
            playAgainButton.invoke()
            return

# in the case that the user signals through voice input or button click to play again, 
# this function is called. It deconstructs the window, and rebuilds it with a fresh game
def playAgain():
    if process21 != "":
        process21.terminate()
    # this does not work
    root.destroy()
    main21(audioChoice)


# function that is called when the user signals through voice or button click to 'hit'
def hitAction():
    global root, xPlayer, player_hand, deck
    if process21 != "":
        process21.terminate()
    tempCard = deck.deal(1)  # deals one card
    output.put("You chose hit. You got a " + str(tempCard))  # computer outputs that they got this card
    tempCardimg = insertImage(str(tempCard), root)
    tempCardimg.place(relx=.12 + xPlayer, rely=.3)  # card is added to the GUI
    player_hand += tempCard  # card is added to the players hand
    xPlayer += .05  # variable represents where to place the card x wise, is incremented for the next card to be placed
    currPlayerScore = str(hand_score(player_hand))  # the players current score
    playerScore = Label(root, text=str("Points: " +currPlayerScore), font=("Tahoma", 30), bg='#8B0000', foreground="white")
    playerScore.place(relx =.17, rely = .2) # the current score is placed/updated
    output.put("Your hand score is now " + str(currPlayerScore))  # computer outputs their current score
    if hand_score(player_hand) >= 21:  # if the computer hits 21 or busts stand is automatically called
        standAction()


# function that is called when the user signals through voice or button click to 'stand'
def standAction():
    global dealer_hand, deck, xDealer, flippedCard, root, standCalled, output
    standCalled = 1
    if process21 != "":
        process21.terminate()
    # disables hit and stand as they can no longer play
    hitButton['state'] = DISABLED
    standButton['state'] = DISABLED
    # next three lines of code destroys the flipped card image on the GUI of the Dealer's hand and puts the front facing version
    flippedCard.destroy()
    flippedCard = insertImage(str(dealer_hand[1]), root)
    flippedCard.place(relx=.62, rely=.3)
    output.put(
        "The dealer's hidden card was a" + str(dealer_hand[1]) + "Their score is now" + str(hand_score(dealer_hand)))
    while hand_score(dealer_hand) < 17 and hand_score(player_hand) < 21:
        # if the dealer's hand is less than 17, they have to continue to get more cards
        # but this is only if the player did not win/bust
        tempCard = deck.deal(1)
        dealer_hand += tempCard
        output.put("Dealer receives a " + str(tempCard) + "there score is now" + str(hand_score(dealer_hand)))
        dealerScore = Label(root, text=str("Points: " +str(hand_score(dealer_hand))), font=("Tahoma", 30), bg='#8B0000', foreground="white")
        dealerScore.place(relx =.65, rely = .2) 
        tempCardimg = insertImage(str(tempCard), root)
        tempCardimg.place(relx=.7 + xDealer, rely=.3)
        xDealer += .05
    dealerScore = Label(root, text=str("Points: " +str(hand_score(dealer_hand))), font=("Tahoma", 30), bg='#8B0000', foreground="white")
    dealerScore.place(relx =.65, rely = .2) 
    finish()  # calls finish function for results and score
    return

# function that is called when the user signals through voice or button click to quit the game
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

# function wraps up game by determing result and outputing the result
def finish():
    global end21, output
    playerScore = hand_score(player_hand)
    dealerScore = hand_score(dealer_hand)
    output.put("Your final score is " + str(playerScore) + "The dealer's final score is" + str(dealerScore))
    result = ""
    if playerScore == 21:
        result = "Player Wins"
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
    resultLabel = Label(root, text=result, font=("Tahoma", 35), bg='#8B0000', foreground="white")
    resultLabel.place(relx=.4, rely=.55)
    output.put("The result of the game is " + result + ". Say again to play again or say quit to quit or click the restart button.")
    end21 = 1  # global end21 variable is assigned so that playagain button can pop up



# main function that deals with the control flow for the game
def main21(audioFromMenu):
    
    # list of global variables makes it easier to deal with threading, and subprocessing. Due to tkinter's nature, there are many
    # variables required to deal with threading
    global root, dealer_hand, player_hand, deck, xDealer, xPlayer, hitButton, standButton, flippedCard, end21, playAgainButton
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
    gameTitle = Label(root, text="21", font = ("Cooper Black", 80),  bg='#8B0000', foreground="white")
    gameTitle.place(relx = .5, rely = .13, anchor=CENTER)
    player = Label(root,text= "PLAYER", font=("Tahoma", 45), bg='#8B0000', foreground="white")
    player.place(relx =.17, rely = .1)
    dealer = Label(root, text="DEALER", font=("Tahoma", 45), bg='#8B0000', foreground="white")
    dealer.place(relx =.65, rely = .1)

    # inserts the flipped card (backside) of the dealer's on the dealers side of the GUI
    cardBack = insertImage("card", root)
    cardBack.place(relx=.455, rely = .3)



    deck.shuffle()  # shuffle the deck
    player_hand = pydealer.Stack()  # player's cards
    dealer_hand = pydealer.Stack()  # dealer's cards

    dealer_hand += deck.deal(1)  # deals the dealer one card for now (the one that is showing)
    player_hand += deck.deal(2)  # deals the player their two cards

    currDealerScore = str(hand_score(dealer_hand))
    dealerScore = Label(root, text=str("Points: " +currDealerScore), font=("Tahoma", 30), bg='#8B0000', foreground="white")
    dealerScore.place(relx =.65, rely = .2)  # adds the dealers score on the GUI and then deals their second card so that the user doesn't know it
    dealer_hand += deck.deal(1)  # second card

    playerScore = Label(root, text=str("Points: " + str(hand_score(player_hand))), font=("Tahoma", 30), bg='#8B0000', foreground="white")
    playerScore.place(relx =.17, rely = .2)  # places the player score on the screen

    imgPlayed = insertImage(dealer_hand[0], root)  # inserts the showing card of the Dealer's on the screen
    imgPlayed.place(relx=0.67, rely=.3)
    flippedCard = insertImage("card", root)  # inserts the flipped card (backside)on the Dealer's side
    flippedCard.place(relx=.62, rely=.3)

    # buttons on the screen to press to hit, stand with the functions to call if the buttons are pressed
    hitButton = Button(root, text="HIT", font=("Tahoma",25), relief=RIDGE,  command=lambda: hitAction())
    hitButton.place(relx=.32, rely=.7)
    standButton = Button(root, text="STAND", font=("Tahoma",25), relief=RIDGE,  command=lambda: standAction())
    standButton.place(relx=.6, rely=.7)


    instructionButton = Button(root, text="?",font=("Tahoma",30), relief=RIDGE, command=lambda: instructions21(audioChoice))
    instructionButton.place(relx = .95,rely = .85)

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
        imgPlayed = insertImage(card, root)
        imgPlayed.place(relx=0.12 + xPlayer, rely=.3)
        xPlayer += .05  # increments the x value to space out the cards on GUI
        output.put("You have a " + str(card))
    playAgainButton = Button(root, text="RESTART",font=("Tahoma",25), relief=RIDGE, command=lambda: playAgain())
    playAgainButton.place(relx=.43, rely = .7)

    output.put("Your hand score is " + str(hand_score(player_hand)))
    output.put("Dealer card showing is a " + str(dealer_hand[0]))

    if hand_score(player_hand) == 21:  # if player gets 21 off the bat stand is called
        standAction()
    else:
        output.put("Welcome to 21. At anytime say yes to hit, no to stand, quit to quit, and again to restart.")
    
    if audioChoice == 1:
        commands21 = Label(root, text= "Welcome to 21. Press hit or say 'yes' to receive a card, or press stand or say 'no' to stand.\nAt anytime you can say 'quit' to quit or 'again' to restart.\n Press the '?' button for instructions or say 'help' or 'instructions'",font=("Tahoma", 20),  bg='#8B0000', foreground="white")
    elif audioChoice == 2:
        commands21 = Label(root, text= "Welcome to 21. \nPress hit button to receive a card and stand to stand.\n Press the '?' button for instructions.", font=("Tahoma", 20),  bg='#8B0000', foreground="white")
    commands21.place(relx= .5, rely= .89, anchor=CENTER)

    root.mainloop()
    end21 = 1
    if process21 != "": # if window is exited attempts to close audio 
        process21.terminate()
  
    os._exit(0)