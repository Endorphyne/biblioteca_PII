import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout,
    QFormLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout,QSpinBox,QDateEdit,QComboBox,
)
from PyQt5.QtCore import Qt, QDate
from conexiones_sql import Database as db
from datetime import datetime
#conexion con la db
db = db('config.ini','biblioteca')
db.connect()
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)
        layout.addRow(self.login_button)
        
        self.setLayout(layout)

    def login(self):
        self.main_window = MainApp()
        self.main_window.show()
        self.close()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Login y CRUD")
        self.setGeometry(100, 100, 800, 600)
        
        # Crear un QStackedWidget para la navegación de ventanas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear la ventana principal CRUD
        self.crud_window = QWidget()
        self.crud_layout = QVBoxLayout(self.crud_window)
        # Crear el TabWidget con pestañas CRUD
        self.tab_widget = QTabWidget()
        # Pestañas
        self.create_tab("Usuarios", db.get_column_names('usuarios'))
        self.create_tab("Clientes", db.get_column_names('clientes'))
        self.create_tab("Libros", db.get_column_names('libros'))
        self.create_tab("Prestamos", db.get_column_names('prestamos'))
        self.create_tab("Reservas", db.get_column_names('reservas'))
        self.crud_layout.addWidget(self.tab_widget)
        self.stacked_widget.addWidget(self.crud_window)
    
    def closeEvent(self, event):
        db.close()  # Cerrar la conexión a la base de datos
        event.accept()  # Aceptar el evento de cierre

    def create_tab(self, title, column_names):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # Crear la tabla con columnas personalizadas
        table = QTableWidget(0, len(column_names))
        table.setHorizontalHeaderLabels(column_names)
        table.setAlternatingRowColors(True)

        # Crear el layout de botones
        button_layout = QHBoxLayout()
        add_button = QPushButton("Agregar")
        edit_button = QPushButton("Modificar")
        delete_button = QPushButton("Eliminar")
        stats_button = QPushButton("Estadísticas")
        refresh_button = QPushButton("Actualizar Tabla")

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(stats_button)
        button_layout.addWidget(refresh_button)

        # Conectar el botón de refresco de la tabla
        refresh_button.clicked.connect(lambda: self.actualizar_tabla(table, title.lower()))

        # Agregar la tabla y los botones al layout de la pestaña
        tab_layout.addWidget(table)
        tab_layout.addLayout(button_layout)

        # Añadir la pestaña al TabWidget
        self.tab_widget.addTab(tab, title)

        # Cargar los datos en la tabla al crear la pestaña
        self.actualizar_tabla(table, title.lower())

        #funciones de los botones
        add_button.clicked.connect(self.open_form)
        edit_button.clicked.connect(self.open_form)
        delete_button.clicked.connect(self.open_form)

    def open_form(self):
        # Obtener el título de la pestaña activa
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_title = self.tab_widget.tabText(current_tab_index)

        if current_tab_title == "Usuarios":
            self.form = formulario_user("Agregar Usuario")
            self.form.show()
        elif current_tab_title == "Clientes":
            self.form = formulario_cliente("Agregar Cliente")
            self.form.show()
        elif current_tab_title == "Libros":
            self.form = formulario_libro("Agregar Libro")
            self.form.show()
        elif current_tab_title == "Prestamos":
            self.form = formulario_prestamo("Agregar Préstamo")
            self.form.show()
        elif current_tab_title == "Reservas":
            self.form = formulario_reserva("Agregar Reserva")
            self.form.show()

    def actualizar_tabla(self, table_widget, table_name):
        """
        Actualiza el contenido del QTableWidget con los datos de la base de datos.
        
        table_widget = El widget QTableWidget que se va a actualizar.
        table_name = Nombre de la tabla en la base de datos.
        """
        try:
            query = f"SELECT * FROM {table_name}"  # Asegúrate de que table_name tenga el nombre correcto
            resultados = db.execute_query(query)

            # Limpiar la tabla antes de cargar nuevos datos
            table_widget.setRowCount(0)

            # Agregar datos al QTableWidget
            for row_number, row_data in enumerate(resultados):
                table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except Exception as e:
            print(f"Error al actualizar la tabla {table_name}: {e}")



