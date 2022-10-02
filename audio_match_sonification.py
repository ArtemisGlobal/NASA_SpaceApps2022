###################################
#Script to sonify an image using key and tempo extracted from a pre-existing song, then mix them together
###################################

import librosa
from pydub import AudioSegment
from PIL import Image
import pandas as pd 
import urllib.request
from subroutines import *
        
        
#####choose image from catalog#########################

image_urls_path = 'WebbDemo.csv'  

image_index = 0  #this can be fed in as an argument, passed by image selector

#####choose song#########

audio_filename = 'electric-feel' #could pass this as argument
# audio_filename = 'sweet-home-alabama' #should be G major, 98bpm, 4/4

audio_format = '.mp3' #.wav or .mp3
     
#####choose sonification parameters#########

start_octave = 3 #keep it kind of high to not clash as much
n_octaves = 3

beats_per_bar = 4  #assume 4/4, doesn't matter much
n_bars = 16   #number of bars before looping sonification

mix = 0.6 #0 to 1 

######################################################################
####load and analyze song##################################################

audio_path = './songs/' + audio_filename + audio_format

song = Song(audio_path) #loads song, finds key and tempo
    
freqs = get_scale_freqs(start_note=song.root + str(start_octave), octaves=n_octaves, scale=song.scale)

#####DOWNLOAD IMAGE, get path###################################
#should also delete image file at end

image_catalog = ImageCatalog(image_urls_path)
image_path = image_catalog.get_image_path(image_index) 

####SONIFICATION################################

time_per_bar = beats_per_bar*60/song.tempo
sonif_duration = n_bars*time_per_bar #seconds, need to set with tempo, key signature and # of bars

print('sonification duration: ',round(sonif_duration,2),'seconds')
print('song duration: ',round(len(song.y)/song.sr,2),'seconds')

sonification = Sonification(image_path, song, freqs, sonif_duration)  
sonification.save_sonification('./sonifications/' + image_catalog.get_image_name(image_index) + '.wav')

#####MIXING####################################

#make sure there is a wav version, needed to load with thinkdsp
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

if len(sonification.y)<len(wave_song.ts):
    n_samp = 0
    n_sonf_samp = len(sonification.y)
    while n_samp<len(wave_song.ts)- n_sonf_samp:
        wave_mix.ys[n_samp:n_samp + n_sonf_samp] = (1 - mix)*wave_song.ys[n_samp:n_samp + n_sonf_samp] + mix*sonification.y
        n_samp += len(sonification.y)
else:
    wave_mix.ys = (1 - mix)*wave_song.ys + mix*sonification.y[:len(wave_song.ys)]
    
wave_mix.normalize(0.9)
wave_mix.write('./mixes/' + audio_filename + ' + ' +image_catalog.get_image_name(image_index) + '.wav')
