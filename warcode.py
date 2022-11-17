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

def cardTie(player_hand, computer_hand):
    cardPlayedPTie = []
    cardPlayedCTie  = []
    
    if player_hand.size >=4:
        for i in range(4):
            cardPlayedPTie.append(player_hand.random_card(remove = True))
    elif player_hand. size == 3:
        for i in range(3):
            cardPlayedPTie.append(player_hand.random_card(remove = True))
    elif player_hand.size == 2:
        for i in range(2):
            cardPlayedPTie.append(player_hand.random_card(remove = True))
    elif player_hand.size == 1: 
        cardPlayedPTie.append(player_hand.random_card(remove = True))

    if computer_hand.size >=4:
        for i in range(4):
            cardPlayedCTie.append(computer_hand.random_card(remove = True))
    elif computer_hand.size == 3:
        for i in range(3):
            cardPlayedCTie.append(computer_hand.random_card(remove = True))
    elif computer_hand.size == 2:
        for i in range(2):
            cardPlayedCTie.append(computer_hand.random_card(remove = True))
    elif computer_hand.size == 1: 
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
            exit
    elif valueCompareTie == 2:
        for cardP in cardPlayedPTie:
            computer_hand.add(cardP)
        for cardC in cardPlayedCTie:
            computer_hand.add(cardC)
        if player_hand.size == 0:
            print("Player Lost")
            exit
    
    return player_hand, computer_hand
deck = pydealer.Deck()
deck.shuffle()

player_hand = pydealer.Stack()
player_hand += deck.deal(26)
computer_hand = pydealer.Stack()
computer_hand +=  deck.deal(26)

while True:
 
    if player_hand.size == 0:
        print("Player Lost")
        break
    elif computer_hand.size == 0:
        print("Computer Lost")
        break

    computer_hand.shuffle()
    player_hand.shuffle()
    cardPlayedP = player_hand.random_card(remove = True)
    cardPlayedC = computer_hand.random_card(remove = True)
    valueCompare = compareCards(str(cardPlayedP), str(cardPlayedC))

    if valueCompare == 0: # cards are equal 
        #1 2 3 and then flip 
        print("equal")
        computer_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
        player_hand, computer_hand = cardTie(player_hand, computer_hand)
    elif valueCompare == 1:
        #print(str(cardPlayedP), "is greater than", str(cardPlayedC))
        player_hand.add(cardPlayedC)
        player_hand.add(cardPlayedP)
    elif valueCompare == 2:
        #print(str(cardPlayedC),"is greater than", str(cardPlayedP))
        computer_hand.add(cardPlayedC)
        computer_hand.add(cardPlayedP)
    print(player_hand.size,"        ", computer_hand.size)
    

         