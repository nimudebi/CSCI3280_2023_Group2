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
        if self.close_audio:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-high-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/volume-xmark-solid-white.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        self.close_audio = not self.close_audio
        self.client.receive_server_data(self.close_audio)

    def muting(self):
        if self.mute:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/microphone-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/microphone-slash-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon)
        self.mute = not self.mute
        self.client.send_data_to_server(False,False,self.mute)

    def boy(self):
        self.client.send_data_to_server(True,False,False)

    def girl(self):
        self.client.send_data_to_server(False,True,False)


    def none(self):
        self.client.send_data_to_server(False,False,False)
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
