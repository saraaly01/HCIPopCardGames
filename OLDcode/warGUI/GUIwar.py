import pydealer
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import speech_recognition as sr
import os, sys, time
from gtts import gTTS
import queue, threading

global output, end
global computer_hand, player_hand, cardPlayedP, cardPlayedC, cardBackPlayer, cardBackComputer
global root, warWait, flip
end = 0 #signals the end of the game
warWait = 0 #variable determines if we are awaiting a war sequence 
output = queue.Queue()  #output queue will hold messages that a thread will output with voice


#outPutAudio is one of the worker functions
def outPutAudio():
    global flip, output, end
    while True: #thread is constantly checking if there is a message on the queue it has to output
        if end:
            root.destroy()
            return
        while output.empty() == False: # if the queue is not empty the thread will get ready to output the message
            msg = output.get(0)
            flip['state'] = DISABLED #if output is being said, user can not hit the button
            #next three lines uses google's package for text to speech
            myobj = gTTS(text=msg, lang='en', tld='us', slow=False)  
            myobj.save("test.mp3")
            os.system("mpg123 test.mp3")   
            if not warWait: #if we are not waiting for a war we can turn the flip button back on
                flip['state'] = NORMAL
    


#audioListener is the other worker function
def audioListener(): 
    global output,end
    r = sr.Recognizer()
    mic = sr.Microphone()
    while True: #constantly using the microphone to check if the user is saying something
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source=source, duration=1)
                audio = r.listen(source, timeout=5)
                msg = r.recognize_google(audio, language='en')
                print(msg)  #for debugging reasons prints msg
            except:
                msg = "-"
        msg = msg.lower()
        if msg== "flip":  #user picked flip and calls flipCard function if we are not waiting for a war
            if not warWait:
                flipCard()
        if msg == "war":
            cardTie() #cardTie is the function that deals with the war
        if msg== "score": #prints out how many cards each player has
            output.put("You have" + str(player_hand.size) + "cards. Computer has" + str(computer_hand.size) + "cards.")
        if msg == "quit" or end: #ends the program
            end = 1
            return
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

def finish():
    global flip
    #gets rid of flip button
    flip.destroy()
    if player_hand.size == 0:
        #computer wins
        playerWinsGame = Label(root, text = "COMPUTER WINS. GAME OVER", font=("Comic Sans MS", 40))
        playerWinsGame.place(relx= .4, rely=.6)
        output("Computer Wins. Game Over.")
    elif computer_hand.size == 0:
        #player wins
        computerWinsGame = Label(root, text = "PLAYER WINS. GAME OVER", font=("Comic Sans MS", 40))
        computerWinsGame.place(relx= .4, rely=.6)
        output("Player Wins. Game Over.")
    return

