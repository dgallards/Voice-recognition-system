""" 
## SECUREMAILING.VOICE

¿No estás cansado de que te roben la cuenta de correo o de robar correos tan fácilmente?

Te presentamos Securemailing.voice, tu deficiente app encargada de reconocerte a ti y solo a ti para enviar correos de una forma más segura.

Con, no solo uno, si no dos mecanismos de seguridad para garantizarte los estándares más elevados de seguridad de un país del tercer mundo, por el modico precio de 3 copilots.

--------------------------------------------------------------------------------

El objetivo de este proyecto es crear un pequeño programa capaz de identificar usuarios a partir de una voz y una contraseña únicas utilizando Machine Learning.
Para ello ofrece una interfaz gráfica con varias funciones básicas implementadas, tales como la creación de usuario y su inicio de sesión, gestión de credenciales y envío de correos.

Se utiliza una gran cantidad de tecnologías en el proyecto tales como MongoDB, PyQt, Cloud Speech o Machine Learning entre otras.

Este archivo controla la interfaz gráfica de la aplicación y la lógica de la misma, haciendo uso de las funciones de la clase VoiceStuff y de la base de datos.
"""

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
from redmail import gmail

# Inicialización de QT y la base de datos.
app = QtWidgets.QApplication(sys.argv)
baseDeDatos = database.dbHandler()

