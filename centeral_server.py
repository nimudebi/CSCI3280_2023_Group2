import socket
import signal
import sys

CENTRAL_SERVER_IP = "192.168.74.42"
CENTRAL_SERVER_PORT = 9999


class CentralServer:
    def __init__(self):
        self.server_list = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
        except OSError:
            print("Failed to bind the socket:")
            self.socket.close()
            return

    def start(self):
        self.socket.listen(100)
        print("Central server started. Listening for connections...")
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            client_socket, address = self.socket.accept()
            print("Connection established with:", address)
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        if data.startswith("START"):
            server_info = data[5:]  # Remove the "START" prefix
            self.server_list.append(server_info)
            print("Server added:", server_info)
        elif data.startswith("STOP"):
            server_info = data[4:]  # Remove the "STOP" prefix
            self.server_list.remove(server_info)
            print("Server removed:", server_info)
        self.send_server_list(client_socket)
        client_socket.close()

    def send_server_list(self, client_socket):
        server_list_string = "\n".join(self.server_list)
        client_socket.send(server_list_string.encode())

    def signal_handler(self, signal, frame):
        print("Terminating the server...")
        self.socket.close()
        sys.exit(0)

if __name__ == "__main__":
    central_server = CentralServer()
    if central_server.socket.fileno() == -1:
        # Socket binding failed, exit the program
        exit()
    central_server.start()
