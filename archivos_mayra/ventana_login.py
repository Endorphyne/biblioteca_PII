from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from db_connection import get_db_connection

class LoginWindow(QMainWindow):
    login_inicio_exitoso = pyqtSignal()  

    def __init__(self):
        super().__init__()
        loadUi("Proyecto_Biblioteca/Archivos Ui/Login.ui", self)
        self.btnIniciar.clicked.connect(self.iniciar_sesion)
        
    def iniciar_sesion(self):
        usuario = self.usuario.text()
        contrasena = self.password.text()
        
        conexion = get_db_connection()
        if conexion:
            cursor = conexion.cursor()
            consulta = "SELECT * FROM usuarios WHERE nombre = %s AND password = %s"
            cursor.execute(consulta, (usuario, contrasena))
            resultado = cursor.fetchone()
            if resultado:
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
                self.login_inicio_exitoso.emit()  
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
            conexion.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")