# Se crean ahora las diferentes pantallas de la aplicación, cargandolas de los archivos .ui
class InitialScreen(QtWidgets.QDialog):
    def __init__(self):
        super(InitialScreen, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("initialScreen.ui", self)  # Load the .ui file


class LoginUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(LoginUsuario, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("loginUsuario.ui", self)  # Load the .ui file


class EnvioCorreo(QtWidgets.QDialog):
    def __init__(self):
        super(EnvioCorreo, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("enviarCorreo.ui", self)  # Load the .ui file


class SigninUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(SigninUsuario, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("signinUsuario.ui", self)  # Load the .ui file
        with open("text.txt", "r") as f:
            self.text.setText(f.read())
            f.close()


class ConfiguracionUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(ConfiguracionUsuario, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("configuracionUsuario.ui", self)  # Load the .ui file


class PanelUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(PanelUsuario, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("panelUsuario.ui", self)  # Load the .ui file


class CreacionUsuario(QtWidgets.QDialog):
    def __init__(self):
        super(CreacionUsuario, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("creacionUsuario.ui", self)  # Load the .ui file


class EnvioEmail(QtWidgets.QDialog):
    def __init__(self):
        super(EnvioEmail, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("enviarCorreo.ui", self)  # Load the .ui file


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        interface.recordVoice()
        self.finished.emit()


# Clase que controla la interfaz gráfica de la aplicación, conexiones entre pantallas y llamadas a diferentes métodos.
class ui:
    def __init__(self):
        self.initialScreen = InitialScreen()
        self.loginUsuario = LoginUsuario()
        self.envioCorreo = EnvioCorreo()
        self.signinUsuario = SigninUsuario()
        self.configuracionUsuario = ConfiguracionUsuario()
        self.panelUsuario = PanelUsuario()
        self.creacionUsuario = CreacionUsuario()

        # Datos del usuario actual
        self.user = {}

        # Conexiones y llamadas a métodos.
        self.initialScreen.show()
        self.initialScreen.signButton.clicked.connect(
            lambda: self.move(self.initialScreen, self.creacionUsuario)
        )
        self.initialScreen.loginButton.clicked.connect(
            lambda: self.move(self.initialScreen, self.loginUsuario)
        )
        self.signinUsuario.loginButton.clicked.connect(
            lambda: self.move(self.signinUsuario, self.panelUsuario)
        )
        self.signinUsuario.recordButton.clicked.connect(lambda: self.recordVoiceThread())
        self.signinUsuario.loginButton.clicked.connect(
            lambda: lambda: self.move(self.signinUsuario, self.panelUsuario)
        )
        self.loginUsuario.errorLabel.setHidden(True)
        self.loginUsuario.signButton.clicked.connect(
            lambda: self.move(self.loginUsuario, self.creacionUsuario)
        )
        self.loginUsuario.listenButton.clicked.connect(lambda: self.detectVoices())
        self.configuracionUsuario.confirmButton.clicked.connect(lambda: self.confirmChanges())
        self.configuracionUsuario.backButton.clicked.connect(
            lambda: self.move(self.configuracionUsuario, self.panelUsuario)
        )
        self.creacionUsuario.createButton.clicked.connect(lambda: self.createUser())
        self.creacionUsuario.backButton.clicked.connect(
            lambda: self.move(self.creacionUsuario, self.initialScreen)
        )
        self.panelUsuario.emailButton.clicked.connect(
            lambda: self.move(self.panelUsuario, self.envioCorreo)
        )
        self.panelUsuario.configButton.clicked.connect(
            lambda: self.move(self.panelUsuario, self.configuracionUsuario)
        )
        self.panelUsuario.logoffButton.clicked.connect(
            lambda: self.move(self.panelUsuario, self.initialScreen)
        )
        self.panelUsuario.deleteButton.clicked.connect(lambda: self.deleteUser())
        self.envioCorreo.sendButton.clicked.connect(lambda: self.sendEmail())
        self.envioCorreo.sendButton.clicked.connect(
            lambda: self.move(self.envioCorreo, self.panelUsuario)
        )
        self.envioCorreo.returnButton.clicked.connect(
            lambda: self.move(self.envioCorreo, self.panelUsuario)
        )

    # Método que toma los datos del usuario y su voz y features con el fin de guardarlas en la base de datos o en archivos del programa.
    def recordVoice(self):
        self.user["username"] = self.creacionUsuario.username.text()
        self.user["password"] = self.creacionUsuario.password.text()
        self.user["email"] = self.creacionUsuario.email.text()
        if baseDeDatos.createUser(self.user):
            voiceStuff.recordVoice(10, self.user["username"])
            voiceStuff.extract_features(self.user["username"], True)

    # Intento de grabación de voz sin bloquear la interfaz. No lo conseguimos.
    def recordVoiceThread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.signinUsuario.recordButton.setEnabled(False)
        self.thread.finished.connect(lambda: self.signinUsuario.loginButton.setEnabled(True))

    # Método que detecta la voz del usuario e intenta identificarlo.
    # Pasa dos comprobaciones, la identificación de la persona y su contraseña, si las dos coinciden, el usuario inicia sesión.
    def detectVoices(self):
        voiceStuff.recordVoice(10, None)
        voiceStuff.regenerateModel()
        nombre = voiceStuff.extract_features(None, False)
        print(nombre)
        conversation = voiceStuff.speechRecognition()
        print(conversation)
        self.user = baseDeDatos.validateUser(nombre, conversation)
        if self.user:
            self.user["username"] = nombre
            self.move(self.loginUsuario, self.panelUsuario)
        else:
            self.loginUsuario.errorLabel.setHidden(False)

    # Método usado para cambiar las credenciales del usuario.
    def confirmChanges(self):
        secondUser = self.user
        if self.configuracionUsuario.username.text() != "":
            secondUser["username"] = self.configuracionUsuario.username.text()
        if self.configuracionUsuario.password.text() != "":
            secondUser["password"] = self.configuracionUsuario.password.text()
        if self.configuracionUsuario.email.text() != "":
            secondUser["email"] = self.configuracionUsuario.email.text()
        if baseDeDatos.updateUser(self.user, secondUser):
            self.user = secondUser
            self.move(self.configuracionUsuario, self.panelUsuario)

    # Metodo usado para tomar los datos del usuario.
    def createUser(self):
        self.username = self.creacionUsuario.username.text()
        self.password = self.creacionUsuario.password.text()
        self.email = self.creacionUsuario.email.text()
        self.move(self.creacionUsuario, self.signinUsuario)

    # Método usado para borrar al usuario de la base de datos y sus archivos.
    def deleteUser(self):
        baseDeDatos.deleteUser(self.user["username"])
        self.move(self.panelUsuario, self.initialScreen)

    # Método usado para moverse entre pantallas.
    def move(self, screen1, screen2):
        screen1.hide()
        screen2.show()

    # Método usado para enviar un correo tomando los datos de diferentes campos de la pantalla y Redmail.
    def sendEmail(self):
        gmail.username = self.user["email"]
        # xkdpshvcnlnscnhv diego.diegogz.gallardo53@gmail.com
        gmail.password = self.envioCorreo.contrasena.text()
        gmail.send(
            subject=self.envioCorreo.asunto.text(),
            receivers=[self.envioCorreo.destinatario.text()],
            text=self.envioCorreo.texto.toPlainText(),
            html=self.envioCorreo.texto.toPlainText(),
        )


interface = ui()
app.exec_()
