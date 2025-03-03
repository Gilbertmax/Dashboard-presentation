import pandas as pd
import numpy as np

class Database:
    def __init__(self):
        self.clientes = self.simular_clientes()
        self.movimientos = self.simular_movimientos()
        self.ejercicios = self.simular_ejercicios()

    def simular_clientes(self):
        clientes = {
            'ClienteID': [1, 2, 3, 4, 5],
            'Nombre': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'],
            'RFC': ['AAA010101AAA', 'BBB020202BBB', 'CCC030303CCC', 'DDD040404DDD', 'EEE050505EEE'],
            'Direccion': ['Calle 1', 'Calle 2', 'Calle 3', 'Calle 4', 'Calle 5']
        }
        return pd.DataFrame(clientes)

    def simular_movimientos(self):
        movimientos = {
            'MovimientoID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'ClienteID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            'Fecha': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', 
                                    '2023-06-01', '2023-07-01', '2023-08-01', '2023-09-01', '2023-10-01']),
            'Tipo': ['Ingreso', 'Egreso', 'Ingreso', 'Egreso', 'Ingreso', 'Egreso', 'Ingreso', 'Egreso', 'Ingreso', 'Egreso'],
            'CuentaContable': ['Ingresos', 'Egresos', 'Ingresos', 'Egresos', 'Ingresos', 'Egresos', 'Ingresos', 'Egresos', 'Ingresos', 'Egresos'],
            'Monto': [1000, 500, 2000, 1000, 3000, 1500, 4000, 2000, 5000, 2500]
        }
        return pd.DataFrame(movimientos)

    def simular_ejercicios(self):
        ejercicios = {
            'EjercicioID': [1, 2, 3],
            'Año': [2021, 2022, 2023]
        }
        return pd.DataFrame(ejercicios)

    def obtener_clientes(self):
        return self.clientes

    def obtener_movimientos_por_cliente(self, cliente_id):
        return self.movimientos[self.movimientos['ClienteID'] == cliente_id]

    def obtener_ejercicios(self):
        return self.ejercicios