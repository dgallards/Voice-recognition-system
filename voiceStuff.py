"""
Este archivo es el encargado de realizar métodos relacionados con el tratamiento de voz, desde el grabado hasta la generación de un modelo de predicción.
"""
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
import sounddevice as sd

# Se crea una clase con el fin de facilitar la llamada a funciones y datos.
class model:
    # Modelo de predicción.
    gmmModel = GaussianMixture()
    # Orden de los archivos cargados, es muy importante mantenerlo para saber cual es la predicción del modelo.
    nameOrder = []

    def __init__(self, gmmModel, nameOrder):
        self.gmmModel = gmmModel
        self.nameOrder = nameOrder

    def updateModel(self, gmmModel):
        self.gmmModel = gmmModel

    def incrementList(self, name):
        self.nameOrder.append(name)


modelio = model("xd", [])

# Método usado para configurar el recorder y grabar audio durante varios segundos.
def record(fs, duration):
    sd._initialize()
    sd.default.samplerate = fs
    sd.default.channels = 2
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    return recording


# Método con dos modos, si no se introduce usuario significa que se está detectando una voz de inicio de sesión.
# Si el usuario se está registrando se guarda su voz en el directorio de audios.
# Si el usuario está logeando, se genera un archivo temporal para detectar su contraseña.
def recordVoice(time, username):
    fs = 44100
    myrecording = record(fs, time)
    if username:
        write("audios/" + username + ".wav", fs, myrecording)
    else:
        write("features.wav", fs, myrecording)
        sound = AudioSegment.from_wav("features.wav")
        sound.export("speech.wav", format="wav")


# Método usado para el Speech to Text, haciendo una llamada a la API de Cloud Speech, tiene que cargar los datos desde un archivo formateado.
def speechRecognition():
    r = sr.Recognizer()
    audio = sr.AudioFile("speech.wav")
    with audio as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="es-ES")


# Método que carga todos los archivos de features de los usuarios existentes en la base de datos y genera un modelo que los predice.
def regenerateModel():

    featureList = []
    fileList = os.listdir(os.getcwd() + "/features")

    for filename in fileList:
        features = np.loadtxt("features/" + filename, delimiter=" ")
        featureList.append(features)
        modelio.incrementList(filename.replace(".csv", ""))

    modelio.updateModel(
        GaussianMixture(
            n_components=len(featureList),
            covariance_type="diag",
            n_init=3,
            reg_covar=1e-1,
            max_iter=1000,
            tol=1e-8,
        )
    )
    modelio.gmmModel.fit(featureList)


# Método usado para extraer las features de un usuario.
# Si el modo es 0 predice si el usuario intentando logear existe en la base de datos.
# Si el modo es 1 extrae y guarda las features del usuario que intenta registrarse.
def extract_features(username, mode):
    filename = "audios/" + username + ".wav" if mode else "speech.wav"
    with soundfile.SoundFile(filename) as audio:
        waveform = audio.read(dtype="float32")
        waveform_mono = librosa.to_mono(waveform.T)

        waveform16k_mono = librosa.resample(
            waveform_mono, orig_sr=audio.samplerate, target_sr=16000
        )
        features = (
            np.squeeze(librosa.feature.mfcc(y=waveform16k_mono, sr=16000, n_mfcc=1))
            .reshape(-1, 1)
            .reshape(1, -1)
        )

        if mode:
            np.savetxt("features/" + username + ".csv", features)
        else:
            return predict(features)


# Método que devuelve un nombre con el resultado de la predicción del modelo.
def predict(features):
    return modelio.nameOrder[modelio.gmmModel.predict(features)[0]]
