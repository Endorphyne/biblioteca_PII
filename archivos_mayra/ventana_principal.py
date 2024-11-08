from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from gestion_usuarios import VentanaUsuario
from gestion_clientes import VentanaCliente
from estadisticas import VentanaEstadisticas

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Proyecto_Biblioteca/Archivos Ui/VentanaPrincipal.ui", self)

        self.btnusuario.clicked.connect(self.show_gestion_usuarios)
        self.btncliente.clicked.connect(self.show_gestion_clientes)
        self.btnestadisticas.clicked.connect(self.show_estadisticas)

    def show_gestion_usuarios(self):
        self.ventana_usuario = VentanaUsuario()
        self.ventana_usuario.show()

    def show_gestion_clientes(self):
        self.ventana_cliente = VentanaCliente()
        self.ventana_cliente.show()

    def show_estadisticas(self):
        self.ventana_estadisticas = VentanaEstadisticas()
        self.ventana_estadisticas.show()
