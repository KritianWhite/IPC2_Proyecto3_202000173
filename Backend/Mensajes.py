from platformdirs import user_cache_dir


class Mensaje:
    def __init__(self,lugar,fecha,hora,user,red, contenido):
        self.lugar = lugar
        self.fecha = fecha
        self.hora = hora
        self.user = user
        self.red = red
        self.contenido = contenido
        #Las primeras son variables de declaracion normal, las otras se declaran con funciones especiales
        self.positivos = 0
        self.negativos = 0
        self.texto = ""
        self.empresa = 'None'
        self.servicio = 'None'
        self.tipo = 'None'
        self.Contener()
    
    def obtenerMensaje(self):
        return self

    #CLASIFICA EN FUNCION SI SON MAYORES, MENORES IGUALES LOS MENSAJES POSITIVOS O NEGATIVOS
    def clasificarMensaje(self):
        separador = ' '
        x = separador.join(self.contenido)
        #print(x)
        if self.positivos > self.negativos:
            self.tipo = 'positivo'
            #print('El mensaje fue ',self.tipo)
        elif self.negativos > self.positivos:
            self.tipo = 'negativo'
            #print('El mensaje fue ',self.tipo)
        elif self.positivos == self.negativos:
            self.tipo = 'neutro'
            #print('El mensaje fue ',self.tipo)

    def clasificarPor_Empresa(self):
        separador = ' '
        x = separador.join(self.contenido)
        #print(x)
        #if self.empresa in self.contenido:
         #   self.empresa = self.contenido
            #print(self.empresa)
        return x

    def Contener(self):
        for text in self.contenido:
            self.texto += text
            self.texto += " "
            #print(self.texto)

class servicio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.total = 0
        self.positivo = 0
        self.negativo = 0
        self.neutro = 0
        self.alias = []

class empresa:
    def __init__(self , nombre):
        self.nombre = nombre
        self.total = 0
        self.positivo = 0
        self.negativo = 0
        self.neutro = 0
        self.servicios = []

