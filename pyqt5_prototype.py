from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import speech_recognition as sr
from gtts import gTTS
from time import sleep
import sys
import os

# Get any input
def getInput():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    #implements error handling in case the audio parser throws an error
    try:
        return r.recognize_google(audio, language="en")
    except:
        return ""

#given text, play that text as audio output
def playOutput(textInp):
    #function transforms text to speech from the "support specialist"
    myobj = gTTS(text=textInp, lang='en', tld='us', slow=False)
    myobj.save("test.mp3")
    os.system("mpg123 test.mp3")
    print("Input is ready to be taken")


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        playOutput("Say 'Yes' or click the button to increment the click counter. For debugging purposes, whatever audio input the computer is able to pick up is printed to the console.")
        i = 0
        while True:
            input = getInput()
            print("Current input: " + input)
            if input == 'yes':
                self.progress.emit(i + 1)
                i += 1
            if input == 'no':
                self.finished.emit()
                break

# Main GUI
class Window(QMainWindow):
    
    #Constructor Method
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()
        self.runLongTask()

    #Seting up the graphics
    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        self.centralWidget.setLayout(layout)
        self.countBtn.setGeometry(200, 150, 100, 300)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    # Method that creates the multiple threads
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.countClicks)
        # Step 6: Start the thread
        self.thread.start()


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())
