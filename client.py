import socket
import threading
import pyaudio


class Client:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running=True

        while 1:
            try:
                self.target_ip = ip
                self.target_port = port
                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        self.receive_thread = threading.Thread(target=self.receive_server_data)
        self.send_thread = threading.Thread(target=self.send_data_to_server)

    def start(self):
        self.receive_thread.start()
        self.send_thread.start()

    def stop(self):
        self.running = False
        self.s.close()


    def receive_server_data(self):
        while self.running:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while self.running:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass


if __name__ == "__main__":
    ip = "42.200.120.73"
    port = 43042
    client = Client(ip, port)
    client.start()