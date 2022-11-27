import pydealer
import numpy as np
from enum import Enum
import speech_recognition as sr
import os
from gtts import gTTS
import time
from playsound import playsound

answer = "hi"
playAgain = ""
r = sr.Recognizer()
mic = sr.Microphone()

#function that allows audio output
def speak(x, y):
    myobj = gTTS(text=x, lang='en', slow=False)
    myobj.save(y + ".mp3")
    playsound(y + ".mp3")

#function that allows audio input and recognition
def recognize():
    print("start talking")
    with mic as source:
        try:
            r.adjust_for_ambient_noise(source=source, duration=1)
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='en', show_all=True)
            print(text)
            return str(text)
        except:
            print("cant recognize speech")
            pass
    print("done talking")

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
    #Logic for switching the value of an ace per game rules
    if score > 21:
        if 11 in mylist:
            mylist.remove(11)
            mylist.append(1)
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
    k=1

    while keepPlaying == True:

        # Sets up the Game
        deck = pydealer.Deck()
        deck.shuffle()
        player_hand = pydealer.Stack()
        dealer_hand = pydealer.Stack()
        dealer_hand += deck.deal(1)
        player_hand += deck.deal(2)

        # Logic for each turn
        continueGame = True
        while continueGame == True:
            # Let the user know the state of the game

            voiceMessage = "dealer has "
            for i in dealer_hand:
                voiceMessage += str(i)
            speak(voiceMessage, str(k))
            k = k + 1
            time.sleep(3)
            speak("Dealer hand score is " + str(hand_score(dealer_hand)), str(k))
            k = k + 1
            time.sleep(3)

            voiceMessage = "you have "
            for i in player_hand:
                voiceMessage += str(i)
            speak(voiceMessage, str(k))
            k = k + 1
            time.sleep(3)
            speak("Your hand score is " + str(hand_score(player_hand)), str(k))
            k = k + 1
            time.sleep(3)
            if hand_score(player_hand) == 21:
                continueGame = False
            else:
                speak("Please choose: Hit or Stand", str(k))
                k = k + 1
                time.sleep(3)
                answer = recognize()
                #print_status(dealer_hand, player_hand)

                #Gets user decision
                try:
                    while answer.find('hit') == -1 and answer.find('stand') == -1:
                        speak("Would you like to hit or stand?", str(k))
                        k = k + 1
                        time.sleep(3)
                        answer = recognize()
                except:
                    continue

                if answer.find('hit') != -1:
                    player_hand += deck.deal(1)
                    if hand_score(player_hand) >= 21:
                        voiceMessage = "you have "
                        for i in player_hand:
                            voiceMessage += str(i)
                        speak(voiceMessage, str(k))
                        k = k + 1
                        time.sleep(3)
                        speak("Your hand score is " + str(hand_score(player_hand)), str(k))
                        k = k + 1
                        time.sleep(3)
                        continueGame = False
                elif answer.find('stand') != -1:
                    while hand_score(dealer_hand) < 17:
                        dealer_hand += deck.deal(1)
                        voiceMessage = "dealer has "
                        for i in dealer_hand:
                            voiceMessage += str(i)
                        speak(voiceMessage, str(k))
                        k = k + 1
                        time.sleep(3)
                        speak("Dealer hand score is " + str(hand_score(dealer_hand)), str(k))
                        k = k + 1
                        time.sleep(3)
                    continueGame = False

        # Game is over, computing results
        gameResult = ""
        if hand_score(dealer_hand) == hand_score(player_hand):  # if tie
            gameResult = "push"
        elif hand_score(dealer_hand) > 21:  # if dealer bust
            wins += 1
            gameResult = "Dealer Bust"
        elif hand_score(dealer_hand) > hand_score(player_hand):  # if dealer > player
            losses += 1
            gameResult = "Dealer Won"
        elif hand_score(player_hand) == 21:  # if player got 21
            wins += 1
            gameResult = "Player hits 21. Player Wins."
        elif hand_score(player_hand) > 21:  # if player bust
            losses += 1
            gameResult = "Player Bust"
        else:  # if player > dealer
            wins += 1
            gameResult = "Player Wins"

        # Outputing results
        #print_status(dealer_hand, player_hand)
        speak(gameResult + ", You have " + str(wins) + " wins and " + str(losses) + " losses", str(k))
        k = k + 1
        time.sleep(3)

        # Game Over: Play another game?
        playAgain = "hi"
        while playAgain.find('yes') == -1 and playAgain.find('no') == -1:
            speak("Would you like to play another game?", str(k))
            k = k + 1
            time.sleep(3)
            try:
                playAgain = recognize()
            except:
                continue
        if playAgain.find('no') != -1:
            keepPlaying = False

main()