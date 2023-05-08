import math
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QFormLayout, QLineEdit

# CODIGO CREADO POR HUGO FAUNDEZ Y MIGUEL VALLADARES

# Clase principal de la aplicación
class AppComparacion(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear dos objetos de la clase "formulas" para comparar
        self.objeto_izquierda = formulas()
        self.objeto_derecha = formulas()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Comparador de triangulos Δ")
        self.setGeometry(100, 100, 400, 300)

        # Configurar el widget principal y su diseño vertical
        widget_principal = QWidget(self)
        self.setCentralWidget(widget_principal)
        layout_principal = QVBoxLayout()
        widget_principal.setLayout(layout_principal)

        # Etiqueta de bienvenida
        etiqueta_bienvenida = QLabel("Bienvenido al Comparador de triangulos Δ")
        layout_principal.addWidget(etiqueta_bienvenida)

        # Etiqueta de instrucciones
        etiqueta_instrucciones = QLabel("Ingrese los datos de ambos triangulos y presione 'Comparar'")
        layout_principal.addWidget(etiqueta_instrucciones)

        # Panel de comparación con tres widgets: visualización izquierda, etiqueta de comparación, visualización derecha
        panel_comparacion = QWidget()
        layout_comparacion = QHBoxLayout()
        panel_comparacion.setLayout(layout_comparacion)
        layout_principal.addWidget(panel_comparacion)

        # Visualización del triangulo izquierdo
        self.visualizacion_objeto_izquierda = Visualizacion(self.objeto_izquierda)
        layout_comparacion.addWidget(self.visualizacion_objeto_izquierda)

        # Etiqueta de comparación
        self.etiqueta_comparacion = QLabel()
        layout_comparacion.addWidget(self.etiqueta_comparacion)

        # Visualización del triangulo derecho
        self.visualizacion_objeto_derecha = Visualizacion(self.objeto_derecha)
        layout_comparacion.addWidget(self.visualizacion_objeto_derecha)

        # Botón de comparar
        boton_comparar = QPushButton("Comparar")
        boton_comparar.clicked.connect(self.comparar_objetos)
        layout_principal.addWidget(boton_comparar)

    def mostrar_dialogo_actualizacion(self):
        # Mostrar el diálogo de actualización de datos
        dialogo = DialogoActualizacion(self, self.objeto_izquierda, self.objeto_derecha)
        dialogo.exec_()

        # Actualizar la visualización de los objetos después de cerrar
        self.visualizacion_objeto_izquierda.actualizar_visualizacion()
        self.visualizacion_objeto_derecha.actualizar_visualizacion()

    def comparar_objetos(self):
        # Comparar las áreas de los triangulos y actualizar la etiqueta de comparación
        if self.objeto_izquierda.area > self.objeto_derecha.area:
            resultado_comparacion = ">"
        elif self.objeto_izquierda.area < self.objeto_derecha.area:
            resultado_comparacion = "<"
        else:
            resultado_comparacion = "="

        self.etiqueta_comparacion.setText(resultado_comparacion)


# Widget de visualización de un objeto
class Visualizacion(QWidget):
    def __init__(self, objeto):
        super().__init__()

        self.objeto = objeto

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Etiqueta de los triangulos
        etiqueta_objeto = QLabel("Δ")
        layout.addWidget(etiqueta_objeto)

        # Etiqueta de datos del triangulo
        self.etiqueta_datos = QLabel()
        layout.addWidget(self.etiqueta_datos)

        # Botón de actualización de datos
        boton_actualizar = QPushButton("Agregar Datos")
        boton_actualizar.clicked.connect(self.mostrar_dialogo_actualizacion)
        layout.addWidget(boton_actualizar)

    def actualizar_visualizacion(self):
        # Actualizar la etiqueta de datos del triangulo
        self.etiqueta_datos.setText(str(self.objeto))

    def mostrar_dialogo_actualizacion(self):
        # Mostrar el diálogo de actualización de datos
        dialogo = DialogoActualizacion(self.objeto)
        dialogo.exec_()
        self.actualizar_visualizacion()


# Diálogo de actualización de datos de un triangulo
class DialogoActualizacion(QDialog):
    def __init__(self, objeto):
        super().__init__()

        self.objeto = objeto

        self.setWindowTitle("Actualizar Datos")
        self.setModal(True)
        layout = QFormLayout()
        self.setLayout(layout)

        # Etiquetas y campos de texto para los lados del triángulo
        self.etiqueta_lado_a = QLabel("Lado A:")
        self.campo_lado_a = QLineEdit()
        layout.addRow(self.etiqueta_lado_a, self.campo_lado_a)

        self.etiqueta_lado_b = QLabel("Lado B:")
        self.campo_lado_b = QLineEdit()
        layout.addRow(self.etiqueta_lado_b, self.campo_lado_b)

        self.etiqueta_lado_c = QLabel("Lado C:")
        self.campo_lado_c = QLineEdit()
        layout.addRow(self.etiqueta_lado_c, self.campo_lado_c)

        # Botón de guardar
        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(self.guardar_datos)
        layout.addWidget(boton_guardar)

    def guardar_datos(self):
        # Obtener los valores de los campos de texto y actualizar los lados del triangulo
        lado_a = self.campo_lado_a.text()
        lado_b = self.campo_lado_b.text()
        lado_c = self.campo_lado_c.text()

        self.objeto.establecer_lados(lado_a, lado_b, lado_c)
        self.accept()

# Clase "formulas" para calcular los datos de un triángulo
class formulas:
    def __init__(self):
        self.lado_a = None
        self.lado_b = None
        self.lado_c = None
        self.altura = None
        self.area = None

    def establecer_lados(self, lado_a, lado_b, lado_c):
        # Establecer los lados del triángulo y recalcular altura y área
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
        # Fórmula del área del triáángulo: base por altura sobre 2
        if self.lado_a is not None and self.altura is not None:
            self.area = (self.lado_a * self.altura) / 2
        else:
            self.area = 0

    def __str__(self):
        # Representación en cadena del triangulo con sus datos
        return f"Lado A: {self.lado_a}\nLado B: {self.lado_b}\nLado C: {self.lado_c}\nAltura: {self.altura}\nÁrea: {self.area}"

if __name__ == "__main__":
    # Crear la aplicación y mostrar la ventana principal
    app = QApplication(sys.argv)
    ventana = AppComparacion()
    ventana.show()
    sys.exit(app.exec_())



