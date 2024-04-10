def audio_change_start_end(input_file,start_time,end_time):
    with open(input_file,'rb') as wav_in:
        # read header file
        header=bytearray(wav_in.read(44))
        # extract the info. from wav header file
        # format_chunk_size=int.from_bytes(header[16:20],'little')
        num_channels=int.from_bytes(header[22:24],'little')
        sample_rate=int.from_bytes(header[24:28],'little')
        byte_rate=int.from_bytes(header[28:32],'little')
        # print("test: byte_rate: ",byte_rate,"\n")
        bits_per_sample=int.from_bytes(header[34:36],'little') # bit unit
        sample_size=bits_per_sample//8 # byte unit # 2
        data_size=int.from_bytes(header[40:44],'little') # byte unit # 320781 bytes
        audio_data=wav_in.read(data_size) # <class 'bytes'>
    num_samples=data_size//sample_size # 160390 samples
    audio_len_sec=num_samples//sample_rate # 7.2739229024943315 seconds
    if(start_time>=end_time or start_time<0 or end_time>audio_len_sec):
        print("Warning: time selection out of region!\n")
        print(start_time)
        print(end_time)
        return
    data_size_new=(end_time-start_time)*byte_rate
    # print("data and data type of data_size_new: ",data_size_new,"  ",type(data_size_new),"\n")
    data_size_new_byte=data_size_new.to_bytes(4,'little')
    audio_data_new = audio_data[int(start_time * byte_rate):int(end_time * byte_rate)]
    header[40:44]=data_size_new_byte
    return header,audio_data_new
