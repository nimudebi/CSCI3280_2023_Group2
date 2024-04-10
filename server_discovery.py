import socket
from PyQt5.QtCore import QTimer, QUrl, Qt,QObject, pyqtSignal, pyqtSlot
import time
import socket

CENTRAL_SERVER_IP = "192.168.92.246"
CENTRAL_SERVER_PORT = 9999


class ServerDiscovery(QObject):
    server_found = pyqtSignal(list)

    def discover_servers(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
            client_socket.send("DISCOVER".encode())
            server_list = client_socket.recv(1024).decode().split("\n")
            for i in range(len(server_list)):
                server_list[i] = server_list[i].split(',')
        except TimeoutError:
            print("Time out")
        except OSError:
            print("Network error")
        except:
            print("fail")
        finally:
            client_socket.close()

        try:
            if len(server_list[0]) == 4:
                self.server_found.emit(server_list)
        except:
            pass
