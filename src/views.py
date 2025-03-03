from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QHBoxLayout, QGroupBox, QLabel, QCompleter)
from PyQt5.QtGui import QColor, QPalette  
from PyQt5.QtCore import Qt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contabilidad de Empresas")
        self.setGeometry(100, 100, 1200, 900)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        panel_busqueda = QGroupBox("Búsqueda de Empresas")
        layout_busqueda = QVBoxLayout()
        self.barra_busqueda_empresas = QLineEdit()
        self.barra_busqueda_empresas.setPlaceholderText("Buscar empresa por nombre...")
        layout_busqueda.addWidget(self.barra_busqueda_empresas)
        self.combo_empresas = QComboBox()
        layout_busqueda.addWidget(self.combo_empresas)
        panel_busqueda.setLayout(layout_busqueda)
        self.layout.addWidget(panel_busqueda)

        panel_filtros = QGroupBox("Filtros")
        layout_filtros = QHBoxLayout()
        self.combo_anios = QComboBox()
        layout_filtros.addWidget(QLabel("Año:"))
        layout_filtros.addWidget(self.combo_anios)
        self.btn_cargar = QPushButton("Cargar Transacciones")
        layout_filtros.addWidget(self.btn_cargar)
        panel_filtros.setLayout(layout_filtros)
        self.layout.addWidget(panel_filtros)

        panel_graficos = QGroupBox("Gráficos")
        layout_graficos = QHBoxLayout()
        self.btn_grafico_barras = QPushButton("Gráfico de Barras")
        self.btn_grafico_lineas = QPushButton("Gráfico de Líneas")
        self.btn_grafico_pastel = QPushButton("Gráfico de Pastel")
        layout_graficos.addWidget(self.btn_grafico_barras)
        layout_graficos.addWidget(self.btn_grafico_lineas)
        layout_graficos.addWidget(self.btn_grafico_pastel)
        panel_graficos.setLayout(layout_graficos)
        self.layout.addWidget(panel_graficos)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.database = Database()
        self.clientes = self.database.obtener_clientes()
        self.cargar_empresas()

        self.configurar_autocompletado()

        self.combo_empresas.currentIndexChanged.connect(self.cargar_anios)
        self.btn_cargar.clicked.connect(self.cargar_transacciones)
        self.btn_grafico_barras.clicked.connect(self.generar_grafico_barras)
        self.btn_grafico_lineas.clicked.connect(self.generar_grafico_lineas)
        self.btn_grafico_pastel.clicked.connect(self.generar_grafico_pastel)

    def configurar_autocompletado(self):
        nombres_empresas = self.clientes['Nombre'].tolist()
        completer = QCompleter(nombres_empresas, self)
        completer.setCaseSensitivity(False) 
        completer.setFilterMode(Qt.MatchStartsWith)  

        
        completer.popup().setStyleSheet("""
            QListView {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:hover {
                background-color: #4CAF50;
                color: white;
            }
        """)

        self.barra_busqueda_empresas.setCompleter(completer)
        self.barra_busqueda_empresas.textChanged.connect(self.filtrar_empresas)

    def cargar_empresas(self):
        self.combo_empresas.clear()
        self.combo_empresas.addItems(self.clientes['Nombre'])

    def filtrar_empresas(self):
        texto_busqueda = self.barra_busqueda_empresas.text().lower()
        empresas_filtradas = [nombre for nombre in self.clientes['Nombre'] if texto_busqueda in nombre.lower()]
        self.combo_empresas.clear()
        self.combo_empresas.addItems(empresas_filtradas)

    def cargar_anios(self):
        empresa_seleccionada = self.combo_empresas.currentText()
        if empresa_seleccionada:
            cliente_id = self.clientes[self.clientes['Nombre'] == empresa_seleccionada]['ClienteID'].values[0]
            movimientos = self.database.obtener_movimientos_por_cliente(cliente_id)
            anios = movimientos['Fecha'].dt.year.unique()
            self.combo_anios.clear()
            self.combo_anios.addItems(map(str, anios))

    def cargar_transacciones(self):
        empresa_seleccionada = self.combo_empresas.currentText()
        anio_seleccionado = self.combo_anios.currentText()
        if empresa_seleccionada and anio_seleccionado:
            cliente_id = self.clientes[self.clientes['Nombre'] == empresa_seleccionada]['ClienteID'].values[0]
            self.transacciones = self.database.obtener_movimientos_por_cliente(cliente_id)
            self.transacciones = self.transacciones[self.transacciones['Fecha'].dt.year == int(anio_seleccionado)]
            self.mostrar_transacciones()

    def mostrar_transacciones(self):
        if hasattr(self, 'transacciones'):
            self.table.setRowCount(self.transacciones.shape[0])
            self.table.setColumnCount(self.transacciones.shape[1])
            self.table.setHorizontalHeaderLabels(self.transacciones.columns)

            for i in range(self.transacciones.shape[0]):
                for j in range(self.transacciones.shape[1]):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.transacciones.iat[i, j])))

    def generar_grafico_barras(self):
        if hasattr(self, 'transacciones'):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            transacciones_agrupadas = self.transacciones.groupby('CuentaContable')['Monto'].sum()
            transacciones_agrupadas.plot(kind='bar', ax=ax)
            ax.set_xlabel('Cuenta Contable')
            ax.set_ylabel('Monto')
            ax.set_title('Total por Cuenta Contable')
            self.canvas.draw()

    def generar_grafico_lineas(self):
        if hasattr(self, 'transacciones'):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            transacciones_agrupadas = self.transacciones.groupby('Fecha')['Monto'].sum()
            transacciones_agrupadas.plot(kind='line', ax=ax)
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Monto')
            ax.set_title('Evolución de Montos por Fecha')
            self.canvas.draw()

    def generar_grafico_pastel(self):
        if hasattr(self, 'transacciones'):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            transacciones_agrupadas = self.transacciones.groupby('Tipo')['Monto'].sum()
            transacciones_agrupadas.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_title('Distribución de Montos por Tipo')
            self.canvas.draw()