class formulario_user(QWidget):
    def __init__(self, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        
        # Campos del formulario
        self.campo1 = QLineEdit()
        self.campo2 = QLineEdit()
        self.campo3 = QLineEdit()
        
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Nombre :", self.campo1)
        self.form_layout.addRow("Contraseña:", self.campo2)
        self.form_layout.addRow("Confirmar Contraseña:", self.campo3)
        
        # Añadir el layout de formulario al layout principal
        self.main_layout.addLayout(self.form_layout)

        # Botones de acción
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        # Añadir botones al layout de botones
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Añadir el layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)
        self.save_button.clicked.connect(lambda: self.guardar_usuario())
        self.cancel_button.clicked.connect(lambda: self.close())

    def comprobrar_campos(self)->bool:
        nombre = self.campo1.text()
        if len(nombre)<0 and len(nombre) >150:
            return False
        if self.campo2.text() != self.campo3.text():
            return False
        return True
        
    def guardar_usuario(self):
        if self.comprobrar_campos():
            values = (self.campo1.text(),self.campo2.text(),datetime.now())
            db.execute_query('INSERT INTO usuarios(nombre,password,fecha_creacion) VALUES (%s,%s,%s)',values)
            self.close()

class formulario_cliente(QWidget):
    def __init__(self, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        
        # Campos del formulario
        self.campo1 = QLineEdit()
        self.campo2 = QLineEdit()
        self.campo3 = QLineEdit()
        self.campo4 = QLineEdit()
        self.campo5 = QLineEdit()
        self.campo6 = QLineEdit()
        self.campo7 = QSpinBox()
        
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Nombre :", self.campo1)
        self.form_layout.addRow("Apellido :", self.campo2)
        self.form_layout.addRow("Documento :", self.campo3)
        self.form_layout.addRow("Nacimiento(yyyy/mm/dd) :", self.campo4)
        self.form_layout.addRow("Direccion:", self.campo5)
        self.form_layout.addRow("Telefono:", self.campo6)
        self.form_layout.addRow("Usuario ID:", self.campo7)

        # Añadir el layout de formulario al layout principal
        self.main_layout.addLayout(self.form_layout)

        # Botones de acción
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        # Añadir botones al layout de botones
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Añadir el layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)
        self.save_button.clicked.connect(lambda: self.guardar_cliente())
        self.cancel_button.clicked.connect(lambda: self.close())
    def guardar_cliente(self):
        values = (self.campo1.text(),self.campo2.text(),self.campo3.text(),self.campo4.text(),self.campo5.text(),datetime.now(),self.campo6.text(),self.campo7.value())
        print(values)
        db.execute_query('INSERT INTO clientes (nombre, apellido, documento, nacimiento, direccion, telefono, fecha_registro,usuarios_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',values)
        self.close()

class formulario_libro(QWidget):
    def __init__(self, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        
        # Campos del formulario
        self.campo1 = QLineEdit()
        self.campo2 = QLineEdit()
        self.campo3 = QLineEdit()
        self.campo4 = QLineEdit()
        self.campo5 = QSpinBox()
        
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Titulo :", self.campo1)
        self.form_layout.addRow("Autor:", self.campo2)
        self.form_layout.addRow("Editorial:", self.campo3)
        self.form_layout.addRow("Genero :", self.campo4)
        self.form_layout.addRow("Stock :", self.campo5)
        
        # Añadir el layout de formulario al layout principal
        self.main_layout.addLayout(self.form_layout)

        # Botones de acción
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        # Añadir botones al layout de botones
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Añadir el layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)
        self.save_button.clicked.connect(lambda: self.guardar_libro())
        self.cancel_button.clicked.connect(lambda: self.close())

    def guardar_libro(self):
        values = (self.campo1.text(),self.campo2.text(),self.campo3.text(),self.campo4.text(),self.campo5.value())
        db.execute_query('INSERT INTO libros(titulo,autor,editorial,genero,copias_disp) VALUES (%s,%s,%s,%s,%s)',values)
        self.close()

