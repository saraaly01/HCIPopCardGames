#war game
import pydealer
import time
from gtts import gTTS
import time
import os
import speech_recognition as sr
#from mutagen.mp3 import MP3



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
    #function transforms text to speech from the "support specialist"
    myobj = gTTS(text=textInp, lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")







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

def cardTie(player_hand, computer_hand):
    cardPlayedPTie = []
    cardPlayedCTie  = []
    
    for i in range(4):
        if player_hand.size == 0:
            break
        cardPlayedPTie.append(player_hand.random_card(remove = True))

    for i in range(4):
        if computer_hand.size == 0:
            break 
        cardPlayedCTie.append(computer_hand.random_card(remove = True))

    valueCompareTie = compareCards(str(cardPlayedPTie[len(cardPlayedPTie) - 1]), str(cardPlayedCTie[len(cardPlayedCTie) - 1]))
    if valueCompareTie == 0: # cards are equal 
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
    elif valueCompareTie == 1:
        for cardP in cardPlayedPTie:
            player_hand.add(cardP)
        for cardC in cardPlayedCTie:
            player_hand.add(cardC)
        if computer_hand.size == 0:
            print("Computer Lost")
            playOutput("You have won the war, and so you will get all 5 cards.")
            exit
    elif valueCompareTie == 2:
        for cardP in cardPlayedPTie:
            computer_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        if player_hand.size == 0:
            print("Player Lost")
            playOutput("Unfortunatly, you have lost, and so you will lose all 5 cards.")
            exit
    
    return player_hand, computer_hand


deck = pydealer.Deck()
deck.shuffle()

player_hand = pydealer.Stack()
player_hand += deck.deal(26)
computer_hand = pydealer.Stack()
computer_hand +=  deck.deal(26)

continuePlaying = True
while continuePlaying == True:
 
    if player_hand.size == 0:
        print("Player Lost")
        playOutput("Player Lost")
        break
    elif computer_hand.size == 0:
        print("Computer Lost")
        playOutput("Computer Lost")
        break

    

    computer_hand.shuffle()
    player_hand.shuffle()
    cardPlayedP = player_hand.random_card(remove = True)
    cardPlayedC = computer_hand.random_card(remove = True)
    
    
    playOutput("The Computer's next card is: " + str(cardPlayedC) + ". Say 'Yes' to flip your next card.")
    myInput = getInput()
    while myInput != 'yes':    
        if myInput == "quit":
            playOutput("Thank you for playing, have a nice day.")
            continuePlaying = False
            break
        myInput = getInput()
        print("Input Recieved")
        print(myInput)

    if continuePlaying == False:
        break
    
    playOutput("Ok. Your next card is " + str(cardPlayedP) + ".")

    valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))
    

    if valueCompare == 0: # cards are equal 
        #1 2 3 and then flip 
        print("equal")
        playOutput("This is equal to " + str(cardPlayedC) + " and so there will be a war.")
        computer_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
        player_hand, computer_hand = cardTie(player_hand, computer_hand)
    # player wins turn
    elif valueCompare == 1:
        print(str(cardPlayedP), "is greater than", str(cardPlayedC))
        playOutput("This is higher than" + str(cardPlayedC) + " and so you get both cards.")
        player_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
    # computer wins turn
    elif valueCompare == 2:
        print(str(cardPlayedC),"is greater than", str(cardPlayedP))
        playOutput("This is lower than" + str(cardPlayedC) + " and so the computer gets both cards.")
        computer_hand.add(cardPlayedC)
        computer_hand.add(cardPlayedP)
    outputString = "the player hand size is now " + str(player_hand.size) + " and the computer hand size is now " + str(computer_hand.size)
    playOutput(outputString)
    print(player_hand.size,"        ", computer_hand.size)
    

         