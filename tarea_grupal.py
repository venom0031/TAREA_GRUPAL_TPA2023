import math
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QFormLayout, QLineEdit


class AplicacionComparacionObjetos(QMainWindow):
    def __init__(self):
        super().__init__()

        self.objeto_izquierda = MiObjeto()
        self.objeto_derecha = MiObjeto()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Comparador de Objetos")
        self.setGeometry(100, 100, 400, 300)

        widget_principal = QWidget(self)
        self.setCentralWidget(widget_principal)

        layout_principal = QVBoxLayout()
        widget_principal.setLayout(layout_principal)

        etiqueta_bienvenida = QLabel("Bienvenido al Comparador de Objetos")
        layout_principal.addWidget(etiqueta_bienvenida)

        etiqueta_instrucciones = QLabel("Ingrese los datos de ambos objetos y presione 'Comparar'")
        layout_principal.addWidget(etiqueta_instrucciones)

        panel_comparacion = QWidget()
        layout_comparacion = QHBoxLayout()
        panel_comparacion.setLayout(layout_comparacion)
        layout_principal.addWidget(panel_comparacion)

        self.visualizacion_objeto_izquierda = VisualizacionObjeto(self.objeto_izquierda)
        layout_comparacion.addWidget(self.visualizacion_objeto_izquierda)

        etiqueta_comparacion = QLabel()
        layout_comparacion.addWidget(etiqueta_comparacion)

        self.visualizacion_objeto_derecha = VisualizacionObjeto(self.objeto_derecha)
        layout_comparacion.addWidget(self.visualizacion_objeto_derecha)

        boton_comparar = QPushButton("Comparar")
        boton_comparar.clicked.connect(self.comparar_objetos)
        layout_principal.addWidget(boton_comparar)

    def mostrar_dialogo_actualizacion(self):
        dialogo = DialogoActualizacion(self, self.objeto_izquierda, self.objeto_derecha)
        dialogo.exec_()

        # Actualizar la visualización de los objetos después de cerrar el diálogo
        self.visualizacion_objeto_izquierda.actualizar_visualizacion()
        self.visualizacion_objeto_derecha.actualizar_visualizacion()

    def comparar_objetos(self):
        if self.objeto_izquierda.area > self.objeto_derecha.area:
            resultado_comparacion = ">"
        elif self.objeto_izquierda.area < self.objeto_derecha.area:
            resultado_comparacion = "<"
        else:
            resultado_comparacion = "="

        self.visualizacion_objeto_derecha.actualizar_etiqueta_comparacion(resultado_comparacion)


class VisualizacionObjeto(QWidget):
    def __init__(self, objeto):
        super().__init__()

        self.objeto = objeto

        layout = QVBoxLayout()
        self.setLayout(layout)

        etiqueta_objeto = QLabel("Objeto")
        layout.addWidget(etiqueta_objeto)

        self.etiqueta_datos = QLabel()
        layout.addWidget(self.etiqueta_datos)

        boton_actualizar = QPushButton("Agregar Datos")
        boton_actualizar.clicked.connect(self.mostrar_dialogo_actualizacion)
        layout.addWidget(boton_actualizar)

    def actualizar_visualizacion(self):
        self.etiqueta_datos.setText(str(self.objeto))

    def mostrar_dialogo_actualizacion(self):
        dialogo = DialogoActualizacion(self.objeto)
        dialogo.exec_()
        self.actualizar_visualizacion()


class DialogoActualizacion(QDialog):
    def __init__(self, objeto):
        super().__init__()

        self.objeto = objeto

        self.setWindowTitle("Actualizar Datos")
        self.setModal(True)

        layout = QFormLayout()
        self.setLayout(layout)

        self.etiqueta_lado_a = QLabel("Lado A:")
        self.campo_lado_a = QLineEdit()
        layout.addRow(self.etiqueta_lado_a, self.campo_lado_a)

        self.etiqueta_lado_b = QLabel("Lado B:")
        self.campo_lado_b = QLineEdit()
        layout.addRow(self.etiqueta_lado_b, self.campo_lado_b)

        self.etiqueta_lado_c = QLabel("Lado C:")
        self.campo_lado_c = QLineEdit()
        layout.addRow(self.etiqueta_lado_c, self.campo_lado_c)

        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(self.guardar_datos)
        layout.addWidget(boton_guardar)

    def guardar_datos(self):
        lado_a = self.campo_lado_a.text()
        lado_b = self.campo_lado_b.text()
        lado_c = self.campo_lado_c.text()

        self.objeto.establecer_lados(lado_a, lado_b, lado_c)
        self.accept()

class MiObjeto:
    def __init__(self):
        self.lado_a = None
        self.lado_b = None
        self.lado_c = None
        self.altura = None
        self.area = None

    def establecer_lados(self, lado_a, lado_b, lado_c):
        self.lado_a = float(lado_a)
        self.lado_b = float(lado_b)
        self.lado_c = float(lado_c)

        self.calcular_altura()
        self.calcular_area()

    def calcular_altura(self):
        # Fórmula de la altura del triángulo utilizando razones trigonométricas: 1/2 * a * b * sen(c)
        if self.lado_a is not None and self.lado_b is not None and self.lado_c is not None:
            radianes = math.radians(self.lado_c)
            self.altura = (1/2) * self.lado_a * self.lado_b * math.sin(radianes)
        else:
            self.altura = 0

    def calcular_area(self):
        # Fórmula del área del triángulo: base por altura sobre 2
        if self.lado_a is not None and self.altura is not None:
            self.area = (self.lado_a * self.altura) / 2
        else:
            self.area = 0

    def __str__(self):
        return f"Lado A: {self.lado_a}\nLado B: {self.lado_b}\nLado C: {self.lado_c}\nAltura: {self.altura}\nÁrea: {self.area}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AplicacionComparacionObjetos()
    ventana.show()
    sys.exit(app.exec_())
