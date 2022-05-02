from xml.etree import ElementTree as ET
import xmltodict, json

from Mensajes import Mensaje, servicio, empresa
import re

def leerXML(xml):
    positivos = []
    negativos = []
    mensajes = []

    doc = xmltodict.parse(xml, encoding="utf-8")

    positivos = doc['solicitud_clasificacion']['diccionario']['sentimientos_positivos']['palabra']
    negativos = doc['solicitud_clasificacion']['diccionario']['sentimientos_negativos']['palabra']
    empresas = doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    listMensajes = doc['solicitud_clasificacion']['lista_mensajes']['mensaje']
    
    tmpMensajes = []
    for mensaje in listMensajes:
        tmp2 = []
        mensaje2 = mensaje.lower().split(' ')
        for message2 in mensaje2:
            if message2 != '\n':
                tmp2.append(message2)
        tmpMensajes.append(tmp2)
    #print(tmpMensajes)

    #----->clasificación de mensajes
    for mensaje in tmpMensajes:
        lugar = ''
        fecha = ''
        hora = ''
        usuario = ''
        redSocial = ''
        tmpMensaje = []
        i = 0 #----> iterador
        for palabra in mensaje:
            if i == 3:
                lugar = palabra
                #print('Lugar: '+lugar)
            elif i == 4:
                fecha = palabra
                #print('Fecha: '+fecha)
            elif i == 5:
                hora = palabra
                #print('Hora: '+hora)
            elif i == 7:
                usuario = palabra
                #print('Usuario: '+palabra)
            elif i == 10:
                redSocial = palabra
                #print('Red social: '+redSocial)
            elif i >= 11:
                tmpMensaje.append(palabra)
                #print(tmpMensaje)
            i+=1
        
        #----->agregando datos extraídos a nuestro objeto
        newMensaje = Mensaje(lugar,fecha,hora, usuario, redSocial, tmpMensaje)
        mensajes.append(newMensaje)
        #print(mensajes)
        
        #---->busqueda de palabras positivas y negativas en el mensaje
        for i in mensajes:
            contadorPositivos = 0
            for j in positivos:
                for k in i.contenido:
                    if j in k:
                        contadorPositivos+=1
            i.positivos = (contadorPositivos)
        #print(i.positivos)

        for i in mensajes:
            contadorNegativos = 0
            for j in negativos:
                for k in i.contenido:
                    if j in k:
                        contadorNegativos += 1
            i.negativos = contadorNegativos
        #print(i.negativos)
    
    #------>busqueda de servicio y empresa
    for m in mensajes:
        m.clasificarMensaje()
        for n in empresas:
            tmpContenido = ' '
            for content in m.contenido:
                tmpContenido += content
                tmpContenido += " "
            if n['nombre'] in tmpContenido:
                m.empresa = n['nombre']

            for servis in n['servicio']:
                try:
                    if servis['alias'] == list:
                        for a in servis['alias']:
                            if a in tmpContenido:
                                m.servicio = servis['@nombre']
                    elif servis['alias'] == str:
                        if servis['alias'] in tmpContenido:
                            m.servicio = servis['@nombre']
                except:
                    if servis['@nombre'] in tmpContenido:
                        m.servicio = servis['@nombre']
    return(mensajes)


class Analizar:
    def __init__(self):
        self.mensajes = []
        self.empresas = []
        self.xml = []
        self.totalMensajes = 0
        self.palabrasPositivas = 0
        self.palabrasNegativas = 0
        self.mensajesNeutros = 0

    def mensajeNuevo(self, LyF, usuario, redSocial):
        new = Mensaje(LyF, usuario, redSocial)
        self.mensajes.append(new)
        return True
    
    def obtenerMensaje(self):
        json = []
        for i in self.mensajes:
            mensaje = {
                'lugar':i.lugar,
                'fecha':i.fecha,
                'user':i.user,
                'red':i.red,
                'tipo':i.tipo
            }
            json.append(mensaje)
        return json

    def fileClas(self, xml):
        pass


