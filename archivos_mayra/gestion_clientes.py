from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QDate
import mysql.connector
from db_connection import get_db_connection

class VentanaCliente(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Proyecto_Biblioteca/Archivos Ui/VentanaCliente.ui", self)

        self.btnregistrar.clicked.connect(self.registrar_cliente)
        self.btnguardar.clicked.connect(self.guardar_cliente)
        self.btnmodificar.clicked.connect(self.modificar_cliente)
        self.btneliminar.clicked.connect(self.eliminar_cliente)
        self.btnsalir.clicked.connect(self.close)

        self.tableclientes.setColumnCount(7)
        self.tableclientes.setHorizontalHeaderLabels(["ID Cliente", "Nombre", "Apellido", "Documento", "Dirección", "Teléfono", "Fecha Nacimiento"])
        
        self.tableclientes.itemSelectionChanged.connect(self.mostrar_detalles_cliente)

        self.cargar_clientes()

    def cargar_clientes(self):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        consulta = "SELECT id_cliente, nombre, apellido, documento, direccion, telefono, fecha_nacimiento FROM clientes"
        cursor.execute(consulta)
        filas = cursor.fetchall()
        self.tableclientes.setRowCount(len(filas))

        for num_fila, datos_fila in enumerate(filas):
            for num_columna, dato in enumerate(datos_fila):
                self.tableclientes.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

        cursor.close()
        conexion.close()

    def registrar_cliente(self):
        nombre = self.txtnombre.text()
        apellido = self.txtapellido.text()
        documento = self.txtdocumento.text()
        direccion = self.txtdireccion.text()
        telefono = self.txttelefono.text()
        fecha_nacimiento = self.nacimiento.date().toString("yyyy-MM-dd")

        if not all([nombre, apellido, documento, direccion, telefono]):
            QMessageBox.warning(self, "Advertencia", "Debe ingresar todos los datos.")
            return

        conexion = get_db_connection()
        cursor = conexion.cursor()

        try:
            consulta = """INSERT INTO clientes (nombre, apellido, documento, direccion, telefono, fecha_nacimiento, fecha_registro)
                       VALUES (%s, %s, %s, %s, %s, %s, NOW())"""
            cursor.execute(consulta, (nombre, apellido, documento, direccion, telefono, fecha_nacimiento))
            conexion.commit()
            QMessageBox.information(self, "Registro exitoso", "Cliente registrado con éxito.")
            self.cargar_clientes()
            self.limpiar_campos()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el cliente: {e}")

        finally:
            cursor.close()
            conexion.close()

    def guardar_cliente(self):
        fila_seleccionada = self.tableclientes.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para guardar cambios.")
            return

        id_cliente = int(self.tableclientes.item(fila_seleccionada, 0).text())
        nombre = self.txtnombre.text()
        apellido = self.txtapellido.text()
        documento = self.txtdocumento.text()
        direccion = self.txtdireccion.text()
        telefono = self.txttelefono.text()
        fecha_nacimiento = self.nacimiento.date().toString("yyyy-MM-dd")

        if not all([nombre, apellido, documento, direccion, telefono]):
            QMessageBox.warning(self, "Advertencia", "Debe ingresar todos los datos.")
            return

        conexion = get_db_connection()
        cursor = conexion.cursor()

        try:
            consulta = """UPDATE clientes
                       SET nombre = %s, apellido = %s, documento = %s, direccion = %s, telefono = %s, fecha_nacimiento = %s
                       WHERE id_cliente = %s"""
            cursor.execute(consulta, (nombre, apellido, documento, direccion, telefono, fecha_nacimiento, id_cliente))
            conexion.commit()
            QMessageBox.information(self, "Actualización exitosa", "Cliente actualizado con éxito.")
            self.cargar_clientes()
            self.limpiar_campos()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el cliente: {e}")

        finally:
            cursor.close()
            conexion.close()

    def modificar_cliente(self):
        fila_seleccionada = self.tableclientes.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para modificar.")
            return

        self.txtnombre.setText(self.tableclientes.item(fila_seleccionada, 1).text())
        self.txtapellido.setText(self.tableclientes.item(fila_seleccionada, 2).text())
        self.txtdocumento.setText(self.tableclientes.item(fila_seleccionada, 3).text())
        self.txtdireccion.setText(self.tableclientes.item(fila_seleccionada, 4).text())
        self.txttelefono.setText(self.tableclientes.item(fila_seleccionada, 5).text())
        fecha_nacimiento_str = self.tableclientes.item(fila_seleccionada, 6).text()
        fecha_nacimiento = QDate.fromString(fecha_nacimiento_str, "yyyy-MM-dd")
        self.nacimiento.setDate(fecha_nacimiento)

    def eliminar_cliente(self):
        fila_seleccionada = self.tableclientes.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar.")
            return

        id_cliente = int(self.tableclientes.item(fila_seleccionada, 0).text())
        
        confirmacion = QMessageBox.question(self, "Confirmación", "¿Está seguro de que desea eliminar este cliente?",
                                            QMessageBox.Yes | QMessageBox.No)
        
        if confirmacion == QMessageBox.Yes:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            
            try:
                consulta = "DELETE FROM clientes WHERE id_cliente = %s"
                cursor.execute(consulta, (id_cliente,))
                conexion.commit()
                QMessageBox.information(self, "Eliminación exitosa", "Cliente eliminado con éxito.")
                self.cargar_clientes()
                self.limpiar_campos()

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el cliente: {e}")

            finally:
                cursor.close()
                conexion.close()

    def limpiar_campos(self):
        self.txtnombre.clear()
        self.txtapellido.clear()
        self.txtdocumento.clear()
        self.txtdireccion.clear()
        self.txttelefono.clear()
        self.nacimiento.setDate(QDate.currentDate())

    def mostrar_detalles_cliente(self):
        fila_seleccionada = self.tableclientes.currentRow()
        if fila_seleccionada == -1:
            return

        id_cliente = int(self.tableclientes.item(fila_seleccionada, 0).text())

        conexion = get_db_connection()
        cursor = conexion.cursor()
        try:
            consulta_prestamos = """
                SELECT p.id_prestamo, p.fecha_inicio, p.fecha_devolucion, l.titulo 
                FROM prestamos p 
                JOIN libros l ON p.id_libro = l.id_libro 
                WHERE p.id_cliente = %s
            """
            cursor.execute(consulta_prestamos, (id_cliente,))
            prestamos = cursor.fetchall()
            self.tableprestamos.setRowCount(len(prestamos))
            self.tableprestamos.setColumnCount(4)
            self.tableprestamos.setHorizontalHeaderLabels(["ID Préstamo", "Fecha Inicio", "Fecha Devolución", "Libro"])

            for num_fila, datos_fila in enumerate(prestamos):
                for num_columna, dato in enumerate(datos_fila):
                    self.tableprestamos.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

            consulta_reservas = """
                SELECT r.id_reserva, r.fecha_solicitud, r.id_estado_res, l.titulo 
                FROM reservas r 
                JOIN libros l ON r.id_libro = l.id_libro 
                WHERE r.id_cliente = %s
            """
            cursor.execute(consulta_reservas, (id_cliente,))
            reservas = cursor.fetchall()
            self.tablereservas.setRowCount(len(reservas))
            self.tablereservas.setColumnCount(4)
            self.tablereservas.setHorizontalHeaderLabels(["ID Reserva", "Fecha Solicitud", "Estado", "Libro"])

            for num_fila, datos_fila in enumerate(reservas):
                for num_columna, dato in enumerate(datos_fila):
                    self.tablereservas.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los detalles del cliente: {e}")

        finally:
            cursor.close()
            conexion.close()
