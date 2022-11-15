import pydealer
import cv2
import numpy as np
from gtts import gTTS
import time
import os
import speech_recognition as sr
from PyQt5 import QtCore, QtGui, QtWidgets

answer = ""

r = sr.Recognizer()
# r.adjust_for_ambient_noise(source, duration=1)
mic = sr.Microphone()
#keepPlaying = True
playAgain = ""


def speak(x, y):
    # Language in which you want to convert
    # language = 'en'
    myobj = gTTS(text=x, lang='en', slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save(y + ".mp3")
    # Playing the converted file
    os.system("start " + y + ".mp3")


def recognize():
    # r = sr.Recognizer()
    # mic = sr.Microphone()
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


def print_status(x, y):
    print("Dealer's Hand:")
    print(x)
    print("Dealer's hand score: " + str(hand_score(x)))
    print("--------------")
    print("Player's Hand:")
    print(y)
    print("Player's hand score: " + str(hand_score(y)))
    print("--------------")
    print("--------------")

def main():
    wins = 0
    losses = 0
    keepPlaying = True

    #rebecca_card_dir = "C:\\Users\\btoth\\Desktop\\Fall_2022\\HCI\\HCIPopCardGames\\cards\\cards"
    crd = {"2 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\2_of_diamonds.png",
           "2 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\2_of_hearts.png",
           "2 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\2_of_clubs.png",
           "2 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\2_of_spades.png",
           "3 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\3_of_diamonds.png",
           "3 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\3_of_hearts.png",
           "3 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\3_of_clubs.png",
           "3 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\3_of_spades.png",
           "4 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\4_of_diamonds.png",
           "4 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\4_of_hearts.png",
           "4 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\4_of_clubs.png",
           "4 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\4_of_spades.png",
           "5 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\5_of_diamonds.png",
           "5 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\5_of_hearts.png",
           "5 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\5_of_clubs.png",
           "5 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\5_of_spades.png",
           "6 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\6_of_diamonds.png",
           "6 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\6_of_hearts.png",
           "6 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\6_of_clubs.png",
           "6 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\6_of_spades.png",
           "7 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\7_of_diamonds.png",
           "7 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\7_of_hearts.png",
           "7 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\7_of_clubs.png",
           "7 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\7_of_spades.png",
           "8 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\8_of_diamonds.png",
           "8 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\8_of_hearts.png",
           "8 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\8_of_clubs.png",
           "8 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\8_of_spades.png",
           "9 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\9_of_diamonds.png",
           "9 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\9_of_hearts.png",
           "9 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\9_of_clubs.png",
           "9 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\9_of_spades.png",
           "10 of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\10_of_diamonds.png",
           "10 of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\10_of_hearts.png",
           "10 of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\10_of_clubs.png",
           "10 of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\10_of_spades.png",
           "Jack of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\jack_of_diamonds2.png",
           "Jack of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\jack_of_hearts2.png",
           "Jack of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\jack_of_clubs2.png",
           "Jack of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\jack_of_spades2.png",
           "Queen of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\queen_of_diamonds2.png",
           "Queen of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\queen_of_hearts2.png",
           "Queen of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\queen_of_clubs2.png",
           "Queen of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\queen_of_spades2.png",
           "King of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\king_of_diamonds2.png",
           "King of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\king_of_hearts2.png",
           "King of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\king_of_clubs2.png",
           "King of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\king_of_spades2.png",
           "Ace of Diamonds": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\ace_of_diamonds.png",
           "Ace of Hearts": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\ace_of_hearts.png",
           "Ace of Clubs": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\ace_of_clubs.png",
           "Ace of Spades": "C:\\Users\\nikki\\PycharmProjects\\CSC355-HW5\\cards\\ace_of_spades.png",
           }

    while True:
        speak("Hello, would you like to play this game using keyboard or voice?","dh")
        time.sleep(5)
        mode=recognize()
        try:
            if mode.find('keyboard') == -1 and mode.find('voice') == -1:
                continue
            else:
                if mode.find('keyboard') != -1:
                    mode='keyboard'
                elif mode.find('voice') != -1:
                    mode='voice'
                break
        except:
            continue

    while keepPlaying:

        deck = pydealer.Deck()
        deck.shuffle()
        player_hand = pydealer.Stack()
        # player_hand+=deck.get("Ace of Spades")
        # player_hand+=deck.get("Ace of Hearts")
        dealer_hand = pydealer.Stack()
        dealer_hand += deck.deal(1)
        dealerArrays = np.array(cv2.imread(crd[str(dealer_hand[-1])]))
        player_hand += deck.deal(2)
        playerArrays = np.concatenate((cv2.imread(crd[str(player_hand[0])]), cv2.imread(crd[str(player_hand[1])])), axis=1)
        while True:
            print_status(dealer_hand, player_hand)

            cv2.imshow('Dealer', dealerArrays)
            cv2.waitKey(5000)
            greet = "dealer has "
            for i in dealer_hand:
                greet += str(i)
            speak(greet, "dh")
            time.sleep(5)
            speak("Dealer hand score is " + str(hand_score(dealer_hand)), "dh")
            time.sleep(5)

            if hand_score(player_hand) == 21:
                wins += 1

                cv2.imshow('Player', playerArrays)
                cv2.waitKey(5000)
                greet = "you have "
                for i in player_hand:
                    greet += str(i)
                speak(greet, "dh")
                time.sleep(5)
                speak("Your hand score is " + str(hand_score(player_hand)), "dh")
                time.sleep(5)

                speak("Player wins, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
                time.sleep(5)
                cv2.destroyAllWindows()
                print('wins:', wins, '\nlosses:', losses)
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    cv2.destroyAllWindows()
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain=""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game, Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False

                    break

                break

            elif hand_score(player_hand) >= 22:
                losses += 1

                cv2.imshow('Player', playerArrays)
                cv2.waitKey(5000)
                greet = "you have "
                for i in player_hand:
                    greet += str(i)
                speak(greet, "dh")
                time.sleep(5)
                speak("Your hand score is " + str(hand_score(player_hand)), "dh")
                time.sleep(5)

                print('wins:', wins, '\nlosses:', losses)
                speak("Player bust, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
                time.sleep(5)
                cv2.destroyAllWindows()
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    cv2.destroyAllWindows()
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain=""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game, Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False

                    break

                break

            while True:
                answer=""
                cv2.imshow('Player', playerArrays)
                cv2.waitKey(5000)
                greet = "you have "
                for i in player_hand:
                    greet += str(i)
                speak(greet, "dh")
                time.sleep(5)
                speak("Your hand score is " + str(hand_score(player_hand)), "dh")
                time.sleep(5)
                speak("Please choose: Hit or Stand", "dh")
                time.sleep(5)
                if mode == 'voice':
                    answer = recognize()
                    try:
                        if answer.find('hit') == -1 and answer.find('stand') == -1:
                            continue

                        else:
                            if answer.find('hit') != -1:
                                answer = 'hit'
                            elif answer.find('stand') != -1:
                                answer = 'stand'
                            break
                    except:
                        continue
                else:
                    while answer.lower() != 'hit' and answer.lower() != 'stand':
                        answer=input("Would you like to hit or stand?")
                    break
            if answer.lower() == 'hit':
                player_hand += deck.deal(1)
                playerArrays = np.concatenate(([playerArrays, cv2.imread(crd[str(player_hand[-1])])]), axis=1)
                cv2.imshow('Player', playerArrays)
                cv2.waitKey(5000)

                continue

            if answer.lower() == 'stand':
                while True:
                    dealer_hand += deck.deal(1)
                    dealerArrays = np.concatenate(([dealerArrays, cv2.imread(crd[str(dealer_hand[-1])])]), axis=1)
                    print_status(dealer_hand, player_hand)

                    cv2.imshow('Dealer', dealerArrays)
                    cv2.waitKey(5000)
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
                cv2.destroyAllWindows()
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain = ""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game? Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False
                    break

                break

            elif hand_score(dealer_hand) > 21:
                wins += 1
                print('wins:', wins, '\nlosses:', losses)
                speak("Dealer bust, you have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
                time.sleep(5)
                cv2.destroyAllWindows()
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain = ""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game? Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False
                    break

                break

            elif hand_score(dealer_hand) > hand_score(player_hand):

                losses += 1
                speak("Dealer won, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
                time.sleep(5)
                cv2.destroyAllWindows()
                print('wins:', wins, '\nlosses:', losses)
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    cv2.destroyAllWindows()
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain = ""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game? Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False
                    break

                break
            else:

                wins += 1
                speak("Player wins, You have " + str(wins) + " wins and " + str(losses) + " losses", "ph")
                time.sleep(5)
                cv2.destroyAllWindows()
                print('wins:', wins, '\nlosses:', losses)
                while True:
                    speak("Would you like to play another game, Yes or No?", "ph")
                    time.sleep(5)
                    if mode == 'voice':
                        playAgain = recognize()
                        try:
                            if playAgain.find('yes') == -1 and playAgain.find('no') == -1:
                                continue
                            else:
                                if playAgain.find('no') != -1:
                                    cv2.destroyAllWindows()
                                    keepPlaying = False
                        except:
                            continue
                    else:
                        playAgain = ""
                        while playAgain.lower() != 'yes' and playAgain.lower() != 'no':
                            playAgain = input("Would you like to play another game? Yes or No?")
                        if playAgain.lower() == 'no':
                            keepPlaying = False
                    break

                break

class Ui_Dialog(object):

    def print_something(self):
        main()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.btnRun = QtWidgets.QPushButton(Dialog)
        self.btnRun.setGeometry(QtCore.QRect(150, 100, 75, 23))
        self.btnRun.setObjectName("btnRun")
        self.btnRun.clicked.connect(self.print_something)
        #self.btnRun.clicked.connect(self.bj14.main())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnRun.setText(_translate("Dialog", "Black Jack"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

