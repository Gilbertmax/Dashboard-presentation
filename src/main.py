import sys
from PyQt5.QtWidgets import QApplication
from views import MainWindow

def main():
    app = QApplication(sys.argv)

    with open('assets/styles.css', 'r') as f:
        app.setStyleSheet(f.read())

    server = "tu_servidor"
    database = "tu_base_de_datos"
    username = "tu_usuario"
    password = "tu_contraseña"

    window = MainWindow(server, database, username, password)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()