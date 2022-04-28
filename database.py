from pymongo import MongoClient
import hashlib


class dbHandler:

    def __init__(self):
        self.server = MongoClient('localhost', 27017)
        self.db = self.server.users

    def createUser(self, user):
        try:
            self.db.users.insert_one(user)
            return True
        except:
            return False

    def updateUser(self, user):
        for foundUser in self.db.users.find({"name": user["name"]}):
            try:
                self.db.users.update_one(foundUser, {"$set": user})
                return True
            except:
                return False
        return False

    def delUser(self, user):
        try:
            self.db.users.delete_one(user)
            return True
        except:
            return False

    def validateUser(self, name, conversation, user):
        for foundUser in self.db.users.find({"name": name}):
            if foundUser["password"] == conversation:
                return user
        return None

    def retrieveUserData(self, name):
        for foundUser in self.db.users.find({"name": name}):
            return foundUser
        return False
