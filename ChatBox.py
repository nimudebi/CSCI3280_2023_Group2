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