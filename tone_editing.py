import librosa
import soundfile as sf

def tone_editing(audio_path, pitch_shift):
    # Load the audio file
    y, sr = librosa.load(audio_path)
    pitch_shift=float(pitch_shift)
    
    # Perform the pitch shifting
    y_shifted = librosa.effects.pitch_shift( y=y,sr=sr,n_steps=pitch_shift)

    # Save the modified audio
    sf.write('D:\CUHK\Y2T2\csci3280\proj\phase1\CantinaBand3_test2.wav', y_shifted, sr)

# Usage example
# audio_path = 'D:\CUHK\Y2T2\csci3280\proj\phase1\CantinaBand3.wav'
# pitch_shift = 10
# tone_editing(audio_path, pitch_shift)