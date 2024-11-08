import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt, QDate
import mysql.connector
from ui_libros import Ui_ventanaLibros
from conexion import obtener_conexion

class VentanaLibros(QMainWindow, Ui_ventanaLibros):
    def __init__(self):
        super(VentanaLibros, self).__init__()
        self.setupUi(self)

        self.conn = obtener_conexion()
        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            QMessageBox.critical(self, "Error", "No se pudo establecer la conexión con la base de datos.")
            sys.exit(1)

        self.spinBoxAnio.setRange(1699, datetime.now().year)
        self.spinBoxCopias.setRange(0, 9999)
        self.cmbGenero.addItems(["Misterio", "Fantasía", "Romance", "Thriller/Suspenso", "Distopía", "Ciencia Ficción"])

        self.filaEditar = None

        self.btnAgregar.clicked.connect(self.registrarLibro)
        self.btnModificar.clicked.connect(self.modificarLibro)
        self.btnEliminar.clicked.connect(self.eliminarLibro)
        self.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)
        self.btnActualizar.clicked.connect(self.mostrar_estadisticas)

        self.tablaLibros.setColumnCount(6)
        self.tablaLibrosGeneros.setColumnCount(2)
        self.tablaTop5.setColumnCount(2)
        self.tablaTop5.setHorizontalHeaderLabels(["Título", "Préstamos"])

        self.tablaLibros.setHorizontalHeaderLabels(["Título", "Autor", "Género", "Año publicación", "Editorial", "Copias disponibles"])
        self.tablaLibrosGeneros.setHorizontalHeaderLabels(["Género", "Cantidad"])
        self.tablaLibros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaLibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaLibros.selectionModel().selectionChanged.connect(self.actualizarEstadoBotones)
        self.actualizarEstadoBotones()
        self.cargarLibros()

    def cargarLibros(self):
        self.tablaLibros.setRowCount(0)
        query = "SELECT titulo, autor, genero, anio_publicacion, editorial, copias_disp, id FROM libros"
        self.cursor.execute(query)
        for (titulo, autor, genero, anio_publicacion, editorial, copias_disp, id) in self.cursor:
            rowPosition = self.tablaLibros.rowCount()
            self.tablaLibros.insertRow(rowPosition)
            self.tablaLibros.setItem(rowPosition, 0, QTableWidgetItem(titulo))
            self.tablaLibros.setItem(rowPosition, 1, QTableWidgetItem(autor))
            self.tablaLibros.setItem(rowPosition, 2, QTableWidgetItem(genero))
            self.tablaLibros.setItem(rowPosition, 3, QTableWidgetItem(str(anio_publicacion)))
            self.tablaLibros.setItem(rowPosition, 4, QTableWidgetItem(editorial))
            self.tablaLibros.setItem(rowPosition, 5, QTableWidgetItem(str(copias_disp)))
            self.tablaLibros.item(rowPosition, 0).setData(Qt.UserRole, id)

    def actualizarEstadoBotones(self):
        hayFilaSeleccionada = self.tablaLibros.selectionModel().hasSelection()
        self.btnModificar.setEnabled(hayFilaSeleccionada)
        self.btnEliminar.setEnabled(hayFilaSeleccionada)

    def registrarLibro(self):
        tituloLibro = self.titulo.text()
        autorLibro = self.autor.text()
        generoLibros = self.cmbGenero.currentText()
        anioPublicacionLibro = self.spinBoxAnio.value()
        editorialLibro = self.editorial.text()
        copiasLibros = self.spinBoxCopias.value()

        if tituloLibro and autorLibro:
            try:
                if self.filaEditar is not None:
                    idLibro = self.tablaLibros.item(self.filaEditar, 0).data(Qt.UserRole)
                    query = ("UPDATE libros SET titulo = %s, autor = %s, genero = %s, "
                            "anio_publicacion = %s, editorial = %s, copias_disp = %s "
                            "WHERE id = %s")
                    values = (tituloLibro, autorLibro, generoLibros, anioPublicacionLibro, editorialLibro, copiasLibros, idLibro)
                    self.cursor.execute(query, values)
                    self.conn.commit()

                    self.tablaLibros.setItem(self.filaEditar, 0, QTableWidgetItem(tituloLibro)) 
                    self.tablaLibros.setItem(self.filaEditar, 1, QTableWidgetItem(autorLibro))
                    self.tablaLibros.setItem(self.filaEditar, 2, QTableWidgetItem(generoLibros))
                    self.tablaLibros.setItem(self.filaEditar, 3, QTableWidgetItem(str(anioPublicacionLibro)))
                    self.tablaLibros.setItem(self.filaEditar, 4, QTableWidgetItem(editorialLibro))
                    self.tablaLibros.setItem(self.filaEditar, 5, QTableWidgetItem(str(copiasLibros)))
                    self.filaEditar = None
                else:
                    query = ("INSERT INTO libros (titulo, autor, genero, anio_publicacion, editorial, copias_disp) "
                            "VALUES (%s, %s, %s, %s, %s, %s)")
                    values = (tituloLibro, autorLibro, generoLibros, anioPublicacionLibro, editorialLibro, copiasLibros)

                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.cargarLibros()
                self.limpiar_campos()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Error", f"No se pudo agregar o modificar el libro: {err}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el título y el autor.")


    def limpiar_campos(self):
        self.titulo.clear()
        self.autor.clear()
        self.cmbGenero.setCurrentIndex(0)
        self.spinBoxAnio.setValue(1)
        self.editorial.clear()
        self.spinBoxCopias.setValue(1)
        self.filaEditar = None

    def eliminarLibro(self):
        filaSeleccionada = self.tablaLibros.currentRow()
        if filaSeleccionada >= 0:
            idLibro = self.tablaLibros.item(filaSeleccionada, 0).data(Qt.UserRole)
            try:
                query = "DELETE FROM libros WHERE id = %s"
                self.cursor.execute(query, (idLibro,))
                self.conn.commit()
                self.tablaLibros.removeRow(filaSeleccionada)
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el libro: {err}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione una fila para eliminar.")

    def modificarLibro(self):
        filaSeleccionada = self.tablaLibros.currentRow()
        if filaSeleccionada >= 0:
            self.titulo.setText(self.tablaLibros.item(filaSeleccionada, 0).text())
            self.autor.setText(self.tablaLibros.item(filaSeleccionada, 1).text())
            self.cmbGenero.setCurrentText(self.tablaLibros.item(filaSeleccionada, 2).text())
            self.spinBoxAnio.setValue(int(self.tablaLibros.item(filaSeleccionada, 3).text()))
            self.editorial.setText(self.tablaLibros.item(filaSeleccionada, 4).text())
            self.spinBoxCopias.setValue(int(self.tablaLibros.item(filaSeleccionada, 5).text()))
            self.filaEditar = filaSeleccionada
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione una fila para modificar.")

    def mostrar_estadisticas(self):
        self.cargar_top_libros_prestados()
        self.cargar_libros_por_genero()

    def cargar_top_libros_prestados(self):
        query = """
            SELECT libros.titulo, COUNT(prestamos.libros_id) AS prestamos
            FROM prestamos
            JOIN libros ON prestamos.libros_id = libros.id
            GROUP BY libros.titulo
            ORDER BY prestamos DESC
            LIMIT 5
        """
        self.cursor.execute(query)
        self.tablaTop5.setRowCount(0)
        for titulo, prestamos in self.cursor:
            print(f"Libro: {titulo}, Prestamos: {prestamos}")
            posicionFila = self.tablaTop5.rowCount()
            self.tablaTop5.insertRow(posicionFila)
            self.tablaTop5.setItem(posicionFila, 0, QTableWidgetItem(titulo))
            self.tablaTop5.setItem(posicionFila, 1, QTableWidgetItem(str(prestamos)))

    def cargar_libros_por_genero(self):
        query = ("SELECT genero, COUNT(*) AS cantidad "
                "FROM libros GROUP BY genero")
        self.cursor.execute(query)
        self.tablaLibrosGeneros.setRowCount(0)
        for genero, cantidad in self.cursor:
            posicionFila = self.tablaLibrosGeneros.rowCount()
            self.tablaLibrosGeneros.insertRow(posicionFila)
            self.tablaLibrosGeneros.setItem(posicionFila, 0, QTableWidgetItem(genero))
            self.tablaLibrosGeneros.setItem(posicionFila, 1, QTableWidgetItem(str(cantidad)))


    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaLibros()
    window.show()
    sys.exit(app.exec())