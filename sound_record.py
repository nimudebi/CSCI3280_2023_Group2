# import numpy as np
import pyaudio
# import binascii
from write_wav_file import write_wav_file

def sound_record(output_file):

    # get input from microphone sampling
    #def access_sample(self):
    chunk=4*1024 # size of each audio chunk
    Format=pyaudio.paInt16
    Channel=1 # suppose I have one input channel
    sam_rate=44100 # sampling rate
    rec_sound=1 # testing
    audio_io=pyaudio.PyAudio()

    flow=audio_io.open(format=Format,channels=Channel,rate=sam_rate,input=True,output=True,frames_per_buffer=chunk)

    # print("Start recording.") # for debug
    audio=[] # audio info. is stored in a list
    for i in range(0, int(sam_rate * rec_sound / chunk)):
        data=flow.read(chunk)
        audio.append(data)
        #print(data,"\n")
        #print(type(data))
        #print(sys.getsizeof(data))
    
    #print(int(sam_rate/chunk*rec_sound))
    #print("stop reading")
    flow.stop_stream()
    flow.close()
    audio_io.terminate()

    # print(audio)
    # audio: list of 0x nums combination.
    # output_file='D:\CUHK\Y2T2\csci3280\proj\phase1\\test1.wav'
    write_wav_file(output_file, b''.join(audio), sam_rate)
# sound_record("D:\CUHK\Y2T2\csci3280\proj\phase1\\record_test1.wav")
