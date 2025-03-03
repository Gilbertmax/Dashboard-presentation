class Empresa:
    def __init__(self, nombre, rfc, direccion):
        self.nombre = nombre
        self.rfc = rfc
        self.direccion = direccion

class Transaccion:
    def __init__(self, empresa, fecha, tipo, cuenta_contable, monto):
        self.empresa = empresa
        self.fecha = fecha
        self.tipo = tipo
        self.cuenta_contable = cuenta_contable
        self.monto = monto