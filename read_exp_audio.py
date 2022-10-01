import librosa
import soundfile
import numpy as np
from pydub import AudioSegment


def read_file(file_name):
    sound = None
    if ".mp3" in file_name:
        return librosa.load(AudioSegment.from_mp3(file_name))
    elif ".wav" in file_name:
        return librosa.load(sound)
    else:
        return None


def output_file(sound_wave, file_name="output.wav", data=np.random.randn(10, 2), sample_rate=44100):
    return soundfile.write(file_name, data, sample_rate, subtype=None, endian=None, format=None, closefd=True)
