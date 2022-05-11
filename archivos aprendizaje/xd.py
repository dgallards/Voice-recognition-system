from pymongo import MongoClient

server = MongoClient("localhost", 27017)
db = server.users

for foundUser in db.users.find():
    print(foundUser)
    # db.users.delete_one(foundUser)


"""
from redmail import gmail
gmail.username = "diego.diegogz.gallardo53@gmail.com"
gmail.password = "xkdpshvcnlnscnhv"
gmail.send(subject="WE're bored", receivers = ["dgallards@alumnos.unex.es"], text = "hola mundo", html = "hola mundo")
print("Correo enviado")

"""
"""
import os
import numpy as np
from sklearn.mixture import GaussianMixture
featureList = []
gmmModel = None
nameOrder = []

def regenerateModel():
    featureList = []
    fileList = os.listdir(os.getcwd() + "/features")
    if len(fileList) > 1:
        for filename in os.listdir(os.getcwd() + "/features"):
            features = np.loadtxt("features/" + filename, delimiter=" ")
            featureList.append(features)
            nameOrder.append(filename.replace(".csv", ""))

    
        #initialize gmm from sklearn
        gmmModel = GaussianMixture(n_components=len(featureList), covariance_type='diag',n_init=3, reg_covar=1e-1, max_iter=1000, tol=1e-8)
        gmmModel.fit(featureList)
regenerateModel()
"""
