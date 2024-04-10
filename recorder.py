import os
import pyaudio
import threading
import wave
import time
from datetime import datetime
from pydub import AudioSegment


class Recorder():
    def __init__(self, chunk=1024, channels=2, rate=44100):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def findInternalRecordingDevice(self, p, target):

        for i in range(p.get_device_count()):
            devInfo = p.get_device_info_by_index(i)
            if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
                return i
        print('无法找到内录设备!')
        return -1

    def start(self):
        self._running = True
        threading.Thread(target=self.__record).start()

    def __record(self):
        self._running = True
        self._frames = []

        p = pyaudio.PyAudio()
        dev_idx_sys = self.findInternalRecordingDevice(p, '立体声混音')
        if dev_idx_sys < 0:
            return
        sys_stream = p.open(input_device_index=dev_idx_sys,
                        format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        dev_idx_mic = self.findInternalRecordingDevice(p, '麦克风阵列')
        if dev_idx_mic < 0:
            return
        mic_stream = p.open(input_device_index=dev_idx_mic,
                            format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        while self._running:
            data_sys = sys_stream.read(self.CHUNK)
            data_mic = mic_stream.read(self.CHUNK)

            audio_sys = AudioSegment(data=data_sys, sample_width=2, frame_rate=self.RATE, channels=self.CHANNELS)
            audio_mic = AudioSegment(data=data_mic, sample_width=2, frame_rate=self.RATE, channels=self.CHANNELS)

            min_len = min(len(audio_sys), len(audio_mic))
            audio_sys = audio_sys[:min_len]
            audio_mic = audio_mic[:min_len]

            overlapped_audio = audio_sys.overlay(audio_mic)

            overlapped_data = overlapped_audio.raw_data

            self._frames.append(overlapped_data)

        sys_stream.stop_stream()
        mic_stream.stop_stream()

        sys_stream.close()
        mic_stream.close()
        # 结束pyaudio
        p.terminate()
        return


    def stop(self):
        self._running = False

    # 保存到文件
    def save(self, fileName):
        # 创建pyAudio对象
        p = pyaudio.PyAudio()
        # 打开用于保存数据的文件
        wf = wave.open(fileName, 'wb')
        # 设置音频参数
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        # 写入数据
        wf.writeframes(b''.join(self._frames))
        # 关闭文件
        wf.close()
        # 结束pyaudio
        p.terminate()


if __name__ == "__main__":

    if not os.path.exists('record'):
        os.makedirs('record')

    print("\npython 录音机 ....\n")
    print("提示：按 r 键并回车 开始录音\n")

    i = input('请输入操作码:')
    if i == 'r':
        rec = Recorder()
        begin = time.time()

        print("\n开始录音,按 s 键并回车 停止录音，自动保存到 record 子目录\n")
        print('start')
        rec.start()
        print('dllm')

        running = True
        while running:
            i = input("请输入操作码:")
            if i == 's':
                running = False
                print("录音已停止")
                rec.stop()
                t = time.time() - begin
                print('录音时间为%ds' % t)
                rec.save("record/rec_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav")