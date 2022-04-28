from cgitb import enable
from curses import panel
import hashlib
import multiprocessing
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import voiceStuff
import database
import sys
from multiprocessing import Process

app = QtWidgets.QApplication(sys.argv)




class InitialScreen(QtWidgets.QDialog):
    def __init__(self):
        super(InitialScreen, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('initialScreen.ui', self) # Load the .ui file


class LoginUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(LoginUsuario, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('loginUsuario.ui', self) # Load the .ui file

class EnvioCorreo(QtWidgets.QDialog):
    def __init__(self):
        super(EnvioCorreo, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('enviarCorreo.ui', self) # Load the .ui file

class SigninUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(SigninUsuario, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('signinUsuario.ui', self) # Load the .ui file
        with open("text.txt", 'r') as f:
            self.text.setText(f.read())
            f.close()

class ConfiguracionUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(ConfiguracionUsuario, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('configuracionUsuario.ui', self) # Load the .ui file

class PanelUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(PanelUsuario, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('panelUsuario.ui', self) # Load the .ui file

class CreacionUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(CreacionUsuario, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('creacionUsuario.ui', self) # Load the .ui file

class ui():

    class Worker(QObject):
            finished = pyqtSignal()
            progress = pyqtSignal(int)
            def run(self):
                """Long-running task."""
                interface.recordVoice()
                self.finished.emit()

    def __init__(self):
        self.initialScreen = InitialScreen()
        self.loginUsuario = LoginUsuario()
        self.envioCorreo = EnvioCorreo()
        self.signinUsuario = SigninUsuario()
        self.configuracionUsuario = ConfiguracionUsuario()
        self.panelUsuario = PanelUsuario()
        self.creacionUsuario = CreacionUsuario()
        self.thread = QThread()
        self.worker = self.Worker()
        self.user

        self.initialScreen.show()
        self.initialScreen.signButton.clicked.connect(lambda: self.move(self.initialScreen, self.creacionUsuario))
        self.initialScreen.loginButton.clicked.connect(lambda: self.move(self.initialScreen, self.loginUsuario))
        self.signinUsuario.loginButton.clicked.connect(lambda: self.move(self.signinUsuario, self.panelUsuario))
        self.signinUsuario.recordButton.clicked.connect(lambda: self.recordVoiceThread())
        self.signinUsuario.loginButton.clicked.connect(lambda: lambda: self.move(self.signinUsuario, self.panelUsuario))
        
        self.loginUsuario.signButton.clicked.connect(lambda: self.move(self.loginUsuario, self.creacionUsuario))
        self.loginUsuario.listenButton.clicked.connect(lambda: self.detectVoices())
        self.configuracionUsuario.confirmButton.clicked.connect(lambda: self.confirmChanges())
        self.configuracionUsuario.backButton.clicked.connect(lambda: self.move(self.configuracionUsuario, self.panelUsuario))
        self.creacionUsuario.createButton.clicked.connect(lambda: self.createUser())
        self.creacionUsuario.backButton.clicked.connect(lambda: self.move(self.creacionUsuario, self.initialScreen))
        self.panelUsuario.emailButton.clicked.connect(lambda: self.move(self.panelUsuario, self.envioCorreo))
        self.panelUsuario.configButton.clicked.connect(lambda: self.move(self.panelUsuario, self.configuracionUsuario))
        self.panelUsuario.logoffButton.clicked.connect(lambda: self.move(self.panelUsuario, self.initialScreen))
        self.panelUsuario.deleteButton.clicked.connect(lambda: self.deleteUser())
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def recordVoice(self):
        self.user["username"] = self.signinUsuario.userName.text()
        self.user["password"] = hashlib.sha256(self.signinUsuario.password.text()).encode().hexdigest(),
        self.user["email"] = self.signinUsuario.email.text()
        if database.createUser(self.user):
            voiceStuff.recordVoice(30, self.username)
            model = voiceStuff.generateModel()
        
    def recordVoiceThread(self):
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.signinUsuario.recordButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.signinUsuario.loginButton.setEnabled(True)
        )

    def detectVoices(self):
        voiceStuff.recordVoice(5)
        nombre = voiceStuff.predict()
        conversation = voiceStuff.speechRecognition()
        self.user = database.validateUser(nombre, conversation)
        if self.user:
            self.username = nombre
            self.move(self.loginUsuario, self.panelUsuario)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error de validación")
            dlg.setText("La configuración de palabras no es válida.")
            dlg.exec()


    def confirmChanges(self):
        self.user["username"] = self.configuracionUsuario.username.text()
        self.user["password"] = self.configuracionUsuario.password.text()
        self.user["email"] = self.configuracionUsuario.email.text()
        if database.updateUser(self.user):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Cambios guardados")
            dlg.setText("Los cambios se han guardado correctamente.")
            dlg.exec()
            self.move(self.configuracionUsuario, self.panelUsuario)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("No se pudieron guardar los cambios.")
            dlg.exec()


    def createUser(self):
        self.username = self.creacionUsuario.username.text()
        self.password = self.creacionUsuario.password.text()

        self.move(self.creacionUsuario, self.signinUsuario)
    
    def deleteUser(self):
        self.move(self.panelUsuario, self.initialScreen)


    def move(self, screen1, screen2):
        screen1.hide()
        screen2.show()



interface = ui()
app.exec_() 
