import socket
import threading
from PyQt5.QtCore import QTimer, QUrl, Qt,QObject, pyqtSignal, pyqtSlot
import time

class ServerDiscovery(QObject):
    server_found = pyqtSignal(str, str, int)

    def discover_servers(self):
        broadcast_address = '<broadcast>'  # 广播地址
        port = 9999

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', port))

        sock.sendto('DISCOVER'.encode(), (broadcast_address, port))

        responses = []
        start_time = time.time()

        while time.time() - start_time < 5:  # 设置超时时间为5秒
            try:
                data, addr = sock.recvfrom(1024)
                responses.append((data.decode(), addr))
            except socket.timeout:
                break

        print(responses)
        for response in responses:
            name, ip, port = response[0].split(',')
            self.server_found.emit(name, ip, int(port))

        sock.close()