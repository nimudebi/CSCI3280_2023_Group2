import socket
import threading
import random

CENTRAL_SERVER_IP = "192.168.74.42"
CENTRAL_SERVER_PORT = 9999


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
                self.port = random.randint(10000, 11000)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        self.running = True
        self.accept_thread = threading.Thread(target=self.accept_connections)

    def start(self):
        self.register_to_central_server("START")
        self.accept_thread.start()

    def stop(self):
        self.register_to_central_server("STOP")
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

    def broadcast(self, data):
        for client in self.connections:
            if client != self.s:
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
                self.broadcast(c, data)
            except:
                c.close()

    def register_to_central_server(self, action):
        central_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            central_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
            message = f"{action}{self.name},{self.ip},{self.port}"
            central_socket.send(message.encode())
            server_list = central_socket.recv(1024).decode()
            # print("Server list received from central server:")
            # print(server_list)
        except:
            print("Failed to connect to the central server.")
        central_socket.close()

if __name__ == "__main__":
    server = Server("niubi")
    server.start()