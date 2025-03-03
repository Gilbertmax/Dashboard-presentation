import pyodbc
import pandas as pd

class Database:
    def __init__(self, server, database, username, password):
        self.connection = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        self.cursor = self.connection.cursor()

    def obtener_clientes(self):
        query = "SELECT ClienteID, Nombre, RFC, Direccion FROM admClientes"
        return pd.read_sql(query, self.connection)

    def obtener_movimientos_por_cliente(self, cliente_id):
        query = f"""
        SELECT MovimientoID, Fecha, Tipo, CuentaContable, Monto
        FROM admMovimientosContables
        WHERE ClienteID = {cliente_id}
        """
        return pd.read_sql(query, self.connection)

    def obtener_ejercicios(self):
        query = "SELECT EjercicioID, Año FROM admEjercicios"
        return pd.read_sql(query, self.connection)