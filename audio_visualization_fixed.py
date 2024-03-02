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
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, signal, color='black')
    ax.set(xlabel='Time (s)', ylabel='Amplitude', title='Audio Waveform')
    ax.grid(True)

    # Convert the plot to an image
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image
