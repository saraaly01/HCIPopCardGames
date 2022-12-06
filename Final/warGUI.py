import pydealer
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading, subprocess
from instructionsWar import *
from globalFunctions import *

# list of global variables makes it easier to deal with threading, and subprocessing. Due to tkinter's nature, there are many
# variables required to deal with threading
global outputWAR, endWAR, audioFromMenu, process, rootWar, warWait, flip
global computer_hand, player_hand, cardPlayedP, cardPlayedC, cardBackPlayer, cardBackComputer

endWAR= 0 #signals the endWARof the game
warWait = 0 #variable determines if we are awaiting a war sequence 
outputWAR = queue.Queue()  #output queue will hold messages that a thread will output with voice


#outPutAudio is one of the worker functions
def outPutAudioWar():
    global flip, outputWAR, endWAR, process
    while True: #thread is constantly checking if there is a message on the queue it has to output
        if endWAR:
            return
        while outputWAR.empty() == False: # if the queue is not empty the thread will get ready to output the message
            msg = outputWAR.get(0)
            flip['state'] = DISABLED #if output is being said, user can not hit the button
            #next three lines uses google's package for text to speech
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)  
            myobj.save("test.mp3")
            process = subprocess.Popen(["mpg123", "test.mp3"])
            if not warWait:
                flip['state'] = NORMAL
    


#audioListener is the other worker function
def audioListenerWar(): 
    global outputWAR,endWAR, warWait, process
    while True: #constantly using the microphone to check if the user is saying something
        msg = getInput(("flip", "war", "score", "instructions", "help", "instruction", "quit"))
        msg = msg.lower()
        if msg== "flip":  #user picked flip and calls flipCard function if we are not waiting for a war
            if warWait ==0:
                flipCard()
        if msg == "war":
            cardTie() #cardTie is the function that deals with the war
        if msg== "score": #prints out how many cards each player has
            outputWAR.put("You have" + str(player_hand.size) + "cards. Computer has" + str(computer_hand.size) + "cards.")
        if msg == "instructions" or msg == "help" or msg == "instruction":
            if audioFromMenu == 1:
                process.terminate()
            instructionsWar(audioFromMenu)
        if msg == "quit" or endWAR: #ends the program
            if audioFromMenu == 1:
                process.terminate()
            quitWar()
            return

def quitWar():
    global endWAR
    endWAR = 1
    rootWar.destroy()
    os._exit(0)

def compareCards(card1, card2): 
    #function takes two cards and compares their numerical value
    #return 1 if card1 greater, return 2 if card2 greater, return 0 if tie
    cardOne = card1.split()
    #card come in as a string like "9 of Spades" we split it so we can get the number onl y
    #number only matters in war, not suit
    cardOne = cardOne[0]
    cardTwo = card2.split()
    cardTwo = cardTwo[0]
    if cardOne == cardTwo:  #tie, returns 0
        return 0
    match cardOne:
        case "Ace":
            cardOne = 14
        case "King":
            cardOne = 13
        case "Queen":
            cardOne = 12
        case "Jack":
            cardOne = 11
    match cardTwo:
        case "Ace":
            cardTwo = 14
        case "King":
            cardTwo = 13
        case "Queen":
            cardTwo = 12
        case "Jack":
            cardTwo = 11
    if int(cardOne) > int(cardTwo): #players value is higher, returns 1
        return 1
    elif int(cardTwo) > int(cardOne): #computers value is higher, returns 2
        return 2

