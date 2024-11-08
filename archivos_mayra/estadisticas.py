from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from db_connection import get_db_connection

class VentanaEstadisticas(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Proyecto_Biblioteca/Archivos Ui/VentanaEstadísticas.ui", self)

        self.btnactualizar.clicked.connect(self.cargar_estadistcas)
        self.tabletop5.setColumnCount(3)
        self.tabletop5.setHorizontalHeaderLabels(["Nombre", "Apellido", "Total Préstamos"])

        self.cargar_estadistcas()

    def cargar_estadistcas(self):
        conexion = get_db_connection()
        if not conexion:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conexion.cursor()
            consulta_total_clientes = "SELECT COUNT(*) FROM clientes"
            cursor.execute(consulta_total_clientes)
            total_clientes = cursor.fetchone()
            if total_clientes:
                self.labeltotalclientes.setText(str(total_clientes[0]))
            else:
                self.labeltotalclientes.setText("0")

            consulta_top_clientes = """
                SELECT c.nombre, c.apellido, COUNT(p.id_prestamo) AS total_prestamos
                FROM clientes c
                JOIN prestamos p ON c.id_cliente = p.id_cliente
                GROUP BY c.id_cliente
                ORDER BY total_prestamos DESC
                LIMIT 5
            """
            cursor.execute(consulta_top_clientes)
            top_clientes = cursor.fetchall()

            self.tabletop5.setRowCount(len(top_clientes))
            for num_fila, datos_fila in enumerate(top_clientes):
                for num_columna, dato in enumerate(datos_fila):
                    self.tabletop5.setItem(num_fila, num_columna, QTableWidgetItem(str(dato)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las estadísticas: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
