
import collections
import json
from xml.etree import ElementTree as ET
import xmltodict
from collections import OrderedDict
from datetime import datetime


from Mensaje import Mensaje, empresa, servicio

def normalice(setso):
    texto = str(setso).lower()
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        texto = texto.replace(a, b)
    return texto


palabrasPositivas=[]
palabrasNegativas=[]
Empresas = []

def leerXML(xml):
    mensajes = []

    doc = xmltodict.parse(xml,encoding="utf-8")
    
    file = open('BaseDatos.xml','w', encoding="utf-8")
    file.write(str(xml).replace('\n', '')) ##---> base de datos
    file.close()

    palabrasPositivas = doc['solicitud_clasificacion']['diccionario']['sentimientos_positivos']['palabra']
    palabrasNegativas = doc['solicitud_clasificacion']['diccionario']['sentimientos_negativos']['palabra']
    Empresas = doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    mensajesList = doc['solicitud_clasificacion']['lista_mensajes']['mensaje']

    tmpMensajes = []
    for m in mensajesList: #---> nuestro tmpMensajes sera una lista de palabra por palabra sin incluir espacios
        temp2 = [] #        ---> ejemplo: tmpMensajes =[hola,mundo]
        mensaje2 = m.lower().split(' ')
        for men2 in mensaje2:
            if men2 != '\n':
                temp2.append(men2)
        tmpMensajes.append(temp2)

    for m in tmpMensajes:
        lugar = ''
        fecha = ''
        hora = ''
        user = ''
        red = ''
        letraPorMensaje = []
        i = 0 #----> iterador para recorrer tmpMensajes=[]
        for palabra in m:
            if i == 3:
                lugar = normalice(palabra)
            elif i == 4:
                fecha = palabra
            elif i == 5:
                hora = palabra
            elif i == 7:
                user = normalice(palabra)
            elif i == 10:
                red = normalice(palabra)
            elif i >= 11:
                letraPorMensaje.append(normalice(palabra)) #---> lista letra por letra ejemplo: letraPorMensaje = [h,o,l,a,m,u,n,d,o]
            i+=1                                           #     (no toma en cuenta los espacios... :D )

        nuevo = Mensaje(lugar, fecha, hora, user, red, letraPorMensaje) #----> enviamos los datos a nuestro doceto
        mensajes.append(nuevo) #---> representamos nuestro docetos como lista 

    #-----> busqueda de palabras positivas y negativas en el mensaje
    for m in mensajes:
        contadorPositivos = 0
        for p in palabrasPositivas:
            for content in m.contenido:
                if normalice(p) in content:
                    contadorPositivos += 1
        m.positivos = (contadorPositivos)

    for m in mensajes:
        contadorNegativos = 0
        for n in palabrasNegativas:
            for content in m.contenido:
                if normalice(n) in content:
                    contadorNegativos += 1
        m.negativos = (contadorNegativos)

    #----> encontrando empresas y servicios
    for m in mensajes:
        m.clasificarMensaje()
        for e in Empresas: 
            tmpContenido = m.texto
            if (normalice(e['nombre'])) in normalice(tmpContenido):
                    m.empresa = (normalice(e['nombre']))

            #----> obtencion de servicio

            if type(e['servicio']) == collections.OrderedDict:
                try:
                    if (type(e['servicio']['alias'])) == list:
                        for ali in (e['servicio']['alias']):
                            if normalice(ali) in normalice(tmpContenido):
                                m.servicio = normalice(e['servicio']['@nombre'])
                    elif (type(e['servicio']['alias'])) == str: #---> se pregunta si es igual cadena, ya que a la hora de que se vacia 
                                                    #     nuestro onjDict, que es una lista donde se encuentra adentro nuestras
                                                    #     empresas y servicios queda solo un string que es 'alias' (evita que pueda crashear nuestra app)
                        if normalice(e['servicio']['alias']) in tmpContenido:
                                m.servicio = normalice(e['servicio']['@nombre'])
                except:
                    if normalice(e['servicio']['@nombre']) in tmpContenido:
                        m.servicio = normalice(e['servicio']['@nombre'])
            elif type(e['servicio']) == list:
                for servis in e['servicio']:
                    try:
                        if (type(servis['alias'])) == list:
                            for alia in (servis['alias']):
                                if normalice(alia) in normalice(tmpContenido):
                                    m.servicio = normalice(servis['@nombre'])
                        elif (type(servis['alias'])) == str:
                            if normalice(servis['alias']) in tmpContenido:
                                    m.servis = normalice(servis['@nombre'])
                    except:
                        if normalice(servis['@nombre']) in tmpContenido:
                            m.servicio = normalice(servis['@nombre'])
    for m in mensajes:
        '''print('\nLugar y fecha: '+m.lugar+' '+m.fecha) 
        print('Hora: '+m.hora) 
        print('Usuario: '+m.user)
        print('Red social: '+m.red)
        print('Empresa {}, servicio {}'.format(m.empresa, m.servicio))
        print('Mensaje: '+m.texto)
        print('El mensaje fue: '+ str(m.tipo).upper())'''
        pass
    

    return (mensajes)


