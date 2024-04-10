import socket
import threading
import random
from pydub import AudioSegment
import numpy as np
import queue
from io import BytesIO

CENTRAL_SERVER_IP = "192.168.92.246"
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
        self.users=[]
        self.audio_buffer = []
        self.tmp_data=[]
        self.complete_data=[]
        self.count=0
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
        self.mix_thread = threading.Thread(target=self.get_data)


    def start(self):
        self.register_to_central_server("START")
        self.accept_thread.start()
        print("yes")
        self.mix_thread.start()

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
            bf = queue.Queue()
            self.connections.append(c)
            self.audio_buffer.append(bf)
            self.tmp_data.append(b'')
            self.complete_data.append(b'')
            threading.Thread(target=self.handle_client, args=(c, addr, self.audio_buffer[self.count])).start()

            self.count += 1

    def broadcast(self, data,c,flag=False):
        for client in self.connections:
            if flag is False:
                if client != self.s and client !=c:
                    try:
                        client.send(data)
                    except:
                        pass
            else:
                if client != self.s:
                    try:
                        client.send(data)
                    except:
                        pass

    def getinfo(self):
        return self.name, self.ip, self.port

    def handle_client(self, c, addr, q):
        while self.running:
            try:
                data = c.recv(1024)
                flag=False
                try:
                    if data.decode()[:4] == 'FUCK':
                        username=data.decode()[4:]
                        print(username)
                        self.users.append(username)
                        str="CHANGE"+",".join(self.users)
                        flag=True
                        self.broadcast(str.encode(),c,flag)
                        print(self.connections)

                    if data.decode()[:4] == 'DAMN':
                        username = data.decode()[4:]
                        self.connections.remove(c)
                        self.users.remove(username)
                        c.close()
                except:

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






'''

                x=len(data)
                y=len(self.tmp_data[i])
                if x+y<1024:
                    self.tmp_data[i]+=data
                elif x+y>1024:
                    z=x+y-1024
                    zata=data[:z]
                    rata=data[z:]
                    self.tmp_data[i]+=zata
                    self.complete_data[i]=self.tmp_data[i]
                    self.tmp_data[i]=rata
                elif x+y==1024:
                    self.tmp_data[i]+=data
                    self.complete_data[i] = self.tmp_data[i]
                    self.tmp_data[i]=b''
'''