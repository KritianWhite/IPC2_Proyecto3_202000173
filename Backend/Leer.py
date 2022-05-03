from msilib import type_key
from xml.etree import ElementTree as ET
import xmltodict, json
from datetime import datetime

from Mensajes import Mensaje, servicio, empresa
import re

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def leerXML(xml):
    positivos = []
    negativos = []
    empresas = []
    mensajes = []

    xEmpresas = []

    doc = xmltodict.parse(xml, encoding="utf-8")

    positivos = doc['solicitud_clasificacion']['diccionario']['sentimientos_positivos']['palabra']
    negativos = doc['solicitud_clasificacion']['diccionario']['sentimientos_negativos']['palabra']

    x = doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    if type(x) == list:
        empresas = doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    else:
        empresas.append(doc['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa'])
        #print(empresas)

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
        #mensajes.sort(key = lambda mensaje: datetime.strptime(mensaje.fecha, '%d/%m/%Y'), reverse=True)
        #print(mensajes)


        #---->busqueda de palabras positivas y negativas en el mensaje
        for r in mensajes:
            contadorPositivos = 0
            for j in positivos:
                for k in r.contenido:
                    if j in k:
                        contadorPositivos+=1
            r.positivos = (contadorPositivos)
        print('\nPalabras positivas: ', r.positivos)

        for i in mensajes:
            contadorNegativos = 0
            for j in negativos:
                for k in i.contenido:
                    if j in k:
                        contadorNegativos += 1
            i.negativos = contadorNegativos
        print('Palabras negativas: ', i.negativos)
        i.clasificarMensaje()

    

    
    #------>busqueda de servicio y empresa
    for m in mensajes:
        for n in empresas:
            tmpContenido = ' '
            #print(type(n))
            #print(n)
            #print(str(n['nombre']))
            for content in m.contenido:
                tmpContenido += content
                tmpContenido += " "
                if str(n['nombre']).lower() in tmpContenido:
                    m.empresas = str(n['nombre'])
                    print(m.empresas)
                    print(m.clasificarPor_Empresa())
                    break

                for servis in str(n['servicio']):
                    try:
                        if type(servis['alias']) == list:
                            for a in str(servis['alias']):
                                if a in tmpContenido:
                                    m.servicio = servis['@nombre']
                        elif type(servis['alias']) == str:
                            if str(servis['alias']) in tmpContenido:
                                m.servicio = servis['@nombre']
                                print(m.servicio)
                                print(m.lasificarPor_Empresa())
                    except:
                        #if str(servis['@nombre']).lower() in tmpContenido:
                        #    m.servicio = servis['@nombre']
                        #    print(m.servicio)
                        pass
    
    return(mensajes)


class Analizar:
    def __init__(self):
        self.mensajes = []
        self.empresas = []
        self.xml = []
        self.totalMensajes = 0
        self.mensajesPositivos = 0
        self.mensajesNegativos = 0
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

    def clasificacion(self, xml):
        self.xml = xml
        self.mensajes = leerXML(xml)

    def listar(self):
        #----> suma del tipo de mensaje obtenido
        for m in self.mensajes:
            self.totalMensajes += 1
            if m.tipo == 'POSITIVO':
                self.mensajesPositivos += 1
            elif m.tipo == 'NEGATIVO': 
                self.mensajesNegativos += 1
            elif m.tipo == 'NEUTRO':
                self.mensajesNeutros += 1

            #----> ordenamiento de mensajes por fecha
            m.fecha = datetime.strptime(m.fecha+" "+m.hora, '%d/%m/%Y %H:%M')
        self.mensajes = sorted(self.mensajes, key=lambda x: x.fecha)







