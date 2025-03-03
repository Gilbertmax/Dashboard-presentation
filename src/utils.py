import pandas as pd
import numpy as np

def simular_datos():
    np.random.seed(42)
    empresas = [f'Empresa {i}' for i in range(1, 11)]
    cuentas_contables = ['Ingresos', 'Egresos', 'Activos', 'Pasivos', 'Capital']
    fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

    data = {
        'Empresa': np.random.choice(empresas, 1000),
        'Fecha': np.random.choice(fechas, 1000),
        'Tipo': np.random.choice(['Ingreso', 'Egreso'], 1000),
        'Cuenta Contable': np.random.choice(cuentas_contables, 1000),
        'Monto': np.random.randint(100, 10000, 1000)
    }
    return pd.DataFrame(data)