def pruebaMensaje(xml2): #---> Practicamente lo mismo, con leve diferencia
    '''filee = open('Backend\BaseDatos.xml', 'r')
    filee = filee.read()

    doc = xmltodict.parse(filee, encoding='utf-8')
    
    SentimientosPositivos = doc['solicitud_clasificacion']['diccionario']['sentimientos_positivos']['palabra']
    SentimientosNegativos = doc['solicitud_clasificacion']['diccionario']['sentimientos_negativos']['palabra']
    Empresas = doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    ListaMensajes = doc['solicitud_clasificacion']['lista_mensajes']['mensaje']'''

    doc2 = xmltodict.parse(xml2, encoding="utf-8")
    mensaje = doc2['mensaje']
    mensaje = mensaje.split(' ')
    lugar = ''
    fecha = ''
    hora = ''
    user = ''
    red = ''
    mensaje0 = []
    i = 0
    for palabra in mensaje:
        if i == 3:
            lugar = normalice(palabra)
        elif i == 4:
            fecha = palabra
        elif i == 5:
            hora = palabra
        elif i == 8:
            user = normalice(palabra)
        elif i == 11:
            red = normalice(palabra)
        elif i >= 12:
            mensaje0.append(normalice(palabra))
        i+=1    
    nuevo = Mensaje(lugar, fecha, hora, user, red, mensaje0)
    for i in Empresas:
        tempcontenido = ''
        for content in nuevo.contenido:
            tempcontenido += content
            tempcontenido += " "

        if (normalice(i['nombre'])) in tempcontenido:
                nuevo.empresa = (normalice(i['nombre']))
        if type(i['servicio']) == collections.OrderedDict:
                try:
                    if (type(i['servicio']['alias'])) == list:
                        for alia in (i['servicio']['alias']):
                            if normalice(alia) in normalice(tempcontenido):
                                nuevo.servicio = normalice(i['servicio']['@nombre'])
                    elif (type(i['servicio']['alias'])) == str:
                        if normalice(i['servicio']['alias']) in tempcontenido:
                                nuevo.servicio = normalice(i['servicio']['@nombre'])
                except:
                    if normalice(i['servicio']['@nombre']) in tempcontenido:
                        nuevo.servicio = normalice(i['servicio']['@nombre'])
        elif type(i['servicio']) == list:
            for service in i['servicio']:
                try:
                    if (type(service['alias'])) == list:
                        for alia in (service['alias']):
                            if normalice(alia) in normalice(tempcontenido):
                                nuevo.servicio = normalice(service['@nombre'])
                    elif (type(service['alias'])) == str:
                        if normalice(service['alias']) in tempcontenido:
                                nuevo.servicio = normalice(service['@nombre'])
                except:
                    if normalice(service['@nombre']) in tempcontenido:
                        nuevo.servicio = normalice(service['@nombre'])
        Positivos = 0
        for j in palabrasPositivas:
            for content in nuevo.contenido:
                if normalice(j) in content:
                    Positivos += 1
        nuevo.positivos = (Positivos)
        Negativos = 0
        for j in palabrasNegativas:
            for content in nuevo.contenido:
                if normalice(j) in normalice (content):
                    Negativos += 1
        nuevo.negativos = (Negativos)
    nuevo.clasificarMensaje()
    nuevo.balancear()
    return(nuevo)


