# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'libros.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_ventanaLibros(object):
    def setupUi(self, ventanaLibros):
        if not ventanaLibros.objectName():
            ventanaLibros.setObjectName(u"ventanaLibros")
        ventanaLibros.resize(1266, 584)
        self.centralwidget = QWidget(ventanaLibros)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(470, 0, 211, 81))
        self.tablaLibros = QTableWidget(self.centralwidget)
        self.tablaLibros.setObjectName(u"tablaLibros")
        self.tablaLibros.setGeometry(QRect(280, 80, 501, 391))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 81, 31))
        self.titulo = QLineEdit(self.centralwidget)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setGeometry(QRect(10, 100, 231, 20))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 140, 81, 31))
        self.autor = QLineEdit(self.centralwidget)
        self.autor.setObjectName(u"autor")
        self.autor.setGeometry(QRect(10, 170, 231, 20))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 210, 81, 31))
        self.cmbGenero = QComboBox(self.centralwidget)
        self.cmbGenero.setObjectName(u"cmbGenero")
        self.cmbGenero.setGeometry(QRect(10, 240, 231, 22))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 280, 161, 31))
        self.spinBoxAnio = QSpinBox(self.centralwidget)
        self.spinBoxAnio.setObjectName(u"spinBoxAnio")
        self.spinBoxAnio.setGeometry(QRect(10, 310, 231, 22))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 350, 81, 31))
        self.editorial = QLineEdit(self.centralwidget)
        self.editorial.setObjectName(u"editorial")
        self.editorial.setGeometry(QRect(10, 380, 231, 20))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 420, 151, 31))
        self.spinBoxCopias = QSpinBox(self.centralwidget)
        self.spinBoxCopias.setObjectName(u"spinBoxCopias")
        self.spinBoxCopias.setGeometry(QRect(10, 450, 231, 22))
        self.btnModificar = QPushButton(self.centralwidget)
        self.btnModificar.setObjectName(u"btnModificar")
        self.btnModificar.setGeometry(QRect(490, 480, 75, 23))
        self.btnAgregar = QPushButton(self.centralwidget)
        self.btnAgregar.setObjectName(u"btnAgregar")
        self.btnAgregar.setGeometry(QRect(290, 480, 75, 23))
        self.btnEliminar = QPushButton(self.centralwidget)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setGeometry(QRect(690, 480, 75, 23))
        self.btnEstadisticas = QPushButton(self.centralwidget)
        self.btnEstadisticas.setObjectName(u"btnEstadisticas")
        self.btnEstadisticas.setGeometry(QRect(860, 480, 75, 23))
        self.btnActualizar = QPushButton(self.centralwidget)
        self.btnActualizar.setObjectName(u"btnActualizar")
        self.btnActualizar.setGeometry(QRect(1110, 480, 75, 23))
        self.tablaTop5 = QTableWidget(self.centralwidget)
        self.tablaTop5.setObjectName(u"tablaTop5")
        self.tablaTop5.setGeometry(QRect(830, 80, 391, 151))
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(990, 10, 211, 81))
        self.tablaLibrosGeneros = QTableWidget(self.centralwidget)
        self.tablaLibrosGeneros.setObjectName(u"tablaLibrosGeneros")
        self.tablaLibrosGeneros.setGeometry(QRect(830, 280, 391, 191))
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(930, 220, 211, 81))
        ventanaLibros.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ventanaLibros)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1266, 21))
        ventanaLibros.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ventanaLibros)
        self.statusbar.setObjectName(u"statusbar")
        ventanaLibros.setStatusBar(self.statusbar)

        self.retranslateUi(ventanaLibros)

        QMetaObject.connectSlotsByName(ventanaLibros)
    # setupUi

    def retranslateUi(self, ventanaLibros):
        ventanaLibros.setWindowTitle(QCoreApplication.translate("ventanaLibros", u"ventanaLibros", None))
        self.label.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">LIBROS</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">T\u00edtulo:</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">Autor:</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">G\u00e9nero:</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">A\u00f1o de publicaci\u00f3n:</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">Editorial:</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:12pt;\">Copias disponibles:</span></p></body></html>", None))
        self.btnModificar.setText(QCoreApplication.translate("ventanaLibros", u"Modificar", None))
        self.btnAgregar.setText(QCoreApplication.translate("ventanaLibros", u"Agregar", None))
        self.btnEliminar.setText(QCoreApplication.translate("ventanaLibros", u"Eliminar", None))
        self.btnEstadisticas.setText(QCoreApplication.translate("ventanaLibros", u"Estad\u00edsticas", None))
        self.btnActualizar.setText(QCoreApplication.translate("ventanaLibros", u"Actualizar", None))
        self.label_8.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">TOP 5</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("ventanaLibros", u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Libros por g\u00e9nero</span></p></body></html>", None))
    # retranslateUi

