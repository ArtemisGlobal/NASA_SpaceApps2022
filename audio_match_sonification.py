###################################
#Script to sonify an image using key and tempo extracted from a pre-existing song, then mix them together
###################################

import librosa
from pydub import AudioSegment
from PIL import Image
import pandas as pd 
import urllib.request
from subroutines import *

#####choose song#########

audio_filename = 'electric-feel' #could pass this as argument

# audio_filename = 'sweet-home-alabama' #should be G major, 98bpm, 4/4

audio_format = '.mp3' #.wav or .mp3
     
#####choose sonification parameters#########

start_octave = 3 #keep it kind of high to not clash as much
n_octaves = 3

pentOn = True #use pentatonic for a less dissonant result

beats_per_bar = 4  #assume 4/4, doesn't matter much
n_bars = 16   #number of bars before looping sonification

mix = 0.6 #0 to 1 

#####choose image#########################

cols = ['ImageName','FileDir','CollectDate','Instrument'] #columns in image list csv
image_urls_path = 'WebbDemo.csv'  

image_index = 0  #this can be fed in as an argument, passed by image selector

######################################################################
####analyse audio##################################################

audio_path = './songs/' + audio_filename + audio_format

y, sr = librosa.load(audio_path)
y_harmonic, y_percussive = librosa.effects.hpss(y)
tonal_frag = Tonal_Fragment(y_harmonic, sr, tend=22)
tonal_frag.print_key()

key = tonal_frag.get_key()
key_letter = key[:2].strip() #should find better way!
key_harmony = key[2:].strip()

if pentOn:
    scale = key_harmony + 'Pent'
else: 
    scale = key_harmony
    
freqs = get_scale_freqs(start_note=key_letter + str(start_octave), octaves=n_octaves, scale=scale)

onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
print('likely tempo: ',tempo,'bpm')

#####IMAGE###################################

df = pd.read_csv(image_urls_path, header=0, usecols=cols,skip_blank_lines=True,encoding='utf-8')#'latin1'
image_names = df['ImageName'].tolist()
image_urls = df['FileDir'].tolist()


image_url = image_urls[image_index] 
image_name = image_names[image_index]
image_format = image_url[-4:]
urllib.request.urlretrieve(image_url, './images/' + image_name + image_format)

img = Image.open('./images/' + image_name + image_format)
img = boost_contrast(img) #makes structure easier to hear

imgR = img.resize(size = (img.width,len(freqs)), resample=Image.LANCZOS) 
pixels = np.array(imgR.convert('L'))/255 #normalize, could leaveas RGB then separate later



####SONIFICATION################################
time_per_bar = beats_per_bar*60/tempo
duration = n_bars*time_per_bar #seconds, need to set with tempo, key signature and # of bars

print('sonification duration: ',round(duration,2),'seconds')

wave_sonif = additive_synth(pixels, freqs, sr, duration)
wave_sonif.normalize(0.9)
wave_sonif.write('./sonifications/' + image_name + '.wav')

#####MIXING####################################

if '.wav' in audio_path:
    wave_song = read_wave(audio_path)
elif '.mp3' in audio_path:
    try:
        wave_song = read_wave(audio_path.strip('mp3') + 'wav')
    except:
        sound = AudioSegment.from_mp3(audio_path)
        sound.export(audio_path.strip('mp3') + 'wav', format="wav")
        wave_song = read_wave(audio_path.strip('mp3') + 'wav')

wave_mix = wave_song.copy()

if len(wave_sonif.ts)<len(wave_song.ts):
    n_samp = 0
    n_sonf_samp = len(wave_sonif.ts)
    while n_samp<len(wave_song.ts)- n_sonf_samp:
        wave_mix.ys[n_samp:n_samp + n_sonf_samp] = (1 - mix)*wave_song.ys[n_samp:n_samp + n_sonf_samp] + mix*wave_sonif.ys
        n_samp += len(wave_sonif.ts)
else:
    print('reduce number of bars for sonification or try a longer song')

wave_mix.normalize(0.9)
wave_mix.write('./mixes/' + audio_filename + ' + ' +image_name + '.wav')
