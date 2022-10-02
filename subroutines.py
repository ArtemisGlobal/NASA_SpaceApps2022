import numpy as np
import librosa
from audiolazy import str2midi, midi2freq, midi2str, str2freq
from thinkdsp import *
from PIL import Image
import pandas as pd
import urllib.request

class Song():
    def __init__(self, audio_path, tend=22):
        self.audio_path = audio_path
        self.tend = tend
        self._load()
        self._get_key()
        self._get_tempo()
        
    def _load(self):
        y, sr = librosa.load(self.audio_path)
        self.y = y
        self.sr = sr
        
    def _get_key(self, pentOn=True):
        y_harmonic, y_percussive = librosa.effects.hpss(self.y)
        tonal_frag = Tonal_Fragment(y_harmonic, self.sr, tend=self.tend) #analyse up to tend
        tonal_frag.print_key()
        key = tonal_frag.get_key()
        self.root = key[:2].strip() #should find better way!
        self.scale = key[2:].strip()
        if pentOn:
            self.scale  = key[2:].strip() + 'Pent'
        else: 
            self.scale  = key[2:].strip()
    
    def _get_tempo(self):
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        self.tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sr)[0]
        print('likely tempo: ',self.tempo)
        
        
class ImageCatalog():
    def __init__(self,image_csv_path):
        self.image_csv_path = image_csv_path
        self._get_metadata()
        
    def _get_metadata(self):
        cols = ['ImageName','FileDir','CollectDate','Instrument'] #columns in image list csv
        df = pd.read_csv(self.image_csv_path, header=0, usecols=cols,skip_blank_lines=True,encoding='utf-8')#'latin1'
        self.image_names = df['ImageName'].tolist()
        self.image_urls = df['FileDir'].tolist()
        
    def get_image_path(self, image_index):
        image_url = self.image_urls[image_index] 
        image_name = self.image_names[image_index]
        if '.jpg' in image_url:
            image_format = '.jpg'
        elif '.png' in image_url:
            image_format = '.png'   
        image_path = './images/' + image_name + image_format
        urllib.request.urlretrieve(image_url, image_path)
        return image_path
    
    def get_image_name(self, image_index):
        return self.image_names[image_index]
    
class Sonification():
    def __init__(self, image_path,song,freqs,sonif_duration):
        self.image_path = image_path
        self.song = song
        self.freqs = freqs
        self.sonif_duration = sonif_duration
        self._get_pixels()
        self._make_sonification()
        
    def _get_pixels(self):
        img = Image.open(self.image_path) 
        img = boost_contrast(img) #makes structure easier to hear

        imgR = img.resize(size = (img.width,len(self.freqs)), resample=Image.LANCZOS) 
        self.pixels = np.array(imgR.convert('L'))/255 #normalize
        
    def _make_sonification(self):
        self.wave = additive_synth(self.pixels, self.freqs, self.song.sr, self.sonif_duration)
        self.wave.normalize(0.9)
        self.y = self.wave.ys
        
    def save_sonification(self,path):
        self.wave.write(path)
        
