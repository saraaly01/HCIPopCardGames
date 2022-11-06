#war game
import pydealer
import time
from gtts import gTTS
import time
import os
import speech_recognition as sr

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


deck = pydealer.Deck()
deck.shuffle()

player_hand = pydealer.Stack()
player_hand += deck.deal(26)
computer_hand = pydealer.Stack()
computer_hand +=  deck.deal(26)

while True:
 
    if player_hand.size == 0 or computer_hand.size == 0:
        break   
    computer_hand.shuffle()
    player_hand.shuffle()
    cardPlayedP = player_hand.random_card(remove = True)
    cardPlayedC = computer_hand.random_card(remove = True)

    valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))
    if valueCompare == 0:
        print("CARDS ARE EQUAL")
        player_hand.add(cardPlayedP)
        computer_hand.add(cardPlayedC)

    elif valueCompare == 1:
        #print(str(cardPlayedP), "is greater than", str(cardPlayedC))
        player_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
    elif valueCompare == 2:
        #print(str(cardPlayedC),"is greater than", str(cardPlayedP))
        computer_hand.add(cardPlayedC)
        computer_hand.add(cardPlayedP)
    print(player_hand.size,"        ", computer_hand.size)
    
"""         while valueCompare == 0:
            cardPlayedP1= player_hand.random_card(remove = True)
            cardPlayedP2= player_hand.random_card(remove = True)
            cardPlayedP3= player_hand.random_card(remove = True)
            cardPlayedPTIE= player_hand.random_card(remove = True)
            cardPlayedC1 = computer_hand.random_card(remove = True)
            cardPlayedC2 = computer_hand.random_card(remove = True)
            cardPlayedC3= computer_hand.random_card(remove = True)
            cardPlayedCTIE= computer_hand.random_card(remove = True)
            valueCompare = compareCards(str(cardPlayedPTIE), str(cardPlayedCTIE))
            if valueCompare == 1:
                player_hand.add(cardPlayedC1,cardPlayedC2, cardPlayedC3, cardPlayedCTIE, cardPlayedP1,  cardPlayedP2,  cardPlayedP3, cardPlayedPTIE)
            elif valueCompare == 2:
                computer_hand.add(cardPlayedC1,cardPlayedC2, cardPlayedC3, cardPlayedCTIE, cardPlayedP1,  cardPlayedP2,  cardPlayedP3, cardPlayedPTIE) """
