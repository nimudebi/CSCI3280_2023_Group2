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
        self.audio_buffer = []
        self.tmp_data=[]
        self.users = []
        self.complete_data=[]
        self.count=0
        while True:
            try:
                self.port = random.randint(10000, 10100)
                self.sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sv.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")
                break
        while True:
            try:
                self.portt = random.randint(10200, 10300)
                self.st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.st.bind((self.ip, self.portt))
                break
            except:
                print("Couldn't bind to that port")
                break

        self.connections = []
        self.txt_connections=[]
        self.running = True
        self.accept_thread = threading.Thread(target=self.accept_connections)


    def start(self):
        self.register_to_central_server("START")
        self.accept_thread.start()
        print("yes")


    def stop(self):
        self.register_to_central_server("STOP")
        self.running = False
        self.sv.close()
        self.st.close()
        for connection in self.connections:
            connection.close()
        for connection in self.txt_connections:
            connection.close()

    def accept_connections(self):
        self.sv.listen(100)
        self.st.listen(100)
        print('Running on IP: ' + self.ip)
        print('Voice Stream Running on port: ' + str(self.port))
        print('Text Stream Running on port: ' + str(self.portt))

        while self.running:
            #try:
            c, addr = self.sv.accept()
            ct,addr = self.st.accept()
            bf = queue.Queue()
            self.connections.append(c)
            self.txt_connections.append(ct)
            self.audio_buffer.append(bf)
            self.tmp_data.append(b'')
            self.complete_data.append(b'')
            threading.Thread(target=self.handle_client, args=(c, addr, self.audio_buffer[self.count])).start()
            threading.Thread(target=self.text_interact, args=(ct, addr,)).start()
            self.count += 1
            #except:
            #    print("what happen?")

    def broadcast(self, data,c,flag=False):
        if flag is False:
            for client in self.connections:
                if client != self.sv and client != c:
                    try:
                        client.send(data)
                    except:
                        pass
        else:
            for client in self.txt_connections:
                if client != self.st:
                    try:
                        client.send(data)
                    except:
                        pass

    def getinfo(self):
        return self.name, self.ip, self.port,self.portt

    def text_interact(self, c, addr):
        while self.running:
            try:
                data = c.recv(1024)
                flag=True
                print("yes")
                if data.decode()[:4] == 'FUCK':
                    username=data.decode()[4:]
                    self.users.append(username)
                    str="CHANGE"+",".join(self.users)
                    self.broadcast(str.encode(),c,flag)

                elif data.decode()[:4] == 'DAMN':
                    username = data.decode()[4:]
                    self.users.remove(username)
                    str = "CHANGE" + ",".join(self.users)
                    print(self.users)
                    self.broadcast(str.encode(), c, flag)
                    self.connections.remove(c)
                    self.txt_connections.remove(c)

                    c.close()

                elif data[:7].decode()=="CAONIMA":
                    self.broadcast(data,c,False)

                else:
                    str = data.decode()
                    self.broadcast(str.encode(), c, flag)

            except:
                c.close()

    def handle_client(self, c, addr, q):
        while self.running:
            try:
                data = c.recv(1024)
                self.broadcast(data, c)
            except:
                c.close()


    def register_to_central_server(self, action):
        central_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            central_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
            message = f"{action}{self.name},{self.ip},{self.port},{self.portt}"
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
