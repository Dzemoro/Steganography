from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy

import sys, os

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        self.setWindowTitle("Bitmap Encryptor")
        
        titleText = QLabel()
        titleText.setText("BITMAP")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Comic Sans',50))
        titleText.setStyleSheet("QLabel {color : #cae8d5}")

        titleText2 = QLabel()
        titleText2.setText("STEGANOGRAPHY")
        titleText2.setAlignment(Qt.AlignCenter)
        titleText2.setFont(QFont('Comic Sans',50))
        titleText2.setStyleSheet("QLabel {color : #cae8d5}")

        self.subtitleText = QLabel()
        self.subtitleText.setText(" ")
        self.subtitleText.setAlignment(Qt.AlignCenter)
        self.subtitleText.setFont(QFont('Comic Sans',20))
        self.subtitleText.setStyleSheet("QLabel {color : #84a9ac}")

        self.infoButton = QPushButton()
        self.infoButton.setText("Info")
        self.infoButton.setFont(QFont('Comic Sans',12))
        self.infoButton.setStyleSheet("QPushButton {background : #3b6978}")
        self.infoButton.setStyleSheet("QPushButton {color : #cae8d5}")
        self.infoButton.clicked.connect(self.infoClicked)

        self.checkTextButton = QPushButton()
        self.checkTextButton.setText("Check text")
        self.checkTextButton.setFont(QFont('Comic Sans',12))
        self.checkTextButton.setStyleSheet("QPushButton {background : #3b6978}")
        self.checkTextButton.setStyleSheet("QPushButton {color : #cae8d5}")
        self.checkTextButton.clicked.connect(self.checkTextClicked)

        self.checkResultButton = QPushButton()
        self.checkResultButton.setText("Check result")
        self.checkResultButton.setFont(QFont('Comic Sans',12))
        self.checkResultButton.setStyleSheet("QPushButton {background : #3b6978}")
        self.checkResultButton.setStyleSheet("QPushButton {color : #cae8d5}")
        self.checkResultButton.clicked.connect(self.checkResultClicked)

        encryptButton = QPushButton()
        encryptButton.setText("Write")
        encryptButton.setFont(QFont('Comic Sans',12))
        encryptButton.setStyleSheet("QPushButton {background : #3b6978}")
        encryptButton.setStyleSheet("QPushButton {color : #cae8d5}")
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("Read")
        decryptButton.setFont(QFont('Comic Sans',12))
        decryptButton.setStyleSheet("QPushButton {background : #3b6978}")
        decryptButton.setStyleSheet("QPushButton {color : #cae8d5}")
        decryptButton.clicked.connect(self.decryptClicked)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(encryptButton)
        buttonsLayout.addWidget(decryptButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)

        checkLayout = QHBoxLayout()
        checkLayout.addWidget(self.checkTextButton)
        checkLayout.addWidget(self.checkResultButton)
        checkLayoutW = QWidget()
        checkLayoutW.setLayout(checkLayout)

        infoButtonsLayout = QHBoxLayout()
        infoButtonsLayout.addWidget(self.infoButton)
        infobuttonsLayoutW = QWidget()
        infobuttonsLayoutW.setLayout(infoButtonsLayout)

        #Main Layout
        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(titleText2)
        mainMenu.addWidget(self.subtitleText)
        mainMenu.addWidget(buttonsLayoutW)
        mainMenu.addWidget(checkLayoutW)
        mainMenu.addWidget(infobuttonsLayoutW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    def encryptClicked(self):
        self.encryptToBitmap()
        self.subtitleText.setText("WRITE MODE")
    
    def decryptClicked(self):
        self.decryptFromBitmap()
        self.subtitleText.setText("READ MODE")

    def checkTextClicked(self):
        info = QMessageBox()
        info.setWindowTitle("Text")
        info.setStyleSheet("QMessageBox {background-color : #cae8d5}")
        f = open("text.txt", "r", encoding="utf-8")
        data = f.read()
        info.setText(data)
        info.setFont(QFont('Courier',12))
        info.exec_()

    def checkResultClicked(self):
        info = QMessageBox()
        info.setWindowTitle("Result")
        info.setStyleSheet("QMessageBox {background-color : #cae8d5}")
        f = open("output.txt", "r", encoding="utf-8")
        data = f.read()
        info.setText(data)
        info.setFont(QFont('Courier',12))
        info.exec_()
    
    def saveClicked(self):
        f = open("result.txt", "w",encoding="utf-8")
        f.write("Encrypted text: "+self.encryptedText.text())
        f.write("\nDecrypted text: "+self.decryptedText.text())
        f.write("\nKey: "+self.genKey())
        f.close()

    def infoClicked(self):
        info = QMessageBox()
        info.setWindowTitle("Info")
        info.setStyleSheet("QMessageBox {background-color : #cae8d5}")
        f = open("info.txt", "r", encoding="utf-8")
        data = f.read()
        info.setText(data)
        info.setFont(QFont('Courier',12))
        info.exec_()
    
    def encryptToBitmap(self):
        if os.stat("text.txt").st_size*8 <= os.stat("bitmap.bmp").st_size:
            BitsArrayPic = numpy.unpackbits(numpy.fromfile("bitmap.bmp", dtype = "uint8"))
            BitsArrayText = numpy.unpackbits(numpy.fromfile("text.txt", dtype = "uint8"))
            i = 54 

            for b in BitsArrayText: 
                BitsArrayPic[i*8+7] = b 
                i = i+1 
                
            for x in range(16): 
                BitsArrayPic[i*8+7] = 1
                i = i+1

            with open("bitmap.bmp","wb") as outputfile:
                outputfile.write(numpy.packbits(BitsArrayPic))
        else:
            info = QMessageBox()
            info.setWindowTitle("Info")
            info.setStyleSheet("QMessageBox {background-color : #cae8d5}")
            info.setText("Wrong data")
            info.setFont(QFont('Courier',12))
            info.exec_()

    
    def decryptFromBitmap(self):
        picBits = numpy.unpackbits(numpy.fromfile("bitmap.bmp", dtype = "uint8"))
        i = 54 
        with open("output.txt","wb") as outputfile:
            checkEnd = []
            outputBits = []
            
            while True:
                for x in range(8): 
                    outputBits.append(picBits[i*8+7])
                    i = i+1
    
                if((outputBits == checkEnd == [1,1,1,1,1,1,1,1]) or i >= len(picBits)/8):
                    outputfile.seek(-1, os.SEEK_END)
                    outputfile.truncate()
                    break
                
                else: 
                    checkEnd = outputBits.copy()
                    outputfile.write(numpy.packbits(outputBits)) 
                    outputBits = []
                     
#MAIN
app = QApplication(sys.argv)
window = Okno()
window.setFixedSize(650,400)
window.setStyleSheet("background-color: #204051")
window.show()

app.exec_()