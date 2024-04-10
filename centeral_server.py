'''
import asyncio
import signal
import websockets

CENTRAL_SERVER_IP = "192.168.99.142"
CENTRAL_SERVER_PORT = 9999


class CentralServer:
    def __init__(self):
        self.server_list = set()
        self.server = None
        self.is_closing = False

    async def start(self, websocket, path):
        print("Connection established with:", websocket.remote_address)
        try:
            async for message in websocket:
                if message.startswith("START"):
                    server_info = message[5:]  # Remove the "START" prefix
                    self.server_list.add(server_info)
                    print("Server added:", server_info)
                elif message.startswith("STOP"):
                    server_info = message[4:]  # Remove the "STOP" prefix
                    self.server_list.remove(server_info)
                    print("Server removed:", server_info)
                await self.send_server_list(websocket)
        except websockets.ConnectionClosed:
            print("Connection closed:", websocket.remote_address)
            self.server_list.discard(websocket)
            await self.send_server_list(websocket)

    async def send_server_list(self, websocket):
        server_list_string = "\n".join(self.server_list)
        await websocket.send(server_list_string)

    def run(self):
        start_server = websockets.serve(self.start, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)
        self.server = asyncio.get_event_loop().run_until_complete(start_server)
        print("Central server started. Listening for connections...")

        if hasattr(signal, "SIGINT"):
            # Register signal handler for SIGINT (Ctrl+C)
            signal.signal(signal.SIGINT, self.signal_handler)

        try:
            asyncio.get_event_loop().run_forever()
        finally:
            self.shutdown()

    def signal_handler(self, sig, frame):
        print("Received signal to shutdown")
        self.is_closing = True

    def shutdown(self):
        if self.is_closing:
            print("Shutting down...")
            if self.server:
                self.server.close()
                asyncio.get_event_loop().run_until_complete(self.server.wait_closed())
            asyncio.get_event_loop().stop()


if __name__ == "__main__":
    central_server = CentralServer()
    central_server.run()

'''''
import socket

CENTRAL_SERVER_IP = "192.168.92.246"
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
            try:
                self.server_list.remove(server_info)
                print("Server removed:", server_info)
            except:
                print("what happen?")
        self.send_server_list(client_socket)
        client_socket.close()

    def send_server_list(self, client_socket):
        server_list_string = "\n".join(self.server_list)
        client_socket.send(server_list_string.encode())


if __name__ == "__main__":
    central_server = CentralServer()
    if central_server.socket.fileno() == -1:
        # Socket binding failed, exit the program
        exit()
    central_server.start()
