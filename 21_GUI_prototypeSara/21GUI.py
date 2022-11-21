import pydealer
import numpy as np
from enum import Enum

answer = ""
playAgain = ""

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

# prints the state of the game to the console
def print_status(x, y):
    print("--------------")
    print("Dealer's Hand:")
    print(x)
    print("Dealer's hand score: " + str(hand_score(x)))
    print("--------------")
    print("Player's Hand:")
    print(y)
    print("Player's hand score: " + str(hand_score(y)))
    print("--------------")


def main():
    wins = 0
    losses = 0
    keepPlaying = True

    while keepPlaying == True:

        #Sets up the Game 
        deck = pydealer.Deck()
        deck.shuffle()
        player_hand = pydealer.Stack()
        dealer_hand = pydealer.Stack()
        dealer_hand += deck.deal(1)
        player_hand += deck.deal(2)

        #Logic for each turn
        continueGame = True
        while continueGame == True:
            # Let the user know the state of the game
            print_status(dealer_hand, player_hand)

            #DGets user desision
            answer = ""
            while answer.lower() != 'hit' and answer.lower() != 'stand':
                answer=input("Would you like to hit or stand?")

            if answer.lower() == 'hit':
                player_hand += deck.deal(1)
                if hand_score(player_hand) >= 21:
                    continueGame = False
            elif answer.lower() == 'stand':
                while hand_score(dealer_hand) < 17:
                    dealer_hand += deck.deal(1)
                continueGame = False
            
        # Game is over, computing results
        gameResult = ""
        if hand_score(dealer_hand) == hand_score(player_hand): # if tie
            gameResult = "push"
        elif hand_score(dealer_hand) > 21: # if dealer bust
            wins += 1
            gameResult = "Dealer Bust"
        elif hand_score(dealer_hand) > hand_score(player_hand): # if dealer > player
            losses += 1
            gameResult = "Dealer Won"
        elif hand_score(player_hand) == 21: # if player got 21
            wins += 1
            gameResult = "Natural"
        elif hand_score(player_hand) > 21: # if player bust
            losses += 1
            gameResult = "Player Bust"
        else: #if player > dealer
            wins += 1
            gameResult = "Player Wins"
        
        # Outputing results
        print('wins:', wins, '\nlosses:', losses)
        print_status(dealer_hand, player_hand)
        print(gameResult + ", You have " + str(wins) + " wins and " + str(losses) + " losses")         
        
        # Game Over: Play another game?
        playAgain = ""
        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
            playAgain = input("Would you like to play another game? Yes or No?")
        if playAgain.lower() == 'no':
            keepPlaying = False

main()