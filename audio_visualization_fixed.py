import matplotlib.pyplot as plt
import numpy as np
import wave

def audio_visualization_fixed(audio_file):
    # open wav file
    wav=wave.open(audio_file,'r')
    # get audio properties
    sample_width = wav.getsampwidth()
    sample_rate = wav.getframerate()
    num_frames = wav.getnframes()
    duration = num_frames / sample_rate
    # Read audio frames
    frames = wav.readframes(num_frames)
    # read audio data
    signal=np.frombuffer(frames,dtype=np.int16)
    # generate time axis
    time=np.linspace(0,duration,num=len(signal))
    # plot the audio waveform
    plt.figure(figsize=(10,4))
    plt.plot(time,signal,color='black')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio Waveform')
    plt.grid(True)
    plt.show()

# audio_visualization_fixed("D:\CUHK\Y2T2\csci3280\proj\phase1\CantinaBand3.wav")