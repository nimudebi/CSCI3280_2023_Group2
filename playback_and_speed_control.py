import pyaudio
import wave

def speed_control(input_wav_file,  speed):
    with open(input_wav_file, 'rb') as input_file:
        header = input_file.read(44)
        data = input_file.read()
        chunk_size = int.from_bytes(header[4:8], byteorder='little')
        sample_rate = int.from_bytes(header[24:28], byteorder='little')
        # byte_rate = int.from_bytes(header[28:30], byteorder='little')

        # Modify header for new frame rate
        if speed != 1:
            new_chunk_size = int(chunk_size * speed)
            new_sample_rate = int(sample_rate * speed)
            # new_byte_rate = byte_rate * speed
            new_header = bytearray(header)
            new_header[4:8] = new_chunk_size.to_bytes(4, byteorder='little')
            new_header[24:28] = new_sample_rate.to_bytes(4, byteorder='little')
            # new_header[28:30] = new_byte_rate.to_bytes(2, byteorder='little')
        elif speed == 1:
            new_header = header
        with open('output_wav_file.wav', 'wb') as output_file:
            output_file.write(new_header)
            output_file.write(data)

def playback(wave_path,speed):
    """
    This funtion is a function to play
    :param wava_path:   The target audio file
    :param speed:       the speed users want
    """
    chunk = 1024

    speed_control(wave_path,speed)
    wf = wave.open('output_wav_file.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()