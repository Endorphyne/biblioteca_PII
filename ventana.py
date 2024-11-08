import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QFormLayout, QMessageBox, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout,QSpinBox,QDateEdit,QComboBox, QDialog
from PyQt5.QtCore import Qt, QDate
from conexiones_sql import Database as db
from datetime import datetime
#conexion con la db
db = db('config.ini','biblioteca')
db.connect()

#Apartado login
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
        password = self.password_input.text()
        if db.check_user(self.username_input.text(),password):
            self.main_window = MainApp()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self,"ADVERTENCIA","Usuario y/o contraseña incorrectos",QMessageBox.Ok)


#Apartado de ventana
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
        db.close()
        event.accept()

    def create_tab(self, title, column_names):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)


        table = QTableWidget(0, len(column_names))
        table.setHorizontalHeaderLabels(column_names)
        table.setAlternatingRowColors(True)

        # Crear el layout de botones
        button_layout = QHBoxLayout()
        agregar_btn = QPushButton("Agregar")
        editar = QPushButton("Modificar")
        eliminar_btn = QPushButton("Eliminar")
        estadisticas_btn = QPushButton("Estadísticas")
        actualizar_btn = QPushButton("Actualizar Tabla")

        button_layout.addWidget(agregar_btn)
        button_layout.addWidget(editar)
        button_layout.addWidget(eliminar_btn)
        button_layout.addWidget(estadisticas_btn)
        button_layout.addWidget(actualizar_btn)

        actualizar_btn.clicked.connect(lambda: self.actualizar_tabla(table, title.lower()))

        tab_layout.addWidget(table)
        tab_layout.addLayout(button_layout)

        self.tab_widget.addTab(tab, title)

        # Cargar los datos en la tabla al crear la pestaña
        self.actualizar_tabla(table, title.lower())

        #Conexion con los metodos
        agregar_btn.clicked.connect(self.open_form)
        editar.clicked.connect(self.open_form2)
        eliminar_btn.clicked.connect(self.eliminar)
        estadisticas_btn.clicked.connect(self.open_stats)

    def eliminar(self):
        indice_pestaña = self.tab_widget.currentIndex()
        
        nombre_pestaña = self.tab_widget.tabText(indice_pestaña)

        current_tab = self.tab_widget.widget(indice_pestaña)
        tabla = current_tab.findChild(QTableWidget)

        items = tabla.selectedItems()
        if items:
            row = items[0].row()
            id = tabla.item(row,0).text()
            # Mensaje de confirmacion
            reply = QMessageBox.question(self, "PELIGRO CUIDADO",
                                         f"¿Esta seguro de que desea eliminar el elemento de id: {id} seleccionado de '{nombre_pestaña}'?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                values = (int(id),)
                db.execute_query(f"DELETE FROM `{nombre_pestaña.lower()}` WHERE id = %s",values)
                

    def open_stats(self):
        # Obtener el título de la pestaña activa
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_title = self.tab_widget.tabText(current_tab_index)
        if current_tab_title == "Clientes":
            stats = estadisticas_clientes()
        elif current_tab_title == "Libros":
            stats = estadistica_libros()
        elif current_tab_title == "Prestamos":
            stats = estadisticas_prestamos()
        elif current_tab_title == "Reservas":
            stats = estadisticas_reservas()
        else:
            QMessageBox.warning(self,"ADVERTENCIA","La tabla seleccionada no tiene estadisticas disponibles",QMessageBox.Ok)
            return None
        stats.exec_()

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

    def open_form2(self):
        # Obtener el título de la pestaña activa
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_title = self.tab_widget.tabText(current_tab_index)

        if current_tab_title == "Usuarios":
            self.form = formulario_user_mod(self,"Agregar Usuario")
            self.form.show()
        elif current_tab_title == "Clientes":
            self.form = formulario_cliente_mod(self,"Agregar Cliente")
            self.form.show()
        elif current_tab_title == "Libros":
            self.form = formulario_libro_mod(self,"Agregar Libro")
            self.form.show()
        elif current_tab_title == "Prestamos":
            self.form = formulario_prestamo_mod(self,"Agregar Préstamo")
            self.form.show()
        elif current_tab_title == "Reservas":
            self.form = formulario_reserva_mod(self,"Agregar Reserva")
            self.form.show()

    def actualizar_tabla(self, table_widget, table_name):
        """
        Actualiza el contenido del QTableWidget con los datos de la base de datos.
        """
        try:
            query = f"SELECT * FROM {table_name}" 
            resultados = db.execute_query(query)


            table_widget.setRowCount(0)

            for row_number, row_data in enumerate(resultados):
                table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except Exception as e:
            print(f"Error al actualizar la tabla {table_name}: {e}")
#Apartado estadisticas
class estadisticas_clientes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 Usuarios con Prestamos")
        self.setGeometry(200, 200, 400, 300)

        # Configurar el layout principal del popup
        layout = QVBoxLayout(self)

        # Crear tabla para mostrar los datos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Cliente_id", "Préstamos"])
        layout.addWidget(self.table_widget)
        self.cargar_tabla()

    def cargar_tabla(self):
        query = """
        SELECT u.nombre AS usuario, COUNT(p.usuarios_id) AS cantidad_prestamos
        FROM prestamos p
        JOIN usuarios u ON p.usuarios_id = u.id
        GROUP BY p.usuarios_id
        ORDER BY cantidad_prestamos DESC
        LIMIT 5;
        """
        resultados = db.execute_query(query)
        
        # Configurar el número de filas
        self.table_widget.setRowCount(len(resultados))

        # Rellenar la tabla con los resultados
        for row_number, row_data in enumerate(resultados):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


class estadistica_libros(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 5 Libros Más Prestados")
        self.setGeometry(200, 200, 400, 300)

        # Configurar el layout principal del popup
        layout = QVBoxLayout(self)

        # Crear tabla para mostrar los datos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Libro_id", "Cant_Préstamos"])
        layout.addWidget(self.table_widget)
        self.cargar_tabla()

    def cargar_tabla(self):
        # Consulta para obtener el top 5 de libros más prestados
        query = """
        SELECT p.libros_id AS libro, COUNT(p.libros_id) AS prestamos
        FROM prestamos p
        JOIN libros l ON p.libros_id = l.id
        GROUP BY p.libros_id
        ORDER BY prestamos DESC
        LIMIT 5;
        """
        resultados = db.execute_query(query)
        
        # Configurar el número de filas
        self.table_widget.setRowCount(len(resultados))

        # Rellenar la tabla con los resultados
        for row_number, row_data in enumerate(resultados):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

class estadisticas_prestamos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estadísticas de Préstamos")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout(self)

        # Crear tabla para mostrar los resultados
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Llamar a la función para cargar las estadísticas
        self.estadisticas_prestamos()
    def estadisticas_prestamos(self):
        query_activos = """
        SELECT COUNT(*) AS prestamos_activos
        FROM prestamos
        WHERE estados_prestamos_id = 1;
        """
        query_finalizados = """
        SELECT COUNT(*) AS prestamos_finalizados
        FROM prestamos
        WHERE estados_prestamos_id = 2;
        """
        query_atrasados = """
        SELECT COUNT(*) AS prestamos_atrasados
        FROM prestamos
        WHERE estados_prestamos_id = 3;
        """
        prestamos_activos = db.execute_query(query_activos)[0][0]
        prestamos_finalizados = db.execute_query(query_finalizados)[0][0]
        prestamos_atrasados = db.execute_query(query_atrasados)[0][0]

        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Estado", "Cantidad"])

        self.table_widget.setItem(0, 0, QTableWidgetItem("Activos"))
        self.table_widget.setItem(0, 1, QTableWidgetItem(str(prestamos_activos)))

        self.table_widget.setItem(1, 0, QTableWidgetItem("Finalizados"))
        self.table_widget.setItem(1, 1, QTableWidgetItem(str(prestamos_finalizados)))

        self.table_widget.setItem(2, 0, QTableWidgetItem("Atrasados"))
        self.table_widget.setItem(2, 1, QTableWidgetItem(str(prestamos_atrasados)))

        total_prestamos = prestamos_activos + prestamos_finalizados + prestamos_atrasados
        self.table_widget.setItem(3, 0, QTableWidgetItem("Total"))
        self.table_widget.setItem(3, 1, QTableWidgetItem(str(total_prestamos)))

class estadisticas_reservas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estadísticas de Reservas")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout(self)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.carga()

    def carga(self):
        query_pendientes = """
        SELECT COUNT(*) AS reservas_pendientes
        FROM reservas
        WHERE id = 1;
        """
        query_cumplidas = """
        SELECT COUNT(*) AS reservas_cumplidas
        FROM reservas
        WHERE id = 2;
        """
        query_canceladas = """
        SELECT COUNT(*) AS reservas_cumplidas
        FROM reservas
        WHERE id = 3;
        """
        reservas_pendientes = db.execute_query(query_pendientes)[0][0]
        reservas_cumplidas = db.execute_query(query_cumplidas)[0][0]
        reservas_canceladas = db.execute_query(query_canceladas)[0][0]

        self.table_widget.setRowCount(3)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Estado de la Reserva", "Cantidad"])

        self.table_widget.setItem(0, 0, QTableWidgetItem("Pendientes"))
        self.table_widget.setItem(0, 1, QTableWidgetItem(str(reservas_pendientes)))

        self.table_widget.setItem(1, 0, QTableWidgetItem("Cumplidas"))
        self.table_widget.setItem(1, 1, QTableWidgetItem(str(reservas_cumplidas)))

        self.table_widget.setItem(0, 0, QTableWidgetItem("Canceladas"))
        self.table_widget.setItem(0, 1, QTableWidgetItem(str(reservas_canceladas)))

#Apartado Formularios
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
            
            values = (self.campo1.text(),db.hashear(self.campo2.text()),datetime.now())
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
        self.campo4 = QComboBox()
        for x in db.execute_query("SELECT genero FROM generos"):
            self.campo4.addItem(x[0])
        self.campo5 = QSpinBox()
        self.campo6 = QDateEdit()
        self.campo6.setCalendarPopup(True)
        
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Titulo :", self.campo1)
        self.form_layout.addRow("Autor:", self.campo2)
        self.form_layout.addRow("Editorial:", self.campo3)
        self.form_layout.addRow("Genero :", self.campo4)
        self.form_layout.addRow("Stock :", self.campo5)
        self.form_layout.addRow("Año de publicacion :", self.campo6)
        
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
        values = (self.campo1.text(),self.campo2.text(),self.campo3.text(),self.campo4.currentIndex()+1,self.campo5.value(),self.campo6.date().toPyDate())
        db.execute_query('INSERT INTO libros(titulo,autor,editorial,id_genero,copias_disp,fecha_publicacion) VALUES (%s,%s,%s,%s,%s,%s)',values)
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

#Apartados Formularios mod
class formulario_user_mod(QWidget):
    def __init__(self,mainApp, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)
        self.main_app = mainApp#Creacion de una estancia de mainapp para acceder a las tablas
        usuarios_tab = self.main_app.tab_widget.widget(0)
        tabla = usuarios_tab.findChild(QTableWidget)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)
        if tabla:
            if isinstance(tabla, QTableWidget):
                items = tabla.selectedItems()
                row = items[0].row()
                nombre = tabla.item(row, 1).text()
                password = tabla.item(row, 2).text()
                creacion = tabla.item(row, 3).text()
                ult_mod = tabla.item(row, 4).text()
                ult_vez = tabla.item(row, 5).text()
            else:
                nombre = "Fallo"
                password = "Fallo"
                creacion = "2222-10-12"
                nombre = "Fallo"
            # Layout del formulario
            self.form_layout = QFormLayout()
            # Campos del formulario
            self.campo1 = QLineEdit(nombre)
            self.campo2 = QLineEdit(password)
            self.campo2.setEchoMode(QLineEdit.Password)
            self.campo3 = QLineEdit()
            self.campo3.setEchoMode(QLineEdit.Password)
            self.campo4 = QDateEdit()
            self.campo4.setDate(QDate.fromString(creacion,"yyyy-MM-dd"))
            self.campo4.setDisabled(True)
            self.campo4.setCalendarPopup(True)
            self.campo5 = QDateEdit()
            self.campo5.setCalendarPopup(True)
            self.campo5.setDate(QDate.fromString(ult_mod,"yyyy-MM-dd"))
            self.campo5.setDisabled(True)
            self.campo6 = QDateEdit()
            self.campo6.setDate(QDate.fromString(ult_vez,"yyyy-MM-dd"))
            self.campo6.setDisabled(True)
            self.campo6.setCalendarPopup(True)

            # Añadir campos al layout del formulario
            self.form_layout.addRow("Nombre :", self.campo1)
            self.form_layout.addRow("Contraseña:", self.campo2)
            self.form_layout.addRow("Confirmacion Contraseña:", self.campo3)
            self.form_layout.addRow("Creacion:", self.campo4)
            self.form_layout.addRow("Ultima mod:", self.campo5)
            self.form_layout.addRow("Ultima Vez:", self.campo6)
            
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
            self.save_button.clicked.connect(lambda: self.guardar_usuario(tabla,row))
            self.cancel_button.clicked.connect(lambda: self.close())
        else:
            QMessageBox.warning(self,"ERROR","Debe seleccionar un usuario de la tabla",QMessageBox.Ok)

    def comprobrar_campos(self)->bool:
        nombre = self.campo1.text()
        if len(nombre)<0 and len(nombre) >150:
            return False
        if self.campo2.text() != self.campo3.text():
            return False
        return True
        
    def guardar_usuario(self,tabla,row):
        if self.comprobrar_campos():
            id = tabla.item(row,0).text()
            values = (self.campo1.text(),self.campo2.text(),datetime.now(),self.campo6.date().toPyDate(),id)
            db.execute_query('UPDATE usuarios set nombre=%s,password=%s,fecha_modificacion=%s,ult_vez=%s WHERE id = %s',values)
            self.close()

class formulario_cliente_mod(QWidget):
    def __init__(self,mainapp, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        self.setGeometry(150, 150, 400, 300)
        self.main_app = mainapp
        clientes_tab = self.main_app.tab_widget.widget(1)
        tabla = clientes_tab.findChild(QTableWidget)
        if tabla:
            if isinstance(tabla,QTableWidget):
                items = tabla.selectedItems()
                row = items[0].row()
                nombre = tabla.item(row,1).text()
                apellido = tabla.item(row,2).text()
                documento = tabla.item(row,3).text()
                nacimiento = tabla.item(row,4).text()
                direccion = tabla.item(row,5).text()
                telefono = tabla.item(row,6).text()
                ID_usuario = tabla.item(row,8).text()
        # Campos del formulario
        self.campo1 = QLineEdit(nombre)
        self.campo2 = QLineEdit(apellido)
        self.campo3 = QLineEdit(documento)
        self.campo3.setInputMask("########")
        self.campo4 = QDateEdit()
        self.campo4.setDate(QDate.fromString(nacimiento,"yyyy-MM-dd"))
        self.campo4.setCalendarPopup(True)
        self.campo5 = QLineEdit(direccion)
        self.campo6 = QLineEdit(telefono)
        self.campo6.setInputMask("####-######")
        self.campo7 = QSpinBox()
        self.campo7.setValue(int(ID_usuario))
        self.campo7.setDisabled(True)
        
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
        self.save_button.clicked.connect(lambda: self.guardar_cliente(tabla,row))
        self.cancel_button.clicked.connect(lambda: self.close())


    def guardar_cliente(self,tabla,row):
        id = tabla.item(row,0).text()
        values = (self.campo1.text(),self.campo2.text(),self.campo3.text(),self.campo4.date().toPyDate(),self.campo5.text(),self.campo6.text(),self.campo7.value(),id)
        print(values)
        db.execute_query('UPDATE clientes SET nombre=%s, apellido=%s, documento=%s, nacimiento=%s, direccion=%s, telefono=%s,usuarios_id=%s WHERE id = %s',values)
        self.close()

class formulario_libro_mod(QWidget):
    def __init__(self,mainapp, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        self.form_layout = QFormLayout()
        self.setGeometry(150, 150, 400, 300)
        self.main_app = mainapp
        libros_tab = self.main_app.tab_widget.widget(2)
        tabla = libros_tab.findChild(QTableWidget)
        if tabla:
            if isinstance(tabla,QTableWidget):
                items = tabla.selectedItems()
                row = items[0].row()
                titulo_libro = tabla.item(row,1).text()
                autor = tabla.item(row,2).text()
                editorial = tabla.item(row,3).text()
                genero = tabla.item(row,4).text()
                stock = tabla.item(row,5).text()
                publicacion = tabla.item(row,6).text()
        # Campos del formulario
        self.campo1 = QLineEdit(titulo_libro)
        self.campo2 = QLineEdit(autor)
        self.campo3 = QLineEdit(editorial)
        self.campo4 = QComboBox()
        for x in db.execute_query('SELECT genero FROM generos'):
            self.campo4.addItem(x[0])
        self.campo4.setCurrentIndex(int(genero)-1)
        self.campo5 = QLineEdit(stock)
        self.campo5.setInputMask("######")
        self.campo6 = QDateEdit()
        self.campo6.setDate(QDate.fromString(publicacion,"yyyy-MM-dd"))
        self.campo6.setCalendarPopup(True)
        # Añadir campos al layout del formulario
        self.form_layout.addRow("Titulo :", self.campo1)
        self.form_layout.addRow("Autor:", self.campo2)
        self.form_layout.addRow("Editorial:", self.campo3)
        self.form_layout.addRow("Genero :", self.campo4)
        self.form_layout.addRow("Stock :", self.campo5)
        self.form_layout.addRow("Fecha Publicacion :", self.campo6)
        
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
        self.save_button.clicked.connect(lambda: self.guardar_libro(tabla,row))
        self.cancel_button.clicked.connect(lambda: self.close())

    def guardar_libro(self,tabla,row):
        id = tabla.item(row,0).text()
        values = (self.campo1.text(),self.campo2.text(),self.campo3.text(),self.campo4.currentIndex()+1,self.campo5.text(),self.campo6.date().toPyDate(),id)
        db.execute_query('UPDATE libros SET titulo=%s,autor=%s,editorial=%s,id_genero=%s,copias_disp=%s,fecha_publicacion=%s WHERE id=%s',values)
        self.close()

class formulario_prestamo_mod(QWidget):
    def __init__(self,mainapp, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        self.main_app = mainapp
        prestamos_tab = self.main_app.tab_widget.widget(3)
        tabla = prestamos_tab.findChild(QTableWidget)
        if tabla:
            if isinstance(tabla,QTableWidget):
                items = tabla.selectedItems()
                row = items[0].row()
                fecha_inicio = tabla.item(row,1).text()
                fecha_fin = tabla.item(row,2).text()
                estado = tabla.item(row,3).text()
                id_libro = tabla.item(row,4).text()
                id_usuario = tabla.item(row,5).text()
        # Campos del formulario
        self.campo1 = QDateEdit()
        self.campo1.setCalendarPopup(True)
        self.campo1.setDate(QDate.fromString(fecha_inicio,"yyyy-MM-dd"))
        self.campo2 = QDateEdit()
        self.campo2.setCalendarPopup(True)
        self.campo2.setDate(QDate.fromString(fecha_fin,"yyyy-MM-dd"))
        self.campo3 = QComboBox()
        for x in db.execute_query('SELECT estado FROM estados_prestamos'):
            self.campo3.addItem(x[0])
        self.campo3.setCurrentIndex(int(estado)-1)
        self.campo4 = QSpinBox()
        self.campo4.setMinimum(1)
        self.campo4.setMaximum((db.execute_query('SELECT COUNT(*) FROM libros'))[0][0])
        self.campo4.setValue(int(id_libro))
        self.campo5 = QSpinBox()
        self.campo5.setMinimum(1)
        self.campo5.setMaximum((db.execute_query('SELECT COUNT(*) FROM usuarios'))[0][0])
        self.campo5.setValue(int(id_usuario))
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
        self.save_button.clicked.connect(lambda: self.guardar_prestamo(tabla,row))
        self.cancel_button.clicked.connect(lambda: self.close())

    def guardar_prestamo(self,tabla,row):
        if self.campo3.currentText() == 'activo':
            estado = 1
        elif self.campo3.currentText() == 'finalizado':
            estado = 2
        else:
            estado = 3
        id = tabla.item(row,0).text()
        values = (self.campo1.date().toPyDate(),self.campo2.date().toPyDate(),estado,self.campo4.value(),self.campo5.value(),id)
        db.execute_query('UPDATE prestamos SET fecha_inicio=%s,fecha_devolucion=%s,estados_prestamos_id=%s,libros_id=%s,usuarios_id=%s WHERE id =%s',values)
        self.close()
    
class formulario_reserva_mod(QWidget):
    
    def __init__(self,mainapp, titulo="Formulario"):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setGeometry(150, 150, 400, 300)

        # Layout principal del formulario
        self.main_layout = QVBoxLayout(self)

        # Layout del formulario
        self.form_layout = QFormLayout()
        self.main_app = mainapp
        reservas_tab = self.main_app.tab_widget.widget(4)
        tabla = reservas_tab.findChild(QTableWidget)
        if tabla:
            if isinstance(tabla,QTableWidget):
                items = tabla.selectedItems()
                row = items[0].row()
                fecha = tabla.item(row,1).text()
                estado = tabla.item(row,2).text()
                id_libro = tabla.item(row,3).text()
                id_usuario = tabla.item(row,4).text()
        # Campos del formulario
        self.campo1 = QDateEdit()
        self.campo1.setDate(QDate.fromString(fecha,"yyyy-MM-dd"))
        self.campo1.setCalendarPopup(True)
        self.campo2 = QComboBox()
        for x in db.execute_query('SELECT estado FROM estados_reservas'):
            self.campo2.addItem(x[0])
        self.campo2.setCurrentIndex(int(estado)-1)
        self.campo3 = QSpinBox()
        self.campo3.setMinimum(1)
        self.campo3.setMaximum((db.execute_query("SELECT COUNT(*) FROM libros"))[0][0])
        self.campo3.setValue(int(id_libro))
        self.campo4 = QSpinBox()
        self.campo4.setMinimum(1)
        self.campo4.setMaximum((db.execute_query("SELECT COUNT(*) FROM usuarios"))[0][0])
        self.campo4.setValue(int(id_usuario))

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
        self.save_button.clicked.connect(lambda: self.guardar_reserva(tabla,row))
        self.cancel_button.clicked.connect(lambda: self.close())
        
    def guardar_reserva(self,tabla,row):
        estado = self.campo2.currentText()
        if estado == "en espera":
            estado = 1
        elif estado == "cumplida":
            estado = 2
        else:
            estado = 3
        id = tabla.item(row,0).text()
        values=(self.campo1.date().toPyDate(),estado,self.campo3.value(),self.campo4.value(),id)
        db.execute_query("UPDATE reservas SET fecha_solicitud=%s,estados_reservas_id=%s,libros_id=%s,usuarios_id=%s WHERE id =%s",values)
        self.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar el archivo de estilo
    with open("estilo_biblioteca.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
