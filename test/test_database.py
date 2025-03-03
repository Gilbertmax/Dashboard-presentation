import unittest
from src.database import Database

class TestDatabase(unittest.TestCase):
    def test_cargar_datos(self):
        db = Database()
        self.assertFalse(db.data.empty)

    def test_obtener_empresas(self):
        db = Database()
        empresas = db.obtener_empresas()
        self.assertTrue(len(empresas) > 0)

    def test_obtener_transacciones_empresa(self):
        db = Database()
        transacciones = db.obtener_transacciones_empresa('Empresa 1')
        self.assertFalse(transacciones.empty)

if __name__ == "__main__":
    unittest.main()