
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
from roomlistUI import *
from server_discovery import ServerDiscovery
from server import Server
from client import Client
from ChatBox import ChatBox

class ChatRoom(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.username=username
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_chat_room)
        #self.ui.pushButton_2.clicked.connect(self.server_found_start)
        self.ui.listWidget.itemDoubleClicked.connect(self.enter_chat_room)
        self.dialog = QInputDialog(self)
        self.servers = []
        self.discovery = ServerDiscovery()
        #self.discovery.server_found.connect(self.handle_server_found)

    def server_found_start(self):
        threading.Thread(target=self.discovery.discover_servers).start()

    def handle_server_found(self, name, ip, port):
        existing_items = self.ui.listWidget.findItems(name, QtCore.Qt.MatchExactly)
        if existing_items:
            return

        server = Server(name)
        self.servers.append(server)
        server.start()
        item = QListWidgetItem(name)
        item.setData(QtCore.Qt.UserRole, (name, ip, port))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.listWidget.addItem(item)
    def enter_chat_room(self, item):
        server = item.data(QtCore.Qt.UserRole)
        name=server[0]
        ip = server[1]
        port = server[2]
        client = Client(ip, port,self.username)
        client.start()
        self.chatbox = ChatBox(client,None)
        self.chatbox.show()

        user = QListWidgetItem(self.username)
        user.setData(QtCore.Qt.UserRole, self.username)
        user.setTextAlignment(QtCore.Qt.AlignCenter)
        self.chatbox.ui.listWidget.addItem(user)


    def add_chat_room(self):
        self.dialog.setInputMode(QInputDialog.TextInput)
        self.dialog.setObjectName("dialog")
        self.dialog.setWindowTitle("Add a chat room")
        self.dialog.setLabelText("Please enter the name of your chat room:")
        self.dialog.setTextValue("")
        self.dialog.resize(400, 1000)
        flags = self.dialog.windowFlags()
        self.dialog.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)
        self.dialog.setStyleSheet("""
                    #dialog{
                        background-color:rgba(224, 254, 255,0);
                        background-image: url(./designer/2.png);
                    } 
                    QPushButton{
                        background-color: rgba(215, 255, 210,20);
                        border-radius: 12px;
                        font: 20px "Century Schoolbook";
                        color: white;
                    }
                """)

        if self.dialog.exec_() == QInputDialog.Accepted:
            room_name = self.dialog.textValue()
            if room_name:
                existing_items = self.ui.listWidget.findItems(room_name, QtCore.Qt.MatchExactly)
                if existing_items:
                    QMessageBox.information(self, "Duplicate Chat Room",
                                            "The chat room already exists. Please enter a different name.")
                else:
                    server = Server(room_name)
                    self.servers.append(server)
                    server.start()
                    item = QListWidgetItem(room_name)
                    item.setData(QtCore.Qt.UserRole, server.getinfo())
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.listWidget.addItem(item)
                    self.chatbox = ChatBox(None, server)
                    self.chatbox.show()
                    user = QListWidgetItem(self.username)
                    user.setData(QtCore.Qt.UserRole, self.username)
                    user.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.chatbox.ui.listWidget.addItem(user)


    # 似乎有个bug，关闭的时候会提示OSError: [WinError 10038] 在一个非套接字上尝试了一个操作。不过目前还没啥影响
    def closeEvent(self, event):
        for server in self.servers:
            server.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatRoom("yes")
    chat_app.show()
    sys.exit(app.exec_())
