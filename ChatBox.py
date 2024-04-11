import sys
import os
import socket
import threading
import time
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer, QUrl, Qt
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QUrl, Qt, QObject, pyqtSignal, pyqtSlot
from chatboxUI import *
from server_discovery import ServerDiscovery
import pyaudio

from karaoke import Karaoke
from phaseIIRecorder import PhaseIIRecorderUI

boy_status = False
girl_status = False
mute_status = False
close_voice_status = False
funny_status = False


class ChatBox(QMainWindow):
    remove_chatbox = pyqtSignal(str)

    def __init__(self, client, server, username):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.username = username
        self.ui.setupUi(self)
        self.msg = ""
        self.my_message = ''
        self.recorder = PhaseIIRecorderUI()
        global boy_status, girl_status, mute_status, close_voice_status, funny_status
        boy_status = girl_status = mute_status = close_voice_status = funny_status = False
        self.client = client
        self.server = server
        self.karaoke = None
        self.user = []
        threading.Thread(target=self.get_online_users).start()
        threading.Thread(target=self.update_text_message).start()
        # add close_voice function
        self.ui.pushButton.clicked.connect(self.close_voice)
        # send txt
        self.ui.pushButton_2.clicked.connect(self.send_txt)
        # sound recorder
        self.ui.pushButton_6.clicked.connect(self.recording)
        # add muting function
        self.ui.pushButton_3.clicked.connect(self.muting)
        # karaoke
        self.ui.pushButton_5.clicked.connect(self.kok)

        # add voice change menu
        self.menu = QMenu()
        self.option1 = QAction("girl")
        self.option1.triggered.connect(self.girl)
        self.menu.addAction(self.option1)
        self.option2 = QAction("boy")
        self.option2.triggered.connect(self.boy)
        self.menu.addAction(self.option2)
        self.option3 = QAction("funny")
        self.option3.triggered.connect(self.funny)
        self.menu.addAction(self.option3)
        self.option4 = QAction("none")
        self.option4.triggered.connect(self.none)
        self.menu.addAction(self.option4)
        self.ui.toolButton.setMenu(self.menu)
        self.ui.toolButton.setPopupMode(QToolButton.InstantPopup)

    def kok(self):
        self.karaoke = Karaoke()
        self.karaoke.show()

    def send_txt(self):
        self.msg = self.ui.textEdit_2.toPlainText()
        self.ui.textEdit_2.clear()
        print("3")
        if self.msg:
            print("4")
            self.msg = self.username + ": " + self.msg
            print(self.msg)
            self.client.send_text_to_server(self.msg)
            self.msg = ''
        else:
            print("you stupid guy send an empty message.")

    def update_text_message(self):
        while True:
            if self.my_message == self.client.message_received:
                continue
            else:
                self.my_message = self.client.message_received
                self.ui.textEdit.append(self.client.message_received)

    def recording(self):
        self.recorder.show()

    def close_voice(self):
        global close_voice_status
        if close_voice_status:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-high-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-xmark-solid-white.svg"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon)
        close_voice_status = not close_voice_status
        # self.close_audio = not self.close_audio
        # self.client.receive_server_data(self.close_audio)

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
        funny_status = False

    def girl(self):
        global boy_status
        global girl_status
        boy_status = False
        girl_status = True
        funny_status = False
        # print("Successfully changed to girl")

    def funny(self):
        global funny_status
        funny_status = True
        boy_status = False
        girl_status = False

    '''
    def boy(self):
        self.client.send_data_to_server(True,False,False)

    def girl(self):
        self.client.send_data_to_server(False,True,False)
    '''

    def none(self):
        global boy_status
        global girl_status
        global funny_status
        boy_status = False
        girl_status = False
        funny_status = False

    def get_online_users(self):
        while True:
            online = self.client.users
            if online == self.user:
                continue
            else:
                self.user = online
                self.ui.listWidget.clear()
                self.ui.listWidget.addItems(self.user)

    def closeEvent(self, event):
        try:
            if self.client:
                self.client.stop()
            if self.server:
                self.remove_chatbox.emit(self.server.getinfo()[0])
                self.server.stop()
        except:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ip = "192.168.92.246"
    port = 10286
    # client = Client(ip, port, "yes")
    chat_app = ChatBox(None, None, "self.username")
    chat_app.show()
    sys.exit(app.exec_())