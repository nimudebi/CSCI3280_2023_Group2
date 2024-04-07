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
from server import Server
from client import Client




class ChatBox(QMainWindow):
    remove_chatbox = pyqtSignal(str)

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
        self.boy_open = False
        self.girl_open = False
        self.mute = False
        self.close_audio = False

    def close_voice(self):
        self.close_audio = not self.close_audio
        # self.close_audio = True

    def muting(self):
        self.mute = not self.mute
        # self.mute = True

    def boy(self):
        self.girl_open = False
        self.boy_open = True

    def girl(self):
        self.boy_open = False
        self.girl_open = True

    def none(self):
        self.boy_open = False
        self.girl_open = False

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
    chat_app = ChatBox(None,None)
    chat_app.show()
    sys.exit(app.exec_())
