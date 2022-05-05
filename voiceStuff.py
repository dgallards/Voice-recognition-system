import speech_recognition as sr
from pydub import AudioSegment
from scipy.io.wavfile import write
import os
import python_speech_features as mfcc
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from scipy.io import wavfile
import librosa
import librosa.display
from librosa.display import waveshow as waveplot
import soundfile
import os
import database
from sklearn.mixture import GaussianMixture

class model:
    gmmModel = GaussianMixture()
    nameOrder = []
    def __init__(self, gmmModel, nameOrder):
        self.gmmModel = gmmModel
        self.nameOrder = nameOrder

    def updateModel(self, gmmModel):
        self.gmmModel = gmmModel
    def incrementList(self, name):
        self.nameOrder.append(name)

modelio = model("xd", [])

def record(fs, duration):

    import sounddevice as sd
    sd._initialize()
    sd.default.samplerate = fs
    sd.default.channels = 2
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    return recording

def recordVoice(time, username):
    fs = 44100
    myrecording = record(fs, time)
    if username:
        write("audios/" + username + ".wav", fs, myrecording)
    else:
        write("features.wav", fs, myrecording)
        sound = AudioSegment.from_wav("features.wav")
        sound.export("speech.wav", format="wav")

def speechRecognition():
    r = sr.Recognizer()
    audio = sr.AudioFile('speech.wav')
    with audio as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="es-ES")

def regenerateModel():

    featureList = []
    fileList = os.listdir(os.getcwd() + "/features")

    for filename in fileList:
        features = np.loadtxt("features/" + filename, delimiter=" ")
        featureList.append(features)
        modelio.incrementList(filename.replace(".csv", ""))

        
    #initialize gmm from sklearn
    modelio.updateModel(GaussianMixture(n_components=len(featureList), covariance_type='diag',n_init=3, reg_covar=1e-1, max_iter=1000, tol=1e-8))
    modelio.gmmModel.fit(featureList)

#extract the features of the new audio.
#mode 1 new user, mode 0 existing user
def extract_features(username, mode):
    filename = "audios/" + username + ".wav" if mode else "speech.wav"
    with soundfile.SoundFile(filename) as audio:
        waveform = audio.read(dtype="float32")
        waveform_mono = librosa.to_mono(waveform.T)

        waveform16k_mono = librosa.resample(waveform_mono, orig_sr=audio.samplerate, target_sr=16000)
        features = np.squeeze(librosa.feature.mfcc(y=waveform16k_mono, sr=16000, n_mfcc=1)).reshape(-1,1).reshape(1,-1)

        if mode: np.savetxt("features/" + username + ".csv", features) 
        else: return predict(features)



def predict(features):
    xd =  modelio.nameOrder[modelio.gmmModel.predict(features)[0]]
    return xd





