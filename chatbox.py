import sys
import os
import socket
import threading
import time
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer, QUrl, Qt,QObject, pyqtSignal, pyqtSlot
from chatboxUI import *
from server_discovery import ServerDiscovery
import pyaudio

boy_status = False
girl_status = False
mute_status = False
close_voice_status = False

class ChatBox(QMainWindow):
    remove_chatbox = pyqtSignal(str)
    #global boy_status, girl_status
    #boy_status = False
    #girl_status = False

    def __init__(self,client,server):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client=client
        self.server=server

    # add close_voice function
        self.ui.pushButton.clicked.connect(self.close_voice)

        # add muting function
        self.ui.pushButton_3.clicked.connect(self.muting)

        # add voice change menu
        self.menu = QMenu()
        self.option1 = QAction("girl")
        self.option1.triggered.connect(self.girl)
        self.menu.addAction(self.option1)
        self.option2 = QAction("boy")
        self.option2.triggered.connect(self.boy)
        self.menu.addAction(self.option2)
        self.option3 = QAction("horror")
        self.option3.triggered.connect(self.horror)
        self.menu.addAction(self.option3)
        self.option4 = QAction("echo")
        self.option4.triggered.connect(self.echo)
        self.menu.addAction(self.option4)
        self.option5 = QAction("none")
        self.option5.triggered.connect(self.none)
        self.menu.addAction(self.option5)
        self.ui.toolButton.setMenu(self.menu)
        self.ui.toolButton.setPopupMode(QToolButton.InstantPopup)
        #self.boy_status = False
        #self.girl_status = False
        #self.mute = False
        #self.close_audio = False

    def close_voice(self):
        global close_voice_status
        if close_voice_status:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-high-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-xmark-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon)
        close_voice_status = not close_voice_status
        #self.close_audio = not self.close_audio
        #self.client.receive_server_data(self.close_audio)
        

    def muting(self):
        global mute_status
        if mute_status:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/microphone-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/microphone-slash-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        mute_status = not mute_status
        '''
        if self.mute:
            self.client.p.terminate()
        else:
            self.client.p=pyaudio.PyAudio()
        '''
    '''
    def boy_open():
        global boy_status
        boy_status = True
        return boy_status
    def girl_open():
        global girl_status
        girl_status = True
        return girl_status
    '''
    def boy(self):
        global boy_status
        global girl_status
        boy_status = True
        girl_status = False

    def girl(self):
        global boy_status
        global girl_status
        boy_status = False
        girl_status = True
        #print("Successfully changed to girl")

    '''
    def boy(self):
        self.client.send_data_to_server(True,False,False)

    def girl(self):
        self.client.send_data_to_server(False,True,False)
    '''
    
    def none(self):
        global boy_status
        global girl_status
        boy_status = False
        girl_status = False
        #self.client.send_data_to_server(False,False,False)
    def horror(self):
        pass

    def echo(self):
        pass
    

    def closeEvent(self, event):
        try:
            if self.server:
                self.server.stop()
                self.remove_chatbox.emit(self.server.getinfo()[0])
            if self.client:
                self.client.stop()
        except:
            event.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ip = "192.168."
    port = 10209
    #client = Client(ip, port, "yes")
    chat_app = ChatBox(None,None)
    chat_app.show()
    sys.exit(app.exec_())