#From: https://github.com/jackmcarthur/musical-key-finder 
# class that uses the librosa library to analyze the key that an mp3 is in
# arguments:
#     waveform: an mp3 file loaded by librosa, ideally separated out from any percussive sources
#     sr: sampling rate of the mp3, which can be obtained when the file is read with librosa
#     tstart and tend: the range in seconds of the file to be analyzed; default to the beginning and end of file if not specified
class Tonal_Fragment(object):
    def __init__(self, waveform, sr, tstart=None, tend=None):
        self.waveform = waveform
        self.sr = sr
        self.tstart = tstart
        self.tend = tend
        
        if self.tstart is not None:
            self.tstart = librosa.time_to_samples(self.tstart, sr=self.sr)
        if self.tend is not None:
            self.tend = librosa.time_to_samples(self.tend, sr=self.sr)
        self.y_segment = self.waveform[self.tstart:self.tend]
        self.chromograph = librosa.feature.chroma_cqt(y=self.y_segment, sr=self.sr, bins_per_octave=24)
        
        # chroma_vals is the amount of each pitch class present in this time interval
        self.chroma_vals = []
        for i in range(12):
            self.chroma_vals.append(np.sum(self.chromograph[i]))
        pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        # dictionary relating pitch names to the associated intensity in the song
        self.keyfreqs = {pitches[i]: self.chroma_vals[i] for i in range(12)} 
        
        keys = [pitches[i] + ' major' for i in range(12)] + [pitches[i] + ' minor' for i in range(12)]

        # use of the Krumhansl-Schmuckler key-finding algorithm, which compares the chroma
        # data above to typical profiles of major and minor keys:
        maj_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        min_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

        # finds correlations between the amount of each pitch class in the time interval and the above profiles,
        # starting on each of the 12 pitches. then creates dict of the musical keys (major/minor) to the correlation
        self.min_key_corrs = []
        self.maj_key_corrs = []
        for i in range(12):
            key_test = [self.keyfreqs.get(pitches[(i + m)%12]) for m in range(12)]
            # correlation coefficients (strengths of correlation for each key)
            self.maj_key_corrs.append(round(np.corrcoef(maj_profile, key_test)[1,0], 3))
            self.min_key_corrs.append(round(np.corrcoef(min_profile, key_test)[1,0], 3))

        # names of all major and minor keys
        self.key_dict = {**{keys[i]: self.maj_key_corrs[i] for i in range(12)}, 
                         **{keys[i+12]: self.min_key_corrs[i] for i in range(12)}}
        
        # this attribute represents the key determined by the algorithm
        self.key = max(self.key_dict, key=self.key_dict.get)
        self.bestcorr = max(self.key_dict.values())
        
        # this attribute represents the second-best key determined by the algorithm,
        # if the correlation is close to that of the actual key determined
        self.altkey = None
        self.altbestcorr = None

        for key, corr in self.key_dict.items():
            if corr > self.bestcorr*0.9 and corr != self.bestcorr:
                self.altkey = key
                self.altbestcorr = corr
                
    # prints the relative prominence of each pitch class            
    def print_chroma(self):
        self.chroma_max = max(self.chroma_vals)
        for key, chrom in self.keyfreqs.items():
            print(key, '\t', f'{chrom/self.chroma_max:5.3f}')
            
    def get_chroma(self):
        chroma_dict = {}
        self.chroma_max = max(self.chroma_vals)
        for key, chrom in self.keyfreqs.items():
            chroma_dict[key] = chrom/self.chroma_max
        return chroma_dict
                
    # prints the correlation coefficients associated with each major/minor key
    def corr_table(self):
        for key, corr in self.key_dict.items():
            print(key, '\t', f'{corr:6.3f}')
    
    # printout of the key determined by the algorithm; if another key is close, that key is mentioned
    def print_key(self):
        print("likely key: ", max(self.key_dict, key=self.key_dict.get), ", correlation: ", self.bestcorr, sep='')
        if self.altkey is not None:
                print("also possible: ", self.altkey, ", correlation: ", self.altbestcorr, sep='')
    
    def get_key(self):
        return max(self.key_dict, key=self.key_dict.get)
    
    # prints a chromagram of the file, showing the intensity of each pitch class over time
    def chromagram(self, title=None):
        C = librosa.feature.chroma_cqt(y=self.waveform, sr=sr, bins_per_octave=24)
        plt.figure(figsize=(12,4))
        librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='chroma', vmin=0, vmax=1)
        if title is None:
            plt.title('Chromagram')
        else:
            plt.title(title)
        plt.colorbar()
        plt.tight_layout()
        plt.show()
        
        
def get_scale_notes(start_note='C1', octaves=3, scale='majorHex'):
    #Returns a list of Diatonic Notes
    
    scales = {
    'ionian':[2,2,1,2,2,2,1],
    'major':[2,2,1,2,2,2,1],
    'dorian':[2,1,2,2,2,1,2],
    'phrygian':[1,2,2,2,1,2,2],
    'lydian':[2,2,2,1,2,2,1],
    'mixolydian':[2,2,1,2,2,1,2],
    'aeolian':[2,1,2,2,1,2,2],
    'minor':[2,1,2,2,1,2,2],
    'lochrian':[1,2,2,1,2,2,2],
    'majorPent':[2,2,3,2,3],
    'minorPent':[3,2,2,3,2],
    'majorHex':[2,2,3,2,2,1],
    'minorHex':[2,1,2,2,3,2],
    'minorPent':[3,2,2,3,2],
    'wholetone':[2,2,2,2,2,2],
    'melodicMinor':[2,1,2,2,2,2,1],
    'harmonicMinor':[2,1,2,2,1,3,1],
    'chromatic':[1]*12,
    }
    
    if type(scale) is str:
        scale_list = scales[scale]
    if type(scale) is list:
        scale_list = scale
        
    scale_notes = []
    for octave in range(octaves):
        midi_note = str2midi(start_note) + (12*octave) #first octave = 0, 2nd=1, etc
        
        for step in scale_list:
            scale_notes.append(midi2str(midi_note))
            midi_note = midi_note + step
    last_midi_note = str2midi(start_note) + (octaves*12) #sets last note
    scale_notes.append(midi2str(last_midi_note)) #there must be a better way to do this
            
    return scale_notes
    
