
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
from SoundRecorder import SoundRecorder

class ChatRoom(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.username=username
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_chat_room)
        self.ui.pushButton_2.clicked.connect(self.server_found_start)
        self.ui.listWidget.itemDoubleClicked.connect(self.enter_chat_room)
        self.dialog = QInputDialog(self)
        self.servers = []
        self.discovery = ServerDiscovery()
        self.discovery.server_found.connect(self.handle_server_found)
        #x = threading.Thread(target=self.handle_server_removed).start()

    def server_found_start(self):
        try:
            x=threading.Thread(target=self.discovery.discover_servers)
            x.start()
            x.join()
        except:
            print("what happen")

    def handle_server_found(self, servers):
        try:
            self.ui.listWidget.clear()
            for server in servers:
                name=server[0]
                ip=server[1]
                port=int(server[2])
                portt=int(server[3])
                item = QListWidgetItem(name)
                item.setData(QtCore.Qt.UserRole, (name, ip, port, portt))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.listWidget.addItem(item)
        except:
            print("what happen?")

    def handle_server_removed(self, name):
        item_to_remove = self.ui.listWidget.findItems(name, QtCore.Qt.MatchExactly)[0]
        self.ui.listWidget.takeItem(self.ui.listWidget.row(item_to_remove))

    def enter_chat_room(self, item):
        try:
            server = item.data(QtCore.Qt.UserRole)
            name=server[0]
            ip = server[1]
            port = int(server[2])
            portt=int(server[3])
            client = Client(ip, port,portt,self.username)
            client.start()
            chatbox = ChatBox(client,None,self.username)
            chatbox.remove_chatbox.connect(self.handle_server_removed)
            chatbox.show()
            #user.setTextAlignment(QtCore.Qt.AlignCenter)
        except:
            print("Server is not exist!")


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
                    info=server.getinfo()
                    name = info[0]
                    ip = info[1]
                    port = int(info[2])
                    portt = int(info[3])
                    client = Client(ip, port, portt, self.username)
                    client.start()

                    chatbox = ChatBox(client, server,self.username)
                    chatbox.remove_chatbox.connect(self.handle_server_removed)
                    chatbox.show()

                    #user.setTextAlignment(QtCore.Qt.AlignCenter)



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