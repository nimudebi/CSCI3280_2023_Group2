import librosa
import soundfile as sf

def tone_editing(audio_path, pitch_shift,output_path):
    y, sr = librosa.load(audio_path)
    pitch_shift=float(pitch_shift)
    y_shifted = librosa.effects.pitch_shift( y=y,sr=sr,n_steps=pitch_shift)
    sf.write(output_path, y_shifted, sr)