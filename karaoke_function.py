import os
import pyaudio
import wave
import numpy as np
import sounddevice as sd
import threading
import time

def karaoke_bgm(input_file):
    """
    :param input_num: if -1, users want to input their own bgm. Else, it means the num of bgm the users chose
    :param input_file: if users want input their own bgm, the input_file is the position the input file. Else it will be None
    :param bgm_dic: the file used to store the bgm this function generates
    :return: the position of the karaoke bgm
    """
    # Install configuration file
    # warning = "If you want to use karaoke function, please ensure that you have anaconda or miniconda on you PC"
    # print(warning)
    # os.system('conda install -c conda-forge ffmpeg libsndfile')
    #
    cmd = 'python -m spleeter separate -p spleeter:2stems -o karaoke_bgm ' + input_file
    os.system(cmd)
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    bgm_file = os.path.abspath('karaoke_bgm') + '\\'+file_name + '\\accompaniment.wav'
    return bgm_file


def record_microphone_and_system_audio(output_file, duration):
    def callback(indata, outdata, frames, time, status):
        outdata[:] = indata

    fs = 44100
    channels = 2

    with sd.OutputStream(callback=callback, dtype='int16', channels=channels, samplerate=fs):
        print("Karaoke started...")
        time.sleep(duration)
        print("Karaoke stopped...")



def karaoke(input_file, bgm_dic = 'karaoke_bgm'):
    accompaniment = karaoke_bgm(input_file, bgm_dic)
    output_file = "output.wav"
    recording_duration = 10  # in seconds

    # Start playing background music in a separate thread
    music_thread = threading.Thread(target=play_audio, args=(accompaniment,))
    music_thread.start()

    # Record microphone and system audio in a separate thread
    record_thread = threading.Thread(target=record_microphone_and_system_audio, args=(output_file, recording_duration))
    record_thread.start()

    # Wait for background music thread to finish
    music_thread.join()

    # Wait for record thread to finish
    record_thread.join()


