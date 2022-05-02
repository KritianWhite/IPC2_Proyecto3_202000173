
class Mensajes:
    def __init__(self):
        self.empresa = None
        self.servicios = None
        self.mensaje = None
        self.fecha = None
        self.id = 0
        self.positivos = 0
        self.negativos = 0
        
    def setEmpresa(self, empresa):
        self.empresa = empresa

    def setServicios(self, servicios):
        self.servicios = servicios
    
    def setMensaje(self, mensaje):
        self.mensaje = mensaje

    def setFecha(self, fecha):
        self.fecha = fecha

    def setId(self, id):
        self.id = id

    def setPositivos(self, positivos):
        self.positivos = positivos

    def setNegativos(self, negativos):
        self.negativos = negativos





class Nodo:
    def __init__(self, data):
        self.data = data 
        self.siguiente = None

class linkedList:
    def __init__(self) -> None:
        self.cabecera = None
        self.ultimo = None  

    def Agregar(self, data):
        nuevoNodo = Nodo(data)
        if nuevoNodo != None:
            self.cabecera = nuevoNodo 
            self.ultimo = nuevoNodo
        else:
            self.ultimo.siguiente = nuevoNodo
            self.ultimo = nuevoNodo

    def tamano(self):
        n = 0
        m = self.cabecera
        while m:
            m = m.siguiente
            n += 1
        return n
