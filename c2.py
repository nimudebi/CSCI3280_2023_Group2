import asyncio
import websockets
import pyaudio


class Client:
    def __init__(self):
        self.target_ip = "192.168.99.142"
        self.target_port = 9808
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                          output=True, frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate,
                                            input=True, frames_per_buffer=self.chunk_size)

    async def connect_to_server(self):
        uri = f"ws://{self.target_ip}:{self.target_port}"
        async with websockets.connect(uri) as websocket:
            print("Connected to Server")
            await self.start_audio(websocket)

    async def start_audio(self, websocket):
        while True:
            receive_task = asyncio.create_task(self.receive_server_data(websocket))
            send_task = asyncio.create_task(self.send_data_to_server(websocket))
            await asyncio.gather(receive_task, send_task)
            await asyncio.sleep(0.1)

    async def receive_server_data(self, websocket):
        while True:
            try:
                data = await websocket.recv()
                print(data)
                self.playing_stream.write(data)
            except websockets.ConnectionClosed:
                break

    async def send_data_to_server(self, websocket):
        while True:
            try:
                data = self.recording_stream.read(1024)
                await websocket.send(data)
            except websockets.ConnectionClosed:
                break

    def run(self):
        asyncio.run(self.connect_to_server())


client = Client()
client.run()