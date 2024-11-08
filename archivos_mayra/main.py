import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ventana_login import LoginWindow
from ventana_principal import VentanaPrincipal

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.login_window.show()
        self.login_window.login_inicio_exitoso.connect(self.show_main_window)

    def show_main_window(self):
        self.ventana_principal = VentanaPrincipal()
        self.login_window.close()
        self.ventana_principal.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoApp()
    sys.exit(app.exec_())

