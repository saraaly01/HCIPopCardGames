from tkinter import *
from PIL import Image, ImageTk
import pydealer
import time
from gtts import gTTS
import os
import speech_recognition as sr
from playsound import playsound
#pip install playsound==1.2.2
from datetime import datetime
import threading
import subprocess



def inputCheck():    
    myInput = getInput()
    while myInput != 'yes':    
        if myInput == "quit":
            playOutput("Thank you for playing, have a nice day.")
            quitPlaying  = 1
            break
        myInput = getInput()
    return


def getInput():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    #implements error handling in case the audio parser throws an error
    try:
        return r.recognize_google(audio, language="en")
    except:
        return ""
    


 

def playOutput(textInp):
    #date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    #filename = "test"+date_string+".mp3"
    myobj = gTTS(text=textInp, lang='en', tld='us', slow=False)
    myobj.save('test.mp3')
    os.system("mpg123 test.mp3")

    
width = int(250/2.5)
height = int(363/2.5)
def compareCards(card1, card2): #return 1 if card1 greater, return 2 if card2 greater, return 0 if tie
    cardOne = card1.split()
    cardOne = cardOne[0]
    cardTwo = card2.split()
    cardTwo = cardTwo[0]
    if cardOne == cardTwo:
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
    if int(cardOne) > int(cardTwo):
        return 1
    elif int(cardTwo) > int(cardOne):
        return 2

