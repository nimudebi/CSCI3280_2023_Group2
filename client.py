import socket
import threading
import pyaudio
import numpy as np
import librosa
import time
import ChatBox

class Client:
    users=[]
    def __init__(self, ip, portv,portt,username):
        self.sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running=True
        self.username=username
        self.message_received = ""

        while 1:
            try:
                self.target_ip = ip
                self.v_port = portv
                self.t_port = portt
                self.sv.connect((self.target_ip, self.v_port))
                self.st.connect((self.target_ip, self.t_port))
                print("Connected to Server")
                break
            except:
                print("Couldn't connect to server")
                break

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        self.rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=self.rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=self.rate, input=True,
                                            frames_per_buffer=chunk_size)

        self.text_receive_thread = threading.Thread(target=self.receive_server_text)
        self.voice_receive_thread = threading.Thread(target=self.receive_server_voice)
        self.voice_send_thread = threading.Thread(target=self.send_voice_to_server)

    def start(self):
        data = b'FUCK' + self.username.encode()
        self.st.send(data)
        self.voice_send_thread.start()
        self.text_receive_thread.start()
        self.voice_receive_thread.start()

    def stop(self):
        data = b'DAMN'+self.username.encode()
        self.st.send(data)
        self.running = False
        self.sv.close()
        self.st.close()


    def send_text_to_server(self,message):
        try:
            data = message.encode()
            self.st.send(data)
        except:
            pass

    def receive_server_voice(self):
        while self.running:
            try:
                data = self.sv.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_voice_to_server(self):
        while self.running:
            try:
                data = self.recording_stream.read(1024)

                if ChatBox.mute_status:
                    continue
                
                if ChatBox.boy_status:
                    nparray = np.frombuffer(data, dtype=np.int16)
                    float_array = nparray.astype(np.float32) / np.iinfo(np.int16).max  # 将音频数据转换为浮点格式
                    pitch_shifted = librosa.effects.pitch_shift(float_array, sr=self.rate, n_steps=-5)
                    normalized_shifted = np.int16(pitch_shifted * np.iinfo(np.int16).max)  # 将音频数据转换回整数格式
                    data = normalized_shifted.tobytes()

                if ChatBox.girl_status:
                    nparray = np.frombuffer(data, dtype=np.int16)
                    float_array = nparray.astype(np.float32) / np.iinfo(np.int16).max  # 将音频数据转换为浮点格式
                    pitch_shifted = librosa.effects.pitch_shift(float_array, sr=self.rate, n_steps=5)
                    normalized_shifted = np.int16(pitch_shifted * np.iinfo(np.int16).max)  # 将音频数据转换回整数格式
                    data = normalized_shifted.tobytes()

                if ChatBox.funny_status:
                    nparray = np.frombuffer(data, dtype=np.int16)
                    float_array = nparray.astype(np.float32) / np.iinfo(np.int16).max  # 将音频数据转换为浮点格式
                    pitch_shifted = librosa.effects.pitch_shift(float_array, sr=self.rate, n_steps=20)
                    normalized_shifted = np.int16(pitch_shifted * np.iinfo(np.int16).max)  # 将音频数据转换回整数格式
                    data = normalized_shifted.tobytes()

                self.sv.sendall(data)
            except:
                pass

    def receive_server_text(self):
        while self.running:
            try:
                data = self.st.recv(1024)
                if data.decode()[:6]=="CHANGE":
                    Client.users=data.decode()[6:].split(",")
                    print(Client.users)
                else:
                    message = data.decode()
                    self.message_received = message
            except:
                pass




if __name__ == "__main__":
    ip = "192.168.99.142"
    port = 10089
    portt= 10290

    client = Client(ip, port,portt,"yes12")
    client.start()
    