class formulario_prestamo(QWidget):
    def __init__(self, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        
        # Campos del formulario
        self.campo1 = QDateEdit()
        self.campo1.setCalendarPopup(True)
        self.campo1.setDate(QDate.currentDate())
        self.campo2 = QDateEdit()
        self.campo2.setCalendarPopup(True)
        self.campo3 = QComboBox()
        for x in db.execute_query('SELECT estado FROM estados_prestamos'):
            self.campo3.addItem(x[0])
        self.campo4 = QSpinBox()
        self.campo4.setMinimum(1)
        self.campo4.setMaximum((db.execute_query('SELECT COUNT(*) FROM libros'))[0][0])
        self.campo5 = QSpinBox()
        self.campo5.setMinimum(1)
        self.campo5.setMaximum((db.execute_query('SELECT COUNT(*) FROM usuarios'))[0][0])

        # Añadir campos al layout del formulario
        self.form_layout.addRow("Fecha Inicio :", self.campo1)
        self.form_layout.addRow("Fecha Fin :", self.campo2)
        self.form_layout.addRow("Estado :", self.campo3)
        self.form_layout.addRow("ID Libro :", self.campo4)
        self.form_layout.addRow("ID user :", self.campo5)
        
        # Añadir el layout de formulario al layout principal
        self.main_layout.addLayout(self.form_layout)

        # Botones de acción
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        # Añadir botones al layout de botones
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Añadir el layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)
        self.save_button.clicked.connect(lambda: self.guardar_prestamo())
        self.cancel_button.clicked.connect(lambda: self.close())

    def guardar_prestamo(self):
        if self.campo3.currentText() == 'activo':
            estado = 1
        elif self.campo3.currentText() == 'finalizado':
            estado = 2
        else:
            estado = 3
        values = (self.campo1.date().toPyDate(),self.campo2.date().toPyDate(),estado,self.campo4.value(),self.campo5.value())
        db.execute_query('INSERT INTO prestamos (fecha_inicio,fecha_devolucion,estados_prestamos_id,libros_id,usuarios_id) VALUES (%s,%s,%s,%s,%s)',values)
        self.close()
    
class formulario_reserva(QWidget):
    def __init__(self, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        
        # Campos del formulario
        self.campo1 = QDateEdit()
        self.campo1.setDate(QDate.currentDate())
        self.campo1.setCalendarPopup(True)
        self.campo2 = QComboBox()
        for x in db.execute_query('SELECT estado FROM estados_reservas'):
            self.campo2.addItem(x[0])
        self.campo3 = QSpinBox()
        self.campo3.setMinimum(1)
        self.campo3.setMaximum((db.execute_query("SELECT COUNT(*) FROM libros"))[0][0])
        self.campo4 = QSpinBox()
        self.campo4.setMinimum(1)
        self.campo4.setMaximum((db.execute_query("SELECT COUNT(*) FROM usuarios"))[0][0])
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Fecha Reserva :", self.campo1)
        self.form_layout.addRow("Estado:", self.campo2)
        self.form_layout.addRow("ID libro:", self.campo3)
        self.form_layout.addRow("ID usuario:", self.campo4)
        
        # Añadir el layout de formulario al layout principal
        self.main_layout.addLayout(self.form_layout)

        # Botones de acción
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        # Añadir botones al layout de botones
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        # Añadir el layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)
        self.save_button.clicked.connect(lambda: self.guardar_reserva())
        self.cancel_button.clicked.connect(lambda: self.close())
        
    def guardar_reserva(self):
        estado = self.campo2.currentText()
        if estado == "en espera":
            estado = 1
        elif estado == "cumplida":
            estado = 2
        else:
            estado = 3
        values=(self.campo1.date().toPyDate(),estado,self.campo3.value(),self.campo4.value())
        db.execute_query("INSERT INTO reservas (fecha_solicitud,estados_reservas_id,libros_id,usuarios_id) VALUES (%s,%s,%s,%s)",values)
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar el archivo de estilo
    with open("estilo_biblioteca.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