def cardTie(player_hand, computer_hand, root):
    labels = []
    cardPlayedPTie = []
    cardPlayedCTie  = []
    playerX = .22
    computerX = .7
    for i in range(4):
        if player_hand.size != 0:
            cardPlayedP = player_hand.random_card(remove = True)
            cardPlayedPTie.append(cardPlayedP)
            img= insertImage(cardPlayedP,root)
            img.place(relx = playerX + (.05 *i), rely = .3)
            labels.append(img)

        if computer_hand.size != 0:
            cardPlayedC = computer_hand.random_card(remove = True)
            cardPlayedCTie.append(cardPlayedC)
            img= insertImage(cardPlayedC,root)
            img.place(relx = computerX - (.05 *i), rely = .3)
            labels.append(img)
    
    #root.update()
    valueCompareTie = compareCards(str(cardPlayedP), str(cardPlayedC))
    if valueCompareTie == 0: # cards are equal 
        tie = Label(root, text= "TIE, CARDS BACK!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
        tie.place(relx =.45, rely = .2)
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        tie.destroy()
    elif valueCompareTie == 1:
        playOutput("You have won the war, and so you will get all 10 cards.")
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            player_hand.add(cardC)
    elif valueCompareTie == 2:
        playOutput("Unfortunatly, you have lost, and the computer will get all 10 cards.")
        for cardP in cardPlayedPTie:
            computer_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
    

    return player_hand, computer_hand, labels, valueCompareTie

def insertImage(cardPlayed,root):
    cardOutput = Image.open("cards\\" + str(cardPlayed) + ".png")
    test = cardOutput.resize((width, height))
    test = ImageTk.PhotoImage(test)
    imglabel = Label(root, image=test)
    imglabel.image = test
    return imglabel


def intialize(rootIN):

    labels = []
    valueCompare = -1
    deck = pydealer.Deck()
    deck.shuffle()

    player_hand = pydealer.Stack()
    player_hand += deck.deal(26)
    computer_hand = pydealer.Stack()
    computer_hand +=  deck.deal(26)

    root = Toplevel(rootIN)
    root.title('PopCardGames')
    root['background']='#8B0000'
    # window width of screen
    window_width= rootIN.winfo_screenwidth()
    # window height of screen              
    window_height= rootIN.winfo_screenheight()

    # set root winow to screen size           
    root.geometry("%dx%d" % (window_width,  window_height))
    gameTitle = Label(root, text= "WAR", font=("Comic Sans MS", 30))
    gameTitle.place(relx = 0.45, rely = 0)

    player = Label(root, text= "PLAYER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    player.place(relx =.2, rely = .1)
    computer = Label(root, text= "COMPUTER", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
    computer.place(relx =.7, rely = .1)

    cardBack = Image.open("cards\\card.png")
    cardBack = cardBack.resize((width, height))
    cardBack = ImageTk.PhotoImage(cardBack)

    cardBackPlayer= Label(root, image=cardBack)
    cardBackPlayer.image = cardBack
    cardBackPlayer.place(relx=0.02, rely=.3)

    cardBackComputer = Label(root, image=cardBack)
    cardBackComputer.image = cardBack
    cardBackComputer.place(relx=.9, rely=.3)

    playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Comic Sans MS", 20))
    playerNumCards.place(relx= 0, rely=.0)
    computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Comic Sans MS", 20))
    computerNumCards.place(relx= 0, rely=0)
    #flip = Button(root, text ="PLAY CARD", command=threading.Thread(target=inputCheck).start)
    #flip.place(relx=.45, rely = .8)
    start = 1
    quitPlaying = 0
    root.update()
    



    while True:   
        computer_hand.shuffle()
        player_hand.shuffle()

        if not start:
            imgPlayedP.destroy()
            imgPlayedC.destroy()
            if valueCompare == 1:
                playerWin.destroy()
            else:
                computerWin.destroy()
            for label in labels:
                label.destroy()
        playOutput("Say yes to flip")
        x= threading.Thread(target=inputCheck, daemon=True)
        x.start()
        x.join()
        root.after(2000)
        start = 0
        print("HEYYYYY")
        playerNumCards.destroy()
        computerNumCards.destroy()

        playerNumCards = Label(cardBackPlayer, text = str(player_hand.size), font=("Comic Sans MS", 20))
        playerNumCards.place(relx= 0, rely=.0)
      
        computerNumCards = Label(cardBackComputer, text = str(computer_hand.size), font=("Comic Sans MS", 20))
        computerNumCards.place(relx= 0, rely=0)
        

        
        if player_hand.size == 0:
            playerWinsGame = Label(root, text = "COMPUTER WINS. GAME OVER", font=("Comic Sans MS", 40))
            playOutput("You Lost. Computer Wins")
            playerWinsGame.place(relx= .4, rely=.6)
            time.sleep(3)
            break
        elif computer_hand.size == 0:
            computerWinsGame = Label(root, text = "PLAYER WINS. GAME OVER", font=("Comic Sans MS", 40))
            playOutput("Computer Lost. You Win!")
            computerWinsGame.place(relx= .4, rely=.6)
            time.sleep(3)
            break



        cardPlayedC = computer_hand.random_card(remove = True)
        imgPlayedC = insertImage(cardPlayedC,root)
        imgPlayedC.place(relx=0.8, rely=.3) 
        playOutput("Ok. The computer flips a " + str(cardPlayedC) + ".")
        cardPlayedP = player_hand.random_card(remove = True)
        imgPlayedP = insertImage(cardPlayedP,root)
        imgPlayedP.place(relx=0.12, rely=.3) 
        playOutput("You flip a" + str(cardPlayedP) + ".")

        valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))
        if valueCompare == 0: # cards are equal 
            playOutput("This is equal to " + str(cardPlayedC) + " and so there will be a war. Say 'War' to continue.")
            tie = Label(root, text= "TIE, WAR!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
            tie.place(relx =.45, rely = .2)
            myInput = getInput()
            while myInput != 'War':    
                if myInput == "quit":
                    playOutput("Thank you for playing, have a nice day.")
                    quitPlaying  = 1
                    break
                myInput = getInput()
            if quitPlaying:
                break
            tie.destroy()
            player_hand, computer_hand, labels, valueCompare = cardTie(player_hand, computer_hand,root)
            if valueCompare == 0:
                player_hand.add(cardPlayedP)
                computer_hand.add(cardPlayedC)

        if valueCompare == 1:
            playOutput("This is higher than" + str(cardPlayedC) + " and so you get both cards.")
            playerWin = Label(root, text= "PLAYER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
            playerWin.place(relx =.15, rely = .2)
            player_hand.add(cardPlayedC)
            player_hand.add(cardPlayedP)
        elif valueCompare == 2: #computer won the card
            playOutput("This is lower than" + str(cardPlayedC) + " and so you get both cards.")
            computerWin = Label(root, text= "COMPUTER's WIN!", font=("Comic Sans MS", 20), bg ='#8B0000', relief="solid")
            computerWin.place(relx =.65, rely = .2)
            computer_hand.add(cardPlayedC)
            computer_hand.add(cardPlayedP)
        outputString = "the player hand size is now " + str(player_hand.size) + " and the computer hand size is now " + str(computer_hand.size)
        playOutput(outputString)
    

        
    root.destroy()
    root.mainloop()
    

    
    
if __name__ == '__main__':
    main()