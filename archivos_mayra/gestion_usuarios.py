from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from db_connection import get_db_connection
import mysql.connector

class VentanaUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Proyecto_Biblioteca/Archivos Ui/VentanaUsuario.ui", self)
         
        self.btnregistrarU.clicked.connect(self.registrar_usuario)
        self.btnguardarU.clicked.connect(self.guardar_usuario)
        self.btnmodificarU.clicked.connect(self.modificar_usuario)
        self.btneliminarU.clicked.connect(self.eliminar_usuario)
        self.btnsalir.clicked.connect(self.close) 

        self.tableusuarios.setColumnCount(6)
        self.tableusuarios.setHorizontalHeaderLabels(["ID Usuario", "Nombre", "Contraseña", "Fecha Creación", "Fecha Modificación", "Última Vez"])

        self.cargar_usuarios()

    def cargar_usuarios(self):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        consulta = "SELECT id_usuario, nombre, password, fecha_creacion, fecha_modificacion, ult_vez FROM usuarios"
        cursor.execute(consulta)
        filas = cursor.fetchall()
        self.tableusuarios.setRowCount(len(filas))

        for num_fila, fila_datos in enumerate(filas):
            for num_columna, dato in enumerate(fila_datos):
                self.tableusuarios.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

        self.tableusuarios.clearSelection()

        cursor.close()
        conexion.close()

    def limpiar_campos(self):
        self.txtnombre.clear()
        self.txtcontrasenia.clear()

    def registrar_usuario(self):
        nombre = self.txtnombre.text()
        contrasena = self.txtcontrasenia.text()
        
        if not nombre or not contrasena:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar todos los datos.")
            return

        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        try:
            consulta = "INSERT INTO usuarios (nombre, password, fecha_creacion) VALUES (%s, %s, NOW())"
            cursor.execute(consulta, (nombre, contrasena))
            conexion.commit()
            QMessageBox.information(self, "Registro exitoso", "Usuario registrado con éxito.")
            self.cargar_usuarios()
            self.limpiar_campos()  

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el usuario: {e}")
        
        finally:
            cursor.close()
            conexion.close()

    def guardar_usuario(self):
        fila_seleccionada = self.tableusuarios.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un usuario para guardar cambios.")
            return
        
        id_usuario = int(self.tableusuarios.item(fila_seleccionada, 0).text())
        nombre = self.txtnombre.text()
        contrasena = self.txtcontrasenia.text()
        
        if not nombre or not contrasena:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar todos los datos.")
            return

        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        try:
            consulta = "UPDATE usuarios SET nombre = %s, password = %s, fecha_modificacion = NOW() WHERE id_usuario = %s"
            cursor.execute(consulta, (nombre, contrasena, id_usuario))
            conexion.commit()
            QMessageBox.information(self, "Actualización exitosa", "Usuario actualizado con éxito.")
            self.cargar_usuarios()
            self.limpiar_campos()  

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el usuario: {e}")
        
        finally:
            cursor.close()
            conexion.close()

    def modificar_usuario(self):
        items_seleccionados = self.tableusuarios.selectedItems()
        if not items_seleccionados:
            QMessageBox.warning(self, "Advertencia", "Seleccione un usuario para modificar.")
            return

        fila_seleccionada = self.tableusuarios.currentRow()
        id_usuario = int(self.tableusuarios.item(fila_seleccionada, 0).text())
        self.txtnombre.setText(self.tableusuarios.item(fila_seleccionada, 1).text())
        self.txtcontrasenia.setText(self.tableusuarios.item(fila_seleccionada, 2).text())

    def eliminar_usuario(self):
        items_seleccionados = self.tableusuarios.selectedItems()
        if not items_seleccionados:
            QMessageBox.warning(self, "Advertencia", "Seleccione un usuario para eliminar.")
            return

        fila_seleccionada = self.tableusuarios.currentRow()
        id_usuario = int(self.tableusuarios.item(fila_seleccionada, 0).text())
    
        confirmacion = QMessageBox.question(self, "Confirmación", "¿Está seguro de que desea eliminar este usuario?",
                                            QMessageBox.Yes | QMessageBox.No)
    
        if confirmacion == QMessageBox.Yes:
            conexion = get_db_connection()
            cursor = conexion.cursor()
        
            try:
                consulta = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(consulta, (id_usuario,))
                conexion.commit()
                QMessageBox.information(self, "Eliminación exitosa", "Usuario eliminado con éxito.")
                self.cargar_usuarios()
                self.limpiar_campos()  

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario: {e}")
        
            finally:
                cursor.close()
                conexion.close()
