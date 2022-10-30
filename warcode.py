# Python program to translate
# speech to text and text to speech
import pydealer
new_ranks = {
    "values": {
        "Ace": 13,
        "King": 12,
        "Queen": 11,
        "Jack": 10,
        "10": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1
    }
}
deck = pydealer.Deck()
deck.shuffle()
hand = deck.deal(7)
print(hand)
print("\n")
print(hand[0])
print(hand[1])
card = str(hand[0])
if hand[0].gt(hand[1]):
    print("greater")
elif hand[0].lt(hand[1]):
    print("less")
else:
    print("tie")
  
""" import speech_recognition as sr
import pyttsx3 
  
# Initialize the recognizer 
r = sr.Recognizer() 
  
# Function to convert text to
# speech
def SpeakText(command):
      
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
      
      
# Loop infinitely for user to
# speak
  
while(1):    
      
    # Exception handling to handle
    # exceptions at the runtime
    try:
          
        # use the microphone as source for input.
        with sr.Microphone() as source2:
              
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.2)
              
            #listens for the user's input 
            audio2 = r.listen(source2)
              
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
  
            print("Did you say ",MyText)
            SpeakText(MyText)
              
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
          
    except sr.UnknownValueError:
        print("unknown error occured") """