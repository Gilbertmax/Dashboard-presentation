import sys
from PyQt5.QtWidgets import QApplication
from views import MainWindow

def main():
    app = QApplication(sys.argv)

    # Cargar estilos CSS
    with open('assets/styles.css', 'r') as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()