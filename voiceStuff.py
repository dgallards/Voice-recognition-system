import speech_recognition as sr
from pydub import AudioSegment
from scipy.io.wavfile import write
import os

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
        audio = r.record(source, language="es-ES")
    return r.recognize_google(audio)

def generateModel():
    #load all files from folder
    for i, filename in enumerate(os.listdir(os.getcwd())):
        return 0

def predict():
    return




