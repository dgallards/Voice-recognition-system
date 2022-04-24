from pymongo import MongoClient
import hashlib

def connectToDB():
    server = MongoClient()
    return MongoClient('localhost', 27017)

def createUser(username, password, email):
    return

def addUser(user):
    return

def deleteUser(user):
    return

