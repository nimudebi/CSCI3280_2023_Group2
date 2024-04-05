import os
import pyaudio

os.system('python -m spleeter separate -p spleeter:2stems -o karaoke_bgm <input_file>')

def karaoke_bgm(input_num,input_file=None, bgm_dic = 'karaoke_bgm'):
    """
    :param input_num: if -1, users want to input their own bgm. Else, it means the num of bgm the users chose
    :param input_file: if users want input their own bgm, the input_file is the position the input file. Else it will be None
    :param bgm_dic: the file used to store the bgm this function generates
    :return: the position of the karaoke bgm
    """
    # Install configuration file
    warning = "If you want to use karaoke function, please ensure that you have anaconda or miniconda on you PC"
    print(warning)
    os.system('conda install -c conda-forge ffmpeg libsndfile')
    if(input_num > 0):
        for i in range(10):
            if(i == input_num):
                bgm_file = 'karaoke_bgm/' + str(i) + '.wav'
                return bgm_file
    else:
        cmd = 'python -m spleeter separate -p spleeter:2stems -o karaoke_bgm ' + input_file
        os.system(cmd)
        bgm_file = 'karaoke_bgm/' + input_file + '/accompaniment.wav'
        return bgm_file
def karaoke(input_bgm):
    # 缺個錄音功能