def get_scale_freqs(start_note='C1', octaves=3, scale='majorHex'):
    scale_notes = get_scale_notes(start_note, octaves, scale)
    scale_freqs = [str2freq(n) for n in scale_notes]
    return scale_freqs

def boost_contrast(image): 
        """boost contrast in current image with cosine curve
        
        argument:PIL image (RGB)
        
        returns: PIL image (RGB)
        """
        
        im_array = np.array(image)
        im_array = 255./2*(1 - np.cos(np.pi*im_array/np.amax(im_array)))
        #im_array = map_value(-np.cos(np.pi*im_array/np.amax(im_array)), -1, 1, 0, 255)
        image = Image.fromarray(im_array.astype(np.uint8), "RGB")#.show()
        return image

def additive_synth(pixel_array, freqs, fs, duration):
    """Converts array to wave with additive synthesis

    returns: thinkdsp wave
    """
    height,width = np.shape(pixel_array)
    freqs_rev = np.array(freqs[::-1])

    Ns = int(fs*duration)

    lut = LUT() #create sine wave look up table 
    delPhase = lut.N * freqs_rev/fs    #phase increment for each frequency
    np.random.seed(0)
    phi = lut.N * np.random.rand(np.shape(pixel_array)[0])  #set initial phase for each frequency

    ts = np.linspace(0, duration, Ns, endpoint=False)

    ys=[]
    for n in range(Ns):
        colindex = int((n/Ns*width)) #or ceil or floor?
        colindexRem = n/Ns*width - colindex

        phi = (phi + delPhase)%lut.N #find new phase of each frequency component
        phi_int = phi.astype(int)

        Amp = pixel_array[:,colindex] + colindexRem*(pixel_array[:,min(colindex+1,width-1)]-pixel_array[:,colindex]) 

        yi = Amp*lut.waveLUT[phi_int]
        ys.append(yi.sum())

    wave = Wave(ys,ts,framerate=fs)
    spectrum = wave.make_spectrum()
    spectrum.low_pass(cutoff=max(freqs),factor=0.) #only if artifact
    wave = spectrum.make_wave()
    return wave

class LUT:
    '''look up table object'''
    def __init__(self, waveform='sine', M=1, N=2**10):
        self.N = N
        if isinstance(waveform,str):
            if waveform not in ['sin','sine','cos','square','tri','triangle','saw','sawtooth']:
                print('Waveform name must be one of',['sin','sine','cos','square','triangle','sawtooth'])
            self.waveform = waveform
            self.M = M
            self._make_wave()
        if isinstance(waveform, list) or isinstance(waveform, np.ndarray):
            self.M = None
            self.custom(waveform)
                
    def _make_wave(self):
        lutSamp = np.arange(self.N)
        if self.waveform in ['sin','sine']:
            self.waveform = 'sine'
            self.waveLUT=np.sin(2 * np.pi * lutSamp/self.N)
        if self.waveform=='cos':
            self.waveLUT=np.cos(2 * np.pi * lutSamp/self.N)
        if self.waveform =='square':
            self.waveLUT=np.zeros(self.N)
            for m in range(self.M):
                self.waveLUT += 4/np.pi/(2*m+1)*np.sin((2*m+1)*2 * np.pi * lutSamp/self.N) 
        if self.waveform in ['tri','triangle']:
            self.waveform = 'triangle'
            self.waveLUT=np.zeros(self.N)
            for m in range(self.M):
                self.waveLUT += 8/(np.pi)**2*(-1)**m/(2*m+1)**2*np.sin((2*m+1)*2 * np.pi * lutSamp/self.N)
        if self.waveform in ['saw','sawtooth']:
            self.waveLUT=np.zeros(self.N)
            for m in range(self.M):
                self.waveLUT += -1/np.pi/(m+1)*np.sin((m+1)*2 * np.pi * lutSamp/self.N)
                
    def custom(self, wave_samples):
        self.waveform = 'custom'
        wave_samples = map_value(wave_samples, min(wave_samples), max(wave_samples), -1, 1.)
        ts_input = np.linspace(0, self.N, len(wave_samples)) #is this right? endpoint=True?
        ts_target = np.arange(0, self.N)
        self.waveLUT = np.interp(ts_target, ts_input, wave_samples, left=None, right=None, period=None)
        return self
    
    def plot(self):
        plt.figure(figsize=(10,3))

        plt.plot(np.arange(0, self.N), self.waveLUT )
        plt.title(self.waveform + ', M =' + str(self.M))
        plt.show()