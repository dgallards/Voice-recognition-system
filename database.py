"""
Clase usada para gestionar la base de datos de Mongo.

De los usuarios se guarda en la base de datos su nombre, contraseña y correo.
Los archivos de audio y features son almacenados en sus respectivas carpetas con el nombre del usuario.
"""

import os
from difflib import SequenceMatcher

import unidecode
from pymongo import MongoClient


class dbHandler:

    # Conexión al servidor.
    def __init__(self):
        self.server = MongoClient("localhost", 27017)
        self.db = self.server.users

    # Creación de usuario. Toma un diccionario con nombre, contraseña y correo del usuario.
    def createUser(self, user):
        try:
            self.db.users.insert_one(user)
            return True
        except:
            return False

    # Actualización de credenciales del usuario, renombra también sus archivos de features y audio.
    def updateUser(self, user, user2):
        for foundUser in self.db.users.find({"username": user["username"]}):
            try:
                self.db.users.update_one(foundUser, {"$set": user2})
                os.rename(
                    "features/" + user["username"] + ".csv",
                    "features/" + user2["username"] + ".csv",
                )
                os.rename(
                    "audios/" + user["username"] + ".wav",
                    "audios/" + user2["username"] + ".wav",
                )
                return True
            except:
                return False
        return False

    # Borrado del usuario de la base de datos y de las carpetas de audio y features.
    def delUser(self, user):
        for foundUser in self.db.users.find({"username": user["username"]}):
            try:
                self.db.users.delete_one(user)
                os.remove("features/" + user["username"] + ".csv")
                os.remove("audios/" + user["username"] + ".wav")
                return True
            except:
                return False

    # Comprobación de identidad del usuario.
    # Se normalizan ambas contraseñas y se comprueba su similitud, si tienen un alto grado, se retornan los datos del usuario.
    def validateUser(self, name, conversation):
        for foundUser in self.db.users.find({"username": name}):
            if conversation:
                ratio = SequenceMatcher(
                    None,
                    unidecode.unidecode(foundUser["password"].lower()),
                    unidecode.unidecode(conversation.lower()),
                ).ratio()
                if ratio >= 0.8:
                    return foundUser
        return None

    # Método usado para obtener las credenciales del usuario.
    def retrieveUserData(self, name):
        for foundUser in self.db.users.find({"username": name}):
            return foundUser
        return False
