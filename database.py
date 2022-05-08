"""
Clase usada para gestionar la base de datos de Mongo.
Sus metodos son autoexplicatorios.
"""

from pymongo import MongoClient
from difflib import SequenceMatcher
import unidecode
import os


class dbHandler:
    def __init__(self):
        self.server = MongoClient("localhost", 27017)
        self.db = self.server.users

    def createUser(self, user):
        try:
            self.db.users.insert_one(user)
            return True
        except:
            return False

    def updateUser(self, user, user2):
        for foundUser in self.db.users.find({"username": user["username"]}):
            try:
                self.db.users.update_one(foundUser, {"$set": user2})
                os.rename(
                    "features/" + user["username"] + ".csv",
                    "features/" + user2["username"] + ".csv",
                )
                os.rename(
                    "audios/" + user["username"] + ".wav", "audios/" + user2["username"] + ".wav"
                )
                return True
            except:
                return False
        return False

    def delUser(self, user):
        for foundUser in self.db.users.find({"username": user["username"]}):
            try:
                self.db.users.delete_one(user)
                os.remove("features/" + user["username"] + ".csv")
                os.remove("audios/" + user["username"] + ".wav")
                return True
            except:
                return False

    def validateUser(self, name, conversation):
        for foundUser in self.db.users.find({"username": name}):
            ratio = SequenceMatcher(
                None,
                unidecode.unidecode(foundUser["password"].lower()),
                unidecode.unidecode(conversation.lower()),
            ).ratio()
            if ratio >= 0.8:
                return foundUser
        return None

    def retrieveUserData(self, name):
        for foundUser in self.db.users.find({"username": name}):
            return foundUser
        return False