#function handles a tie in war
def cardTie():
    global rootWar, labels, player_hand, computer_hand, cardPlayedP, cardPlayedC, flip, warWait
    warWait = 0
    computer_hand.shuffle()
    player_hand.shuffle()
    labels[-1].destroy() #tie widget
    labels[-2].destroy() #waitWarButton widget
    cardPlayedPTie = [] #array keeps track of all cards played in tie for the player 
    cardPlayedCTie  = [] #array keeps track of all cards played in tie for the computer
    playerX = .22 #x value for placing cards on the players side (left side of screen)
    computerX = .7 #x value for placing cards on the computers side (right side of screen)


    for i in range(4): 
        #in a tie, four cards should be placed, with the fourth card being the one you compare to
        #if player/computer hand is less than 4 just puts down all they have and compares the last card
        if player_hand.size != 0:
            cardPlayedPcurr = player_hand.random_card(remove = True)
            cardPlayedPTie.append(cardPlayedPcurr)
            outputWAR.put("You flip a " + str(cardPlayedPcurr))
            img= insertImage(cardPlayedPcurr,rootWar)
            img.place(relx = playerX + (.05 *i), rely = .3)
            labels.append(img)
        if computer_hand.size != 0:
            cardPlayedCcurr = computer_hand.random_card(remove = True)
            cardPlayedCTie.append(cardPlayedCcurr)
            outputWAR.put("Computer flips a " + str(cardPlayedCcurr))

            img= insertImage(cardPlayedCcurr,rootWar)
            img.place(relx = computerX - (.05 *i), rely = .3)
            labels.append(img)
    
    valueCompareTie = compareCards(str(cardPlayedPcurr), str(cardPlayedCcurr))

    if valueCompareTie == 0: # cards are equal 
        outputWAR.put("Tie again. Everyone gets their cards back.")
        tie = Label(rootWar, text= "TIE, CARDS BACK!", font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        tie.place(relx= .5, rely= .74, anchor=CENTER)
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        labels.append(tie)
        player_hand.add(cardPlayedP)
        computer_hand.add(cardPlayedC)
    elif valueCompareTie == 1: #player gets cards in the round
        outputWAR.put("YOU GET THE CARDS!")
        playerWin =Label(rootWar, text= "PLAYER GETS CARDS!", font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        playerWin.place(relx= .5, rely= .74, anchor=CENTER)
        labels.append(playerWin)
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            player_hand.add(cardC)
        player_hand.add(cardPlayedP)
        player_hand.add(cardPlayedC)
    elif valueCompareTie == 2: #computer gets cards in the round
        outputWAR.put("COMPUTER GETS CARDS")
        computerWin = Label(rootWar, text= "COMPUTER GETS CARDS!", font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        computerWin.place(relx= .5, rely= .74, anchor=CENTER)
        labels.append(computerWin)
        for cardP in cardPlayedPTie:
            computer_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        computer_hand.add(cardPlayedP)
        computer_hand.add(cardPlayedC)
    
    flip['state'] = NORMAL

    if computer_hand.size == 0 or player_hand.size == 0 and (warWait == 0): #someone ran out of cards
        finish()
    return


#main function of the program, when card gets flipped
def flipCard():
    global rootWar, labels
    global cardBackPlayer, cardBackComputer, cardPlayedP, cardPlayedC, computer_hand, player_hand
    global warWait, flip
    flip['state'] = DISABLED
    if audioFromMenu == 1:
        process.terminate()
    computer_hand.shuffle()
    player_hand.shuffle()
    
    #destroys any widgets we do not need from previous round(s)
    for label in labels:
        label.destroy()
 
    #updates the visual feedback for the number of cards and adds it to the label array so we can delete in the future
    playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Tahoma", 20))
    playerNumCards.place(relx= 0, rely=.0)
    labels.append(playerNumCards)
    computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Tahoma", 20))
    computerNumCards.place(relx= 0, rely=0)
    labels.append(computerNumCards)

    if computer_hand.size == 0 or player_hand.size == 0 and (warWait == 0): #game is over someone doesnt have any cards
        finish()
        return

    #places the cards played on the screen
    cardPlayedC = computer_hand.random_card(remove = True)
    imgPlayedC = insertImage(cardPlayedC,rootWar)
    imgPlayedC.place(relx=0.8, rely=.3) 
    labels.append(imgPlayedC)
    cardPlayedP = player_hand.random_card(remove = True)
    imgPlayedP = insertImage(cardPlayedP,rootWar)
    imgPlayedP.place(relx=0.12, rely=.3) 
    labels.append(imgPlayedP)
    outputWAR.put("You flip a " + str(cardPlayedP) + "The computer flips a " + str(cardPlayedC))

    valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))
    if valueCompare == 0: # cards are equal 
        outputWAR.put("Cards Tied. Hit the War button or if playing with audio say war to continue.")
        tie = Label(rootWar, text= "TIE, WAR!",  font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        tie.place(relx= .5, rely= .74, anchor=CENTER)
        labels.append(tie)
        waitWarButton = Button(rootWar, text ="WAR", font=("Tahoma",25), relief=RIDGE, command=lambda: cardTie())
        waitWarButton.place(relx=.462, rely = .43)
        labels.append(waitWarButton)
        warWait = 1

    if valueCompare == 1: #player wins the cards
        outputWAR.put("YOU GET THE CARDS")
        playerWin = Label(rootWar, text= "PLAYER GETS CARDS!", font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        playerWin.place(relx= .5, rely= .74, anchor=CENTER)
        labels.append(playerWin)
        player_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
        flip['state'] = NORMAL

    elif valueCompare == 2: #computer won the card
        outputWAR.put("COMPUTER GETS CARDS!")
        computerWin = Label(rootWar, text= "COMPUTER GETS CARDS!", font=("Tahoma", 30), bg ='#8B0000', foreground="white")
        computerWin.place(relx= .5, rely= .74, anchor=CENTER)
        labels.append(computerWin)
        computer_hand.add(cardPlayedC)
        computer_hand.add(cardPlayedP)
        flip['state'] = NORMAL
    return

def finish():
    #game is over, outputs results
    flip.destroy()
    if player_hand.size == 0:
        playerWinsGame = Label(rootWar, text = "COMPUTER WINS. GAME OVER", font=("Tahoma", 40), bg='#8B0000', foreground="white")
        playerWinsGame.place(relx= .5, rely= .74, anchor=CENTER)
        outPutAudioWar("Computer Wins. Game Over")
    elif computer_hand.size == 0:
        computerWinsGame = Label(rootWar, text = "PLAYER WINS. GAME OVER",font=("Tahoma", 40), bg='#8B0000', foreground="white")
        computerWinsGame.place(relx= .5, rely= .74, anchor=CENTER)
        outPutAudioWar("Player Wins. Game Over")
    return

#main function for war. It deals with the initialization fot the war game.
def intialize(audio):
    
    global rootWar, labels, flip, outputWAR, endWAR, audioFromMenu, process
    global cardBackPlayer, cardBackComputer,  cardPlayedP, cardPlayedC, computer_hand, player_hand
    audioFromMenu = audio
    labels = []
    deck = pydealer.Deck()
    deck.shuffle()
    #intializes hands 
    player_hand = pydealer.Stack()
    player_hand += deck.deal(26)
    computer_hand = pydealer.Stack()
    computer_hand +=  deck.deal(26)


    rootWar = Tk()
    rootWar.title('War')
    rootWar['background']='#8B0000'
    # window width of screen
    window_width= rootWar.winfo_screenwidth()
    # window height of screen              
    window_height= rootWar.winfo_screenheight()
    # set rootWar winow to screen size           
    rootWar.geometry("%dx%d" % (window_width,  window_height))
    rootWar.state("zoomed")


    gameTitle = Label(rootWar, text= "WAR", font = ("Cooper Black", 80),  bg='#8B0000', foreground="white")
    gameTitle.place(relx = .5, rely = .13, anchor=CENTER)

    player = Label(rootWar, text= "PLAYER", font=("Tahoma", 40), bg='#8B0000', foreground="white")
    player.place(relx =.17, rely = .2)
    computer = Label(rootWar,  text= "COMPUTER", font=("Tahoma", 40), bg='#8B0000', foreground="white")
    computer.place(relx =.65, rely = .2)

    #represents the decks of the players, will put number of cards they have on here
    cardBack = Image.open("cards\\card.png")
    cardBack = cardBack.resize((int(250/2.5),int(363/2.5)))
    cardBack = ImageTk.PhotoImage(cardBack)
    cardBackPlayer= Label(rootWar, image=cardBack,  borderwidth=0, highlightthickness=0)
    cardBackPlayer.image = cardBack
    cardBackPlayer.place(relx=0.02, rely=.3)
    cardBackComputer = Label(rootWar, image=cardBack,  borderwidth=0, highlightthickness=0)
    cardBackComputer.image = cardBack
    cardBackComputer.place(relx=.9, rely=.3)

    #outputs the number of cards of the player and computer to the GUI
    playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Comic Sans MS", 20))
    playerNumCards.place(relx= 0, rely=.0)
    labels.append(playerNumCards)
    computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Comic Sans MS", 20))
    computerNumCards.place(relx= 0, rely=0)
    labels.append(computerNumCards)

    instructionButton = Button(rootWar, text="?", font=("Tahoma",30), relief=RIDGE, command=lambda: instructionsWar(audioFromMenu))
    instructionButton.place(relx = .95,rely = .85)

    flip = Button(rootWar, text ="FLIP",  font=("Tahoma",25), relief=RIDGE, command=lambda: flipCard())
    flip.place(relx=.465, rely = .3)

    # creates two threads. Listener and Speaker. Listener's worker function continuosuly listens for output.
    # Speaker's work function continuously looks if they need to output something
    if audioFromMenu == 1:   
        audioSpeakerThread = threading.Thread(target=outPutAudioWar)
        audioSpeakerThread.start()
        audioListenerThread = threading.Thread(target=audioListenerWar)
        audioListenerThread.start()

    #audio ouput
    outputWAR.put("Welcome to War. Say flip anytime to flip card. Say quit anytime to end. Say score anytime for the score.")

    #visual output
    if audioFromMenu == 1:
        commandsWar = Label(rootWar, text= "Welcome to War. Say flip anytime to flip card or press the button. \nPress the '?' button for instructions or say 'help' or 'instructions'.\n Say 'score' anytime for the score. Say 'quit' anytime to end.",  font=("Tahoma", 20),  bg='#8B0000', foreground="white")
    elif audioFromMenu == 2:
        commandsWar = Label(rootWar, text= "Welcome to War. Press the flip button to flip cards. \nPress the '?' button for instructions.",  font=("Tahoma", 20),  bg='#8B0000', foreground="white")
    commandsWar.place(relx= .5, rely= .87, anchor=CENTER)

    rootWar.mainloop()
    endWAR =1 
    if audioFromMenu == 1: #if window is exited attempts to close audio 
        process.terminate()
    os._exit(0)