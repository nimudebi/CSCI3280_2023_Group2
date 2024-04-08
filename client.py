import socket
import threading
import pyaudio
import numpy as np
import librosa
import chatbox

class Client:
    def __init__(self, ip, port,username):
        self.username = username
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running=True
        self.username=username
        # self.chatbox = ChatBox(None, None)

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
        self.rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=self.rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=self.rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        self.receive_thread = threading.Thread(target=self.receive_server_data)
        self.send_thread = threading.Thread(target=self.send_data_to_server)

    def start(self):
        self.receive_thread.start()
        self.send_thread.start()
        data = b'FUCK'+self.username.encode()
        self.s.send(data)



    def stop(self):
        self.running = False
        data = b'DAMN'+self.username.encode()
        self.s.send(data)
        self.s.close()

    def receive_server_data(self):
        while self.running:
            try:
                if chatbox.close_voice_status:
                    print("close_voice_status:", chatbox.close_voice_status)
                else:
                    data = self.s.recv(1024)
                    self.playing_stream.write(data)
                    print(data)
            except:
                pass

    def send_data_to_server(self):
        while self.running:
            try:
                data = self.recording_stream.read(1024)
                #print(girl_status)
                #print(boy_status)
                if chatbox.boy_status:
                    nparray = np.frombuffer(data, dtype=np.int16)
                    float_array = nparray.astype(np.float32) / np.iinfo(np.int16).max  # 将音频数据转换为浮点格式
                    print("boy_status:", chatbox.boy_status)
                    print("successfully change to boy")
                    #pitch_shifted = librosa.effects.pitch_shift(nparray, sr=self.rate, n_steps= -5)
                    pitch_shifted = librosa.effects.pitch_shift(float_array, sr=self.rate, n_steps=-5)
                    normalized_shifted = np.int16(pitch_shifted * np.iinfo(np.int16).max)  # 将音频数据转换回整数格式
                    data = normalized_shifted.tobytes()
                    #data = pitch_shifted.astype(np.int16).tobytes()
                    print("Finally successfully changed to boy")

                if chatbox.girl_status:
                    nparray = np.frombuffer(data, dtype=np.int16)
                    float_array = nparray.astype(np.float32) / np.iinfo(np.int16).max  # 将音频数据转换为浮点格式
                    print("girl_status:", chatbox.girl_status)
                    print("successfully change to girl")
                    pitch_shifted = librosa.effects.pitch_shift(float_array, sr=self.rate, n_steps=5)
                    #pitch_shifted = librosa.effects.pitch_shift(nparray, sr=self.rate, n_steps= 5)
                    print("successfully shifted pitch")
                    normalized_shifted = np.int16(pitch_shifted * np.iinfo(np.int16).max)  # 将音频数据转换回整数格式
                    data = normalized_shifted.tobytes()
                    #data = pitch_shifted.astype(np.int16).tobytes()
                    print("Finally successfully changed to girl")

                if chatbox.mute_status:
                    print("mute_status:", chatbox.mute_status)
                    print("Successfully mute.")
                    continue
                else:
                    print("mute_status", chatbox.mute_status)
                    print("You unmuted.")

                self.s.sendall(data)
            except:
                pass


if __name__ == "__main__":
    ip = "192.168.92.246"
    port = 10514
    client = Client(ip, port,"yes")
    client.start()