#function handles a tie in war
def cardTie():
    global root, labels, player_hand, computer_hand, cardPlayedP, cardPlayedC, flip, warWait
    #cardPlayedP and cardPlayedC are the cards that resulted in the war to begin with, we have to keep track of them to return them back
    warWait = 0 #we are no longer waiting for the war button/command to be said because it is about to be dealt with
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
            #outputs each card to the screen on the players side
            cardPlayedPcurr = player_hand.random_card(remove = True)
            cardPlayedPTie.append(cardPlayedPcurr)
            output.put("You flip a " + str(cardPlayedPcurr))
            img= insertImage(cardPlayedPcurr,root)
            img.place(relx = playerX + (.05 *i), rely = .3)
            labels.append(img)

        if computer_hand.size != 0:
            #outputs each card to the screen on the computers side
            cardPlayedCcurr = computer_hand.random_card(remove = True)
            cardPlayedCTie.append(cardPlayedCcurr)
            output.put("Computer flips a " + str(cardPlayedCcurr))
            img= insertImage(cardPlayedCcurr,root)
            img.place(relx = computerX - (.05 *i), rely = .3)
            labels.append(img)
    
    valueCompareTie = compareCards(str(cardPlayedPcurr), str(cardPlayedCcurr))

    if valueCompareTie == 0: # cards are equal, everyone gets their cards back 
        output.put("Tie again. Everyone gets their cards back.")
        tie = Label(root, text= "TIE, CARDS BACK!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        tie.place(relx =.45, rely = .2)
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        labels.append(tie)
        player_hand.add(cardPlayedP)
        computer_hand.add(cardPlayedC)
    elif valueCompareTie == 1: #players receives all the cards
        output.put("You receive the cards")
        playerWin = Label(root, text= "PLAYER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        playerWin.place(relx =.15, rely = .2)
        labels.append(playerWin)
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            player_hand.add(cardC)
        player_hand.add(cardPlayedP)
        player_hand.add(cardPlayedC)
    elif valueCompareTie == 2: #computer receives all the cards
        output.put("Computer receives the cards")
        computerWin = Label(root, text= "COMPUTER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        computerWin.place(relx =.65, rely = .2)
        labels.append(computerWin)
        for cardP in cardPlayedPTie:
            computer_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        computer_hand.add(cardPlayedP)
        computer_hand.add(cardPlayedC)
    
    flip['state'] = NORMAL #flip button can now be clicked again as War has been dealt with 

    if computer_hand.size == 0 or player_hand.size == 0 and (warWait == 0):
        #if computer or player has no cards the game is over, calls finish function
        finish()
    return

def insertImage(cardPlayed,root):
    #function prepares label for GUI and sends its back to be placed 
    width = int(250/2.5)
    height = int(363/2.5) #cards got resized to look smaller on the GUI
    cardOutput = Image.open("cards\\" + str(cardPlayed) + ".png")
    test = cardOutput.resize((width, height))
    test = ImageTk.PhotoImage(test)
    imglabel = Label(root, image=test)
    imglabel.image = test
    return imglabel

def flipCard():
    #basically the main funciton of the program. Each person flips a card and the cards are compared and dealth with 
    global root, labels
    global cardBackPlayer, cardBackComputer, cardPlayedP, cardPlayedC, computer_hand, player_hand
    global warWait, flip
    computer_hand.shuffle() #shuffles cards to make it more random
    player_hand.shuffle()
    
    for label in labels: 
        #destroys any widegts stored in the labels array to update the GUI
        label.destroy()

    #gets updated number of player cards and outputs it to gui. stores in label array to delete next flip 
    playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Comic Sans MS", 20))
    playerNumCards.place(relx= 0, rely=.0)
    labels.append(playerNumCards)
    #gets updated number of computer cards and outputs it to gui. stores in label array to delete next flip 
    computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Comic Sans MS", 20))
    computerNumCards.place(relx= 0, rely=0)
    labels.append(computerNumCards)

    if computer_hand.size == 0 or player_hand.size == 0 and (warWait == 0):
        #if computer or player has no cards the game is over, calls finish function
        finish()
        return

    #takes a random card out of the player and computers hand and removes it, puts the picture on the GUI, ouputs it with speech to text
    cardPlayedC = computer_hand.random_card(remove = True)
    imgPlayedC = insertImage(cardPlayedC,root)
    imgPlayedC.place(relx=0.8, rely=.3) 
    labels.append(imgPlayedC)
    cardPlayedP = player_hand.random_card(remove = True)
    imgPlayedP = insertImage(cardPlayedP,root)
    imgPlayedP.place(relx=0.12, rely=.3) 
    labels.append(imgPlayedP)
    output.put("You flip a " + str(cardPlayedP) + "The computer flips a " + str(cardPlayedC))

    #calles compareCards to find out which card was higher
    valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))
    if valueCompare == 0: # cards are equal, war will commence
        output.put("Cards Tied. Say WAR to continue. ")
        tie = Label(root, text= "TIE, WAR!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        tie.place(relx =.45, rely = .2)
        labels.append(tie)
        waitWarButton = Button(root, text ="WAR", command=lambda: cardTie())
        waitWarButton.place(relx=.45, rely = .85)
        labels.append(waitWarButton)
        warWait = 1 #this variable signals that we are waiting for a war

    if valueCompare == 1: #player wins the cards
        output.put("You receive the cards")
        playerWin = Label(root, text= "PLAYER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        playerWin.place(relx =.15, rely = .2)
        labels.append(playerWin)
        player_hand.add(cardPlayedC) #player receives both cards to their hand
        player_hand.add(cardPlayedP)

    elif valueCompare == 2: #computer won the card
        output.put("Computer receives the cards")
        computerWin = Label(root, text= "COMPUTER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        computerWin.place(relx =.65, rely = .2)
        labels.append(computerWin)
        computer_hand.add(cardPlayedC) #computer receives both cards to their hand
        computer_hand.add(cardPlayedP)
    return


def intialize():
    #function intializes the GUI
    global root, labels, flip, output, end
    global cardBackPlayer, cardBackComputer,  cardPlayedP, cardPlayedC, computer_hand, player_hand
    labels = [] #labels list holds a list of widgets that need to be deleted constantly to update the GUI

    #sets up the deck, and splits deck evenly between computer and player hand
    deck = pydealer.Deck()
    deck.shuffle()
    player_hand = pydealer.Stack()
    player_hand += deck.deal(26)
    computer_hand = pydealer.Stack()
    computer_hand +=  deck.deal(26)

    #creates window
    root = Tk()
    root.title('War')
    root['background']='#8B0000'
    # window width of screen
    window_width= root.winfo_screenwidth()
    # window height of screen              
    window_height= root.winfo_screenheight()
    # set root winow to screen size           
    root.geometry("%dx%d" % (window_width,  window_height))
    
    #adds some text to GUI
    gameTitle = Label(root, text= "WAR", font=("Comic Sans MS", 30))
    gameTitle.place(relx = 0.45, rely = 0)
    player = Label(root, text= "PLAYER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    player.place(relx =.2, rely = .1)
    computer = Label(root, text= "COMPUTER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    computer.place(relx =.7, rely = .1)

    #adds the backside of the card to represent each players deck, the number of cards they have will be on top of it
    cardBack = Image.open("cards\\card.png")
    cardBack = cardBack.resize((int(250/2.5),int(363/2.5)))
    cardBack = ImageTk.PhotoImage(cardBack)
    cardBackPlayer= Label(root, image=cardBack)
    cardBackPlayer.image = cardBack
    cardBackPlayer.place(relx=0.02, rely=.3)
    cardBackComputer = Label(root, image=cardBack)
    cardBackComputer.image = cardBack
    cardBackComputer.place(relx=.9, rely=.3)

    #creates the widget with number of cards each player has and displays it on top of their "deck"
    playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Comic Sans MS", 20))
    playerNumCards.place(relx= 0, rely=.0)
    labels.append(playerNumCards)
    computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Comic Sans MS", 20))
    computerNumCards.place(relx= 0, rely=0)
    labels.append(computerNumCards)

    flip = Button(root, text ="FLIP", command=lambda: flipCard())
    flip.place(relx=.45, rely = .8)

    # creates two threads. Listener and Speaker. Listener's worker function continuosuly listens for output.
    # Speaker's work function continuously looks if they need to output something
    audioListenerThread = threading.Thread(target=audioListener)
    audioListenerThread.start()
    audioSpeakerThread = threading.Thread(target=outPutAudio)
    audioSpeakerThread.start()
    output.put("Welcome to War. Say flip anytime to flip cards. Say quit anytime to end. Say score anytime to get the score.")
    root.mainloop()
    end = 1 #this part of the program will be reached when they close out their window 
    return
    