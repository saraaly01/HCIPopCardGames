import pydealer
import time
from gtts import gTTS
import time
import os
import speech_recognition as sr
answer = ""
type = ""
wins = 0
losses = 0
r = sr.Recognizer()
#r.adjust_for_ambient_noise(source, duration=1)
mic = sr.Microphone()
keepPlaying=True
playAgain=""
answer=""

def speak(x,y):
    # Language in which you want to convert
    #language = 'en'
    myobj = gTTS(text=x, lang='en', slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save(y+".mp3")
    # Playing the converted file
    os.system("start "+y+".mp3")

def recognize():
   # r = sr.Recognizer()
   # mic = sr.Microphone()
        print("start talking")
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source=source, duration=1)
                audio = r.listen(source,timeout=5)
                text = r.recognize_google(audio, language = 'en', show_all = True )
                print(text)
                return str(text)
            except:
                print("cant recognize speech")
                pass
        print("done talking")

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


while keepPlaying:
    deck = pydealer.Deck()
    deck.shuffle()

    player_hand = pydealer.Stack()
    dealer_hand = pydealer.Stack()
    dealer_hand += deck.deal(1)
    player_hand += deck.deal(2)

    while True:
        print("dealer hand: ")
        print(dealer_hand)
        print("dealer hand value: " + str(hand_score(dealer_hand)))
        print("player hand: ")
        print(player_hand)
        print("player hand value: " + str(hand_score(player_hand)))
        greet="dealer has "
        for i in dealer_hand:
            greet+=str(i)
        speak(greet,"dh")
        time.sleep(5)
        speak("Dealer hand score is "+str(hand_score(dealer_hand)),"dh")
        time.sleep(5)
        if hand_score(player_hand) >= 22:
            losses += 1

            print('wins:', wins, '\nlosses:', losses)
            speak("Player bust, You have "+str(wins)+" wins and "+str(losses)+" losses","ph")
            time.sleep(5)
            while True:
                speak("Would you like to play another game, Yes or No?", "ph")
                time.sleep(5)
                playAgain=recognize()

                if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                    continue
                else:
                    if playAgain.find('no') != -1:
                        keepPlaying=False
                break
            break

        while True:
            greet = "you have "
            for i in player_hand:
                greet += str(i)
            speak(greet, "dh")
            time.sleep(5)
            speak("Your hand score is " + str(hand_score(player_hand)), "dh")
            time.sleep(5)
            speak("Please choose: Hit or Stand","dh")
            time.sleep(5)
            answer = recognize()

            if answer.find('hit') == -1 and answer.find('stand') == -1:
                continue

            else:
                if answer.find('hit') != -1:
                    answer='hit'
                elif answer.find('stand') != -1:
                    answer='stand'
                break

        if answer == 'hit':
            player_hand += deck.deal(1)
            continue

        if answer == 'stand':
            while True:
                dealer_hand += deck.deal(1)
                print("dealer hand: ")
                print(dealer_hand)
                print("dealer hand value: " + str(hand_score(dealer_hand)))
                print("player hand: ")
                print(player_hand)
                print("player hand value: " + str(hand_score(player_hand)))
                greet = "dealer has "
                for i in dealer_hand:
                    greet += str(i)
                speak(greet, "dh")
                time.sleep(5)
                speak("Dealer hand score is " + str(hand_score(dealer_hand)), "dh")
                time.sleep(5)
                greet = "you have "
                for i in player_hand:
                    greet += str(i)
                speak(greet, "dh")
                time.sleep(5)
                speak("Your hand score is " + str(hand_score(player_hand)), "dh")
                time.sleep(5)
                if hand_score(dealer_hand) >= 17:
                    break
                time.sleep(1)

        if hand_score(dealer_hand) == hand_score(player_hand):

            print('wins:', wins, '\nlosses:', losses)
            speak("Push, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
            time.sleep(5)
            while True:
                speak("Would you like to play another game, Yes or No?", "ph")
                time.sleep(5)
                playAgain = recognize()
                if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                    continue
                else:
                    if playAgain.find('no') != -1:
                        keepPlaying = False
                break

            break

        elif hand_score(dealer_hand) > 21:
            wins += 1
            print('wins:', wins, '\nlosses:', losses)
            speak("Dealer bust, you have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
            time.sleep(5)
            while True:
                speak("Would you like to play another game, Yes or No?", "ph")
                time.sleep(5)
                playAgain=recognize()
                if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                    continue
                else:
                     if playAgain.find('no') != -1:
                        keepPlaying=False
                break
            break

        elif hand_score(dealer_hand) > hand_score(player_hand):
            losses += 1
            speak("Dealer won, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
            time.sleep(5)
            print('wins:', wins, '\nlosses:', losses)
            while True:
                speak("Would you like to play another game, Yes or No?", "ph")
                time.sleep(5)
                playAgain=recognize()
                if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                    continue
                else:
                    if playAgain.find('no') != -1:
                        keepPlaying=False
                break
            break
        else:
            wins += 1
            speak("Player wins, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
            time.sleep(5)
            print('wins:', wins, '\nlosses:', losses)
            while True:
                speak("Would you like to play another game, Yes or No?", "ph")
                time.sleep(5)
                playAgain=recognize()
                if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                    continue
                else:
                    if playAgain.find('no') != -1:
                        keepPlaying = False
                break
            break


