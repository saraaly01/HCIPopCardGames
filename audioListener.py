import speech_recognition as sr
import re

# If the function is acting up. Uncomment lines 29 and 30 in order to see more of whats happening.

# given a list of desired words, getInput will get audio input from the user and 
# parse the input to determine whether the input contains one or more of the desired words
# ex: the getInput(('yes', 'no')) function is run on various audio input.

# "Yes" -> getInput('yes', 'no') == 'yes'
# "Yes yes yes" -> getInput('yes', 'no') == 'yes'
# "Yes push the button" -> getInput('yes', 'no') == 'yes'
# "yes no push the button" -> getInput('yes', 'no') == 'More than one desired word was found.'
# "hello, my name is Bob" -> getInput('yes', 'no') == 'No desired word was found.'

# Note: getInput function will not work if a word in desiredWords is a contraction such as don't, isn't or mustn't
# I can make this function work with contractions in the future, but I'll do it once there is no other work to do.
def getInput(desiredWords):

    
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    try:
        rawAudioInput = r.recognize_google(audio, language="en")
        #splits the audio into a list of words
        splitInput = re.split("[\W]+", rawAudioInput)
        # print("Raw Audio Input: ", rawAudioInput)
        # print("Split input: ", splitInput)

        # keeps track of all the words from desiredWords that were found in the audio input
        foundWord = ""
        
        for inputWord in splitInput:
            for desiredWord in desiredWords:
                # if the current word from the input is a match:
                if inputWord.lower() == desiredWord.lower():
                    
                    #if its the first word to be found:
                    if foundWord == "":
                        foundWord = inputWord
                    #if a different word has already been found:
                    elif foundWord != inputWord:
                        return "More than one desired word was found."
        
        if foundWord == "":
            return "No desired word was found."
        else:
            return foundWord
    
    #implements error handling in case the audio parser throws an error
    except sr.RequestError:
        return "error"
    except sr.UnknownValueError:
        return "unable to recognize speech"

getInput()