class Adminstrador: 
    def __init__(self):
        self.mensajes = []
        self.empresas = []
        self.xml = []

        self.totalMensajes =0
        self.totalPositivos = 0
        self.totalNegativos = 0
        self.totalNeutros = 0

        self.nose = [] #----Z reporte 1
        self.reporte2 = {}
        self.reporte3 = {}
        self.reporte4 = []

    def mostrarMensaje(self):
        diccionarioMensajes = []
        for mensaje in self.mensajes:
            diccionario = {
                'lugar' : mensaje.lugar,
                'fecha' : mensaje.fecha,
                'hora' : mensaje.hora,
                'usuario' : mensaje.user,
                'red' : mensaje.red,
                'empresa' : mensaje.empresa,
                'servicio' : mensaje.servicio,
                'contenido' : mensaje.contenido,
                'tipo' : mensaje.tipo
            }
            diccionarioMensajes.append(diccionario)
        json = {
            'listadoMen' : diccionarioMensajes
        }
        self.reporte3 = (json)
        return (json)
        return json

    def nuevo_mensaje(self,LyF,user,red):
        new = Mensaje(LyF,user,red)
        self.mensajes.append(new)
        return True
    
    def obtener_mensajes(self):
        json=[]
        for i in self.mensajes:
            mensaje={
                'lugar':i.lugar,
                'fecha':i.fecha,
                'user':i.user,
                'red':i.red,
                'tipo':i.tipo,
                'contenido': i.contenido
            }
            json.append(mensaje)
        return json

    def recibirXML(self, xml):
        self.xml = xml
        self.mensajes = leerXML(xml)

    def clasificacionMensajes(self):
        for m in self.mensajes:
            self.totalMensajes += 1
            if m.tipo == 'positivo':
                self.totalPositivos += 1
            elif m.tipo == 'negativo':
                self.totalNegativos += 1
            elif m.tipo == 'neutro':
                self.totalNeutros += 1
            # parse de fecha, realmente no se si haya sido necesario :)
            m.fecha = datetime.strptime((str(m.fecha)), "%d/%m/%Y")
        self.mensajes = sorted(self.mensajes, key= lambda x: x.fecha) #--> sorted nos ordena los mensajes por fecha

        # --> obteniendo cantidad de mensajes por emporesa, incluyendo su tipo de mensaje :D
        for m2 in self.mensajes:
            if len(self.empresas) == 0:
                new = empresa(m2.empresa) #--> se crea una empresa si no hay una
                new.total += 1
                if m2.tipo == 'positivo':
                    new.positivo += 1
                elif m2.tipo == 'negativo':
                    new.negativo += 1
                elif m2.tipo == 'neutro':
                    new.neutro += 1
                nuevo = servicio(m2.servicio) #---> agregamos el servicio
                nuevo.total += 1
                if m2.tipo == 'positivo':
                    nuevo.positivo += 1
                elif m2.tipo == 'negativo':
                    nuevo.negativo += 1
                elif m2.tipo == 'neutro':
                    nuevo.neutro += 1
                new.servicios.append(nuevo)
                self.empresas.append(new)
            else: #---> si no encontro nada se reocorren las empresas
                busqueda = 0
                for emp in self.empresas:
                    if emp.nombre == m2.empresa:
                        busqueda += 1
                        emp.total += 1
                        if m2.tipo == 'positivo':
                            emp.positivo += 1
                        elif m2.tipo == 'negativo':
                            emp.negativo += 1
                        elif m2.tipo == 'neutro':
                            emp.neutro += 1
                        #---> validamos servicios
                        if (len(emp.servicios)) == 0: #---> si no hay servicios, se crea
                            nuevo = servicio(m2.servicio)
                            nuevo.total += 1
                            if m2.tipo == 'positivo':
                                nuevo.positivo += 1
                            elif m2.tipo == 'negativo':
                                nuevo.negativo += 1
                            elif m2.tipo == 'neutro':
                                nuevo.neutro += 1
                            emp.servicios.append(nuevo) #---> agregamos al servicio
                        else:
                            Encontrado2 = 0
                            for s in emp.servicios:
                                if s.nombre == m2.servicio:
                                    Encontrado2 += 1
                                    s.total += 1
                                    if m2.tipo == 'positivo':
                                        s.positivo += 1
                                    elif m2.tipo == 'negativo':
                                        s.negativo += 1
                                    elif m2.tipo == 'neutro':
                                        s.neutro += 1
                            #S --> saliendo del for validamos si no se encontro nada en los servicios
                            if Encontrado2 == 0:
                                nuevo = servicio(m2.servicio)
                                nuevo.total += 1
                                if m2.tipo == 'positivo':
                                    nuevo.positivo += 1
                                elif m2.tipo == 'negativo':
                                    nuevo.negativo += 1
                                elif m2.tipo == 'neutro':
                                    nuevo.neutro += 1
                                emp.servicios.append(nuevo)
                # ---> por si las moscas xd (si no encontro nada)
                if busqueda == 0:
                    new = empresa(m2.empresa)
                    new.total += 1
                    if m2.tipo == 'positivo':
                        new.positivo += 1
                    elif m2.tipo == 'negativo':
                        new.negativo += 1
                    elif m2.tipo == 'neutro':
                        new.neutro += 1
                    nuevo = servicio(m2.servicio)
                    nuevo.total += 1
                    if m2.tipo == 'positivo':
                        nuevo.positivo += 1
                    elif m2.tipo == 'negativo':
                        nuevo.negativo += 1
                    elif m2.tipo == 'neutro':
                        nuevo.neutro += 1
                    new.servicios.append(nuevo)
                    self.empresas.append(new)

    def salidaXML(self):
        texto = '<?xml version="1.0"?>'
        texto += '\n<lista_respuestas>'
        texto += '\n<respuesta>'
        texto += '\n<fecha>' + ' '+ str (datetime.now().date()) +' ' +'</fecha>'
        texto += '\n<mensajes>'
        texto += '\n<total>' + ' '+ str (self.totalMensajes) +' ' +'</total>'
        texto += '\n<positivos>' + ' '+ str (self.totalPositivos) +' ' +'</positivos>'
        texto += '\n<negativos>' + ' '+ str (self.totalNegativos) +' ' +'</negativos>'
        texto += '\n<neutros>' + ' '+ str (self.totalNeutros) +' ' +'</neutros>'
        texto += '\n</mensajes>'
        texto += '\n<analisis>'
        for em in self.empresas:
            texto += '\n<empresa nombre= \"' + em.nombre + '\">'
            texto += '\n<mensajes>'
            texto += '\n<total>' + ' '+ str(em.total) +' ' +'</total>'
            texto += '\n<positivos>' + ' '+ str(em.positivo) +' ' +'</positivos>'
            texto += '\n<negativos>' + ' '+ str(em.negativo) +' ' +'</negativos>'
            texto += '\n<neutros>' + ' '+ str(em.neutro) +' ' +'</neutros>'
            texto += '\n</mensajes>'
            texto += '\n<servicios>'
            for ss in em.servicios:
                texto += '\n<servicio nombre= \"' + ss.nombre + '\">'
                texto += '\n<mensajes>'
                texto += '\n<total>' + ' '+ str(ss.total) +' ' +'</total>'
                texto += '\n<positivos>' + ' '+ str(ss.positivo) +' ' +'</positivos>'
                texto += '\n<negativos>' + ' '+ str(ss.negativo) +' ' +'</negativos>'
                texto += '\n<neutros>' + ' '+ str(ss.neutro) +' ' +'</neutros>'
                texto += '\n</mensajes>'
                texto += '\n</servicio>'
            texto += '\n</servicios>'
            texto += '\n</empresa>'
        texto += '\n</analisis>'
        texto += '\n</respuesta>'
        texto += '\n</lista_respuestas>'
        
        return(texto)

    def clasificacionFecha(self, fecha, empresa):
        # parseamos la fecha, ya que se habia parseado y se recibe un string
        fecha = str(fecha).replace('-','/')
        fecha = datetime.strptime(fecha, "%Y/%m/%d")
        fecha = fecha.strftime("%d/%m/%Y")
        fecha = datetime.strptime(fecha, "%d/%m/%Y")
        clasificacion = []
        if empresa == 'todas':
            for mensaje in self.mensajes: #--> recorremos todas las empresas
                if mensaje.fecha == fecha:
                    Encontrado =0 #---> Contador de mensajes encontrados
                    for i in clasificacion:
                        if i['nombre'] == mensaje.empresa:
                            i['total'] += 1
                            if mensaje.tipo == 'positivo':
                                i['positivos'] += 1
                            elif mensaje.tipo == 'negativo':
                                i['negativos'] += 1
                            elif mensaje.tipo == 'neutro':
                                i['neutros'] += 1
                            Encontrado += 1
                    #--> por si no se encontró nada
                    if Encontrado == 0:
                        positivos=0
                        negativos = 0 
                        neutros = 0
                        if mensaje.tipo == 'positivo':
                            positivos += 1
                        elif mensaje.tipo == 'negativo':
                            negativos += 1
                        elif mensaje.tipo == 'neutro':
                            neutros += 1
                        #--> creamos un diccionario
                        nuevo = {
                            'nombre':mensaje.empresa,
                            'fecha': mensaje.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutros': neutros,
                        }
                        clasificacion.append(nuevo) #---> agregamos nuestro diccionario a la lista
        else :
            #--> si no recorremos nuevo verificando si ambas fechas y empresas concuerdan
            for mensaje in self.mensajes:
                if mensaje.fecha == fecha and mensaje.empresa == empresa:
                    print(mensaje.fecha, empresa)
                    Encontrado =0 
                    for i in clasificacion:
                        if i['nombre'] == mensaje.empresa:
                            i['total'] += 1
                            if mensaje.tipo == 'positivo':
                                i['positivos'] += 1
                            elif mensaje.tipo == 'negativo':
                                i['negativos'] += 1
                            elif mensaje.tipo == 'neutro':
                                i['neutros'] += 1
                            Encontrado += 1
                    #--> si en dado caso no se encontró nada
                    if Encontrado == 0:
                        print(mensaje.empresa)
                        positivos=0
                        negativos = 0 
                        neutros = 0
                        if mensaje.tipo == 'positivo':
                            positivos += 1
                        elif mensaje.tipo == 'negativo':
                            negativos += 1
                        elif mensaje.tipo == 'neutro':
                            neutros += 1
                        # --> volvemos a crear diccionario
                        nuevo = {
                            'nombre':mensaje.empresa,
                            'fecha': mensaje.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutros': neutros,
                        } 
                        clasificacion.append(nuevo)

        reporte2 = {
            'Listado': clasificacion,
            'fecha': fecha
        }   
        print(reporte2)
        self.reporte2 = reporte2
        return (reporte2)     
                

    def clasificacionRango_Fecha(self, fecha1, fecha2, empresa):
        Fechas_listado = []
        #---> parseo de las variables a fecha porque se recibe un string
        fecha1 = str(fecha1).replace('-','/')
        fecha1 = datetime.strptime(fecha1, "%Y/%m/%d")
        fecha1 = fecha1.strftime("%d/%m/%Y")
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")

        fecha2 = str(fecha2).replace('-','/')
        fecha2 = datetime.strptime(fecha2, "%Y/%m/%d")
        fecha2 = fecha2.strftime("%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")

        for mensaje in self.mensajes:
            # ---> verificamos si las fechas son iguales y proceder con la busqueda
            if (mensaje.fecha >= fecha1) and (mensaje.fecha <= fecha2):
                    if empresa == 'todas':
                        Encontrado1 = 0 #---> contador mensajes encontrados en el intervalo
                        for i in Fechas_listado:
                            if i['nombre'] == mensaje.empresa and i['fecha']== mensaje.fecha:
                                Encontrado += 1
                        # ---> si no se encontro nada
                        if Encontrado1 == 0:
                            positivos = 0
                            negativos = 0 
                            neutros = 0
                            if mensaje.tipo == 'positivo':
                                positivos += 1
                            elif mensaje.tipo == 'negativo':
                                negativos += 1
                            elif mensaje.tipo == 'neutro':
                                neutros += 1
                            # ---> creamos el diccionario
                            nuevo = {
                                'nombre':mensaje.empresa,
                                'fecha': mensaje.fecha,
                                'total': 1,
                                'positivos': positivos,
                                'negativos': negativos,
                                'neutros': neutros,
                            }
                            Fechas_listado.append(nuevo)
                        # ---> si no se vuelve a buscar nuevamente
                        else:
                            for i in Fechas_listado:
                                if i['nombre'] == mensaje.empresa and i['fecha']== mensaje.fecha:
                                    i['total'] += 1
                                    if mensaje.tipo == 'positivo':
                                        i['positivos'] += 1
                                    elif mensaje.tipo == 'negativo':
                                        i['negativos'] += 1
                                    elif mensaje.tipo == 'neutro':
                                        i['neutros'] += 1
                    # ---> si nuevamente no se encontro nada, volvemos a buscar, ya que se encontrarn ya incluidas las empresas nuevas, si llegasen a ver
                    else:
                        Encontrado1 = 0
                        for i in Fechas_listado:
                            if i['nombre'] == mensaje.empresa == empresa and i['fecha']== mensaje.fecha:
                                Encontrado += 1
                        if Encontrado1 == 0 and mensaje.empresa == empresa:
                            positivos=0
                            negativos = 0 
                            neutros = 0
                            if mensaje.tipo == 'positivo':
                                positivos += 1
                            elif mensaje.tipo == 'negativo':
                                negativos += 1
                            elif mensaje.tipo == 'neutro':
                                neutros += 1
                            # --> creamos el diccionario
                            nuevo = {
                                'nombre':empresa,
                                'fecha': mensaje.fecha,
                                'total': 1,
                                'positivos': positivos,
                                'negativos': negativos,
                                'neutros': neutros,
                            }
                            Fechas_listado.append(nuevo)
                        # ---> si no, volvemos a buscar en el diccionario que ya contiene empresas
                        else:
                            for i in Fechas_listado:
                                if i['nombre'] == empresa and i['fecha']== mensaje.fecha:
                                    i['total'] += 1
                                    if mensaje.tipo == 'positivo':
                                        i['positivos'] += 1
                                    elif mensaje.tipo == 'negativo':
                                        i['negativos'] += 1
                                    elif mensaje.tipo == 'neutro':
                                        i['neutros'] += 1
        json = {
            'listado' : Fechas_listado
        }
        self.reporte3 = (json)
        return (json)

    def retornar_empresas(self):
        dictionary = {}
        #print ('Tamo activo papi')
        for em in self.empresas:
            print (em.nombre)
            dictionary.append(em.nombre)
        print (dictionary)
        return (dictionary)

    def prueba_mensaje(self, xml2):
        mensajePrueba = pruebaMensaje(xml2)
        texto = '<?xml version="1.0"?>' + '\n'
        texto += '<respuesta>' + '\n'
        texto += '<fecha> ' + str(mensajePrueba.fecha) +' </fecha>' + '\n'
        texto += '<red_social> ' + str(mensajePrueba.red) +' </red_social>' + '\n'
        texto += '<usuario> ' + str(mensajePrueba.user) +' </usuario>' + '\n'
        texto += '<empresas>' '\n'
        texto += '<empresa nombre = ' + str(mensajePrueba.empresa) + ' >'  + '\n'
        texto += '<servicio> ' + str(mensajePrueba.servicio) +' </fecha>' + '\n'
        texto += '</empresa> '+ '\n'
        texto += '</empresas> '+ '\n'
        texto += '<palabras_positivas> ' + str(mensajePrueba.positivos) +' </palabras_positivas>' + '\n'
        texto += '<palabras_negativas> ' + str(mensajePrueba.negativos) +' </palabras_negativas>' + '\n'
        texto += '<sentimiento_positivo> ' + str(mensajePrueba.balancePositivo) + '%' +' </sentimiento_positivo>' + '\n'
        texto += '<sentimiento_negativo> ' + str(mensajePrueba.balanceNegativo) + '%' +' </sentimiento_negativo>' + '\n'
        texto += '<sentimiento_analizado> ' + str(mensajePrueba.tipo) + '%' +' </sentimiento_analizado>' + '\n'
        texto += '</respuesta>' + '\n'
        self.reporte4 = texto
        return (texto)

