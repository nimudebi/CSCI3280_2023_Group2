def write_wav_file(filename,audio_data,sample_rate=44100):
    # WAV file header constants
    chunk_id = b"RIFF"
    format_type = b"WAVE"
    subchunk1_id = b"fmt "
    subchunk1_size = 16  # Size of the fmt chunk (16 bytes for PCM)
    audio_format = 1  # PCM format
    num_channels = 1  # Mono audio
    bits_per_sample = 16  # 16 bits per sample
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    subchunk2_id = b"data"

    # Calculate the data size
    data_size = len(audio_data)
    # Total file size excluding the first 8 bytes (RIFF chunk_id and file size)
    chunk_size = 36 + data_size

    with open(filename, "wb") as wav_file:
        # Write the WAV file header                             # byte_number
        wav_file.write(chunk_id)                                # 0
        wav_file.write(chunk_size.to_bytes(4, "little"))        # 4
        wav_file.write(format_type)                             # 8
        wav_file.write(subchunk1_id)                            # 12
        wav_file.write(subchunk1_size.to_bytes(4, "little"))    # 16
        wav_file.write(audio_format.to_bytes(2, "little"))      # 20
        wav_file.write(num_channels.to_bytes(2, "little"))      # 22
        wav_file.write(sample_rate.to_bytes(4, "little"))       # 24
        wav_file.write(byte_rate.to_bytes(4, "little"))         # 28
        wav_file.write(block_align.to_bytes(2, "little"))       # 30
        wav_file.write(bits_per_sample.to_bytes(2, "little"))   # 32
        wav_file.write(subchunk2_id)                            # 36
        wav_file.write(data_size.to_bytes(4, "little"))         # 40

        wav_file.write(audio_data)                              # 44, audio data starts here

