# import numpy as np
import pyaudio
# import binascii
from write_wav_file import write_wav_file


def sound_record():
    # get input from microphone sampling
    CHUNK = 4 * 1024  # size of each audio chunk
    FORMAT = pyaudio.paInt16
    CHANNEL = 1  # suppose I have one input channel
    SAM_RATE = 44100  # sampling rate
    rec_sound = 1  # testing
    audio_io = pyaudio.PyAudio()

    flow = audio_io.open(format=Format, channels=Channel, rate=sam_rate, input=True, output=True,
                         frames_per_buffer=chunk)

    audio = []  # audio info. is stored in a list
    for i in range(0, int(sam_rate * rec_sound / chunk)):
        data = flow.read(chunk)
        audio.append(data)


    flow.stop_stream()
    flow.close()
    audio_io.terminate()

    write_wav_file(output_file, b''.join(audio), sam_rate)
