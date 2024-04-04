import socket
import threading
import random


def get_private_ip():
    def get_private(item):
        return item != '127.0.0.1'

    hostname = socket.gethostname()
    a = socket.gethostbyname_ex(hostname)
    ip_address = filter(get_private, a[2])
    return list(ip_address)[0]


class Server:
    def __init__(self, room_name):
        self.ip = get_private_ip()
        self.name = room_name
        while True:
            try:
                self.port = random.randint(1024, 65535)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        self.running = True
        self.accept_thread = threading.Thread(target=self.accept_connections)

    def start(self):
        self.accept_thread.start()

    def stop(self):
        self.running = False
        self.s.close()
        for connection in self.connections:
            connection.close()

    def accept_connections(self):
        self.s.listen(100)

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()
            self.connections.append(c)
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data.encode())
                except:
                    pass

    def getinfo(self):
        return self.name, self.ip, self.port

    def handle_client(self, c, addr):
        while self.running:
            try:
                data = c.recv(1024)
                # print(data)
                self.broadcast(c, data)

            except socket.error:
                c.close()


if __name__ == "__main__":
    server = Server("niubi")
    server.start()