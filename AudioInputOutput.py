
#speak function- converts text into mp3 file
def speak(x, y):
    # Language in which you want to convert
    # language = 'en'
    myobj = gTTS(text=x, lang='en', slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save(y + ".mp3")
    # Playing the converted file
    os.system("start " + y + ".mp3")


