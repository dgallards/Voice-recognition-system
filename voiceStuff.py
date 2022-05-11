"""
Este archivo es el encargado de realizar métodos relacionados con el tratamiento de voz, desde el grabado hasta la generación de un modelo de predicción.

Para la toma de voz, se ha decidido

El modelo de predicción en el que se ha basado el proyecto es Gaussian Mixture Model.
Se ha escogido éste modelo debido a que consigue buenos niveles de precisión sin comprometer la velocidad de generación del modelo y de obtener una predicción.
No obstante, los resultados de predicción obtenidos son mediocres, fallando a veces a pesar del bajo número de usuarios.
"""

import os

import librosa
import librosa.display
import numpy as np
import sounddevice as sd
import soundfile
import speech_recognition as sr
from librosa.display import waveshow as waveplot
from pydub import AudioSegment
from scipy.io.wavfile import write
from sklearn.mixture import GaussianMixture


# Se crea una clase con el fin de facilitar la llamada a funciones y datos.
class Model:
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


# Creación de un modelo vacío.
modelio = Model("Empty", [])

# Método usado para configurar el recorder y grabar audio durante varios segundos, medido por el parámetro duration.
# El bitrate es marcado por fs.
def record(fs, duration):
    sd._initialize()
    sd.default.samplerate = fs
    sd.default.channels = 2
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    return recording


# Método con dos modos, si no se introduce usuario significa que se está detectando una voz de inicio de sesión.
# Si el usuario se está registrando se guarda su voz en el directorio de audios.
# Si el usuario está iniciando sesión, se genera un archivo temporal para detectar su contraseña con la API de Google.
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
        try:
            text = r.recognize_google(audio, language="es-ES")
            return text
        except:
            return None


# Método que carga todos los archivos de features de los usuarios existentes en la base de datos y genera un modelo que los predice.
def regenerateModel():

    featureList = []
    fileList = os.listdir(os.getcwd() + "/features")

    # Carga de features
    for filename in fileList:
        features = np.loadtxt("features/" + filename, delimiter=" ")
        featureList.append(features)
        modelio.incrementList(filename.replace(".csv", ""))

    # Generación del modelo.
    modelio.updateModel(GaussianMixture(len(featureList)))
    modelio.gmmModel.fit(featureList)


# Método usado para extraer las features de un usuario.
# Si el modo es 0 predice si el usuario intentando logear existe en la base de datos.
# Si el modo es 1 extrae y guarda las features del usuario que intenta registrarse.
def extract_features(username, mode):
    filename = "audios/" + username + ".wav" if mode else "speech.wav"
    with soundfile.SoundFile(filename) as audio:

        # Preprocesamiento del audio.
        waveform = audio.read(dtype="float32")
        waveform_mono = librosa.to_mono(waveform.T)

        waveform16k_mono = librosa.resample(
            waveform_mono, orig_sr=audio.samplerate, target_sr=16000
        )

        # Extracción de features.
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
