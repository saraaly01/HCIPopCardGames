# HCIPopCardGames

## PopCard Games is an accessible card game hub.
   The program offers the games 21 and War. The games can be played with and without voice and sound. The program uses tkinter for the GUI, and multithreading and subprocesses along with Google's text to speech and speech recognition for the voice/sound feature. 
 
## Installations
Install python (a version atleast 3.10.6 will work)
- pip install tk (tkinter) 
- pip install Pillow (requirements might be satified by previous installation but just incase)
- pip install pydealer
- pip install SpeechRecognition
- pip install gTTS
- pip install pyaudio
- pip install numpy

The mpg123 files do not need to be installed as they are already in the working directory. 

## How to run
 Install the packages from above. Once you install python you can copy this command:
 
 pip install tk Pillow pydealer SpeechRecognition gTTS numpy pyaudio

 After the repository is cloned, you only need to run the "menu.py" file (python menu.py) after moving into the "Final" directory.
 
 ## File Descriptions
 
 menu.py : Menu interface of the game. Allows users to hear instructions and speak input. Also allows users to read instructions and click on input. Allows users to pick if they want to play the game with audio or silent, and lets them choose 21 or war which will go to gui21.py and warGUI.py respectively. 
 
 warGUI.py: The game of War. GUI component and audio component (if user picks this from the menu). Uses pydealer and tkinter for visual and card package.
 
 gui21.py: The game of 21. GUI component and audio component (if user picks this from the menu). Uses pydealer and tkinter for visual and card package. 
 
 instructionsWar.py and instructions21.py: Called if the user requests instructions on the respective games. Mostly just text on a window.
 
 globalFunctions: Two functions that are used repeatedly by all the programs. Insertimage function is to display an image on the GUI. Getinput function is a way to send words that we are waiting for the user to say and check if they are saying it.
 
 Cards: a directory with all the images of the 52 cards plus one image of the back of a card.
 
