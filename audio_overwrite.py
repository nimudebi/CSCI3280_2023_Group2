def audio_overwrite(input_file, output_file, start_time, fresh_recording):
    with open(fresh_recording, 'rb') as wav_fresh:
        header_fresh = bytearray(wav_fresh.read(44))
        num_channels_fresh = int.from_bytes(header_fresh[22:24], 'little')
        sample_rate_fresh = int.from_bytes(header_fresh[24:28], 'little')
        byte_rate_fresh = int.from_bytes(header_fresh[28:32], 'little')
        bits_per_sample_fresh = int.from_bytes(header_fresh[34:36], 'little')
        sample_size_fresh = bits_per_sample_fresh // 8
        data_size_fresh = int.from_bytes(header_fresh[40:44], 'little')
        audio_data_fresh = bytearray(wav_fresh.read(data_size_fresh))
        num_samples_fresh = data_size_fresh // sample_size_fresh
        audio_len_sec_fresh = num_samples_fresh // sample_rate_fresh


    if sample_rate_fresh != 44100:
        print("invalid sample rate")
        return

    with open(input_file, 'rb') as wav_in:
        # read header file
        header_in = bytearray(wav_in.read(44))
        # extract the info. from wav header file
        # format_chunk_size=int.from_bytes(header[16:20],'little')
        num_channels_in = int.from_bytes(header_in[22:24], 'little')
        sample_rate_in = int.from_bytes(header_in[24:28], 'little')
        byte_rate_in = int.from_bytes(header_in[28:32], 'little')
        # print("test: byte_rate: ",byte_rate,"\n")
        bits_per_sample_in = int.from_bytes(header_in[34:36], 'little')  # bit unit
        sample_size_in = bits_per_sample_in // 8  # byte unit # 2
        data_size_in = int.from_bytes(header_in[40:44], 'little')  # byte unit # 320781 bytes
        audio_data_in = bytearray(wav_in.read(data_size_in))  # <class 'bytes'>
        num_samples_in = data_size_in // sample_size_in  # 160390 samples
        audio_len_sec_in = num_samples_in // sample_rate_in  # 7.2739229024943315 seconds

    if start_time < 0 or int(start_time) > audio_len_sec_in:
        print("Warning: Time region out of limit!\n")

    audio_data_new = bytearray()

    if int(int(start_time) + audio_len_sec_fresh) <= audio_len_sec_in:
        audio_data_new.extend(audio_data_in[0:int(int(start_time) * byte_rate_in)])
        audio_data_new.extend(audio_data_fresh[0:int(audio_len_sec_fresh * byte_rate_fresh)])
        audio_data_new.extend(audio_data_in[
                              (int(int(start_time) * byte_rate_in) + int(audio_len_sec_fresh * byte_rate_fresh)):(
                                  int(audio_len_sec_in * byte_rate_in))])

    if int(int(start_time) + audio_len_sec_fresh) > audio_len_sec_in:
        audio_data_new.extend(audio_data_in[0:int(int(start_time) * byte_rate_in)])
        audio_data_new.extend(audio_data_fresh)
        data_size_new = int(start_time) * byte_rate_in + audio_len_sec_fresh * byte_rate_fresh
        # data_size_new = int(int(start_time) + audio_len_sec_fresh) * byte_rate_in

        # print("data and data type of data_size_new: ",data_size_new,"  ",type(data_size_new),"\n")
        data_size_new_byte = data_size_new.to_bytes(4, 'little')
        header_in[40:44] = data_size_new_byte
    # store new data into new wav file
    with open(output_file, 'wb') as wav_out:
        wav_out.write(header_in)
        wav_out.write(audio_data_new)
    # print("finish saving trimming data\n")

