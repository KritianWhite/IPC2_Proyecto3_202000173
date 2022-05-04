
from xml.etree import ElementTree as ET
import xmltodict
from datetime import datetime

from Mensajes import Mensaje, servicio, empresa

def normalize(setso):
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
                lugar = normalize(palabra)
                #print('Lugar: '+lugar)
            elif i == 4:
                fecha = palabra
                #print('Fecha: '+fecha)
            elif i == 5:
                hora = palabra
                #print('Hora: '+hora)
            elif i == 7:
                usuario = normalize(palabra)
                #print('Usuario: '+usuario)
            elif i == 10:
                redSocial = normalize(palabra)
                #print('Red social: '+redSocial)
            elif i >= 11:
                tmpMensaje.append(normalize(palabra))
                #print(tmpMensaje)
            i+=1
        
        #----->agregando datos extraídos a nuestro objeto
        newMensaje = Mensaje(lugar,fecha,hora, usuario, redSocial, tmpMensaje)
        mensajes.append(newMensaje)
        mensajes.sort(key = lambda mensaje: datetime.strptime(mensaje.fecha, '%d/%m/%Y'), reverse=True)
        #print(mensajes)


        #---->busqueda de palabras positivas y negativas en el mensaje
        for r in mensajes:
            contadorPositivos = 0
            for j in positivos:
                for k in r.contenido:
                    if normalize(j) in k:
                        contadorPositivos+=1
            r.positivos = (contadorPositivos)
        #print('\nPalabras positivas: ', r.positivos)

        for i in mensajes:
            contadorNegativos = 0
            for j in negativos:
                for k in i.contenido:
                    if normalize(j) in k:
                        contadorNegativos += 1
            i.negativos = contadorNegativos
        #print('Palabras negativas: ', i.negativos)
        #i.clasificarMensaje()

    
    #------>busqueda de servicio y empresa
    for m in mensajes:
        for n in empresas:
            tmpContenido = ' '
            for content in m.contenido:
                tmpContenido += content
                tmpContenido += " "
            if normalize(n['nombre']) in tmpContenido:
                m.empresas = normalize(n['nombre'])
                q = m.empresas
                #print('\n',m.empresas)
                #print(m.clasificarPor_Empresa())
                #m.clasificarMensaje()

            for servis in n['servicio']:
                tmpServicios = []
                m.servicio = normalize(servis['@nombre'])
                tmpServicios.append(m.servicio)
                print(tmpServicios)
                
                try:
                    if normalize(servis['@nombre']) in (tmpContenido):
                        m.servicio = normalize(servis['@nombre'])
                        #tmpServicios.append(m.servicio)
                        #print(tmpServicios)
                        #print(normalize(servis['@nombre']))
                    elif type(servis['alias']) == list:
                        for a in servis['alias']:
                            if normalize(a) in normalize(tmpContenido):
                                m.servicio = normalize(servis['@nombre'])
                                #print(m.servicio)     
                    elif type(servis['alias']) == str:
                        if normalize(servis['alias']) in tmpContenido:
                            m.servicio = normalize(servis['@nombre'])
                            #print(m.servicio)
                except:
                    #if normalize(servis['@nombre'])in (tmpContenido):
                    #    print(normalize(servis['@nombre']))
                        #m.servicio = normalize(servis['@nombre'])
                        #print(m.servicio)
                    pass
                        

                
            #-----> impresión del mensaje como tal
                    '''
                    print('\nLugar: '+ m.lugar)
                    print('Fecha: '+ m.fecha)
                    print('Hora: '+ m.hora)
                    print('Usuario: '+ m.user)
                    print('Red social: '+ m.red)
                    print('Empresa: ', q)
                    print('Servicio: ', m.servicio)
                    print(m.clasificarPor_Empresa())
                    m.clasificarMensaje()'''
                    break
                
    return(mensajes)


class Analizar:
    def __init__(self):
        self.mensajes = []
        self.empresas = []
        self.xml = []
        self.totalMensajes = 0
        self.mensajesPositivos = 0 #---> Total positivos
        self.mensajesNegativos = 0 #---> Total negativos
        self.mensajesNeutros = 0 #---> Total neutros

    def mensajeNuevo(self, Lugar, fecha, hora, usuario, redSocial, contenido):
        new = Mensaje(Lugar, fecha, hora, usuario, redSocial, contenido)
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

    
    def recibirXML(self, xml):
        self.xml = xml
        self.mensajes = leerXML(xml)
    

    def Sampar_a_Listas(self):
        #----> suma del tipo de mensaje obtenido
        self.totalMensajes = 0 #-----> establecemos la cantidad de mensajes en 0, para que no se vayan sumando mientras se caargan archivos
        for m in self.mensajes:
            self.totalMensajes += 1
            if m.tipo == 'positivo':
                self.mensajesPositivos += 1
            elif m.tipo == 'negativo': 
                self.mensajesNegativos += 1
            elif m.tipo == 'neutro':
                self.mensajesNeutros += 1
                #print('Cantidad de mensajes neutros: ',self.mensajesNeutros)
        #print('Total mensajes: ', self.totalMensajes)

        #---> sumando la cantidad de mensajes sin importar su tipo
        for k in self.mensajes:
            if len(self.mensajes) == 0:
                tmp = empresa(k.empresa)
                tmp.total += 1
                if k.tipo == 'positivo':
                    tmp.positivo += 1
                elif k.tipo == 'negativo':
                    tmp.negativo += 1
                elif k.tipo == 'neutro':
                    tmp.neutro += 1

                nuevo = servicio(k.servicio)
                nuevo.total += 1

                if k.tipo == 'positivo':
                    nuevo.positivo += 1
                elif k.tipo == 'negativo':
                    nuevo.negativo += 1
                elif k.tipo == 'neutro':
                    nuevo.neutro += 1 

                tmp.servicios.append(nuevo)
                self.empresas.append(tmp)
            
            else:
                search = 0
                for l in self.empresas:
                    if l.nombre == k.empresa:
                        search += 1
                        l.total += 1
                        if k.tipo == 'positivo':
                            l.positivo += 1
                        elif k.tipo == 'negativo':
                            l.negativo += 1
                        elif k.tipo == 'neutro':
                            l.neutro += 1

                        #---> Validar servicios si no hay servicios
                        if len(k.servicio) == 0:
                            nuevo = servicio(k.servicio) #-----> Se añade un servicio si la lista esta vacia
                            nuevo.total += 1
                            if k.tipo == 'positivo':
                                nuevo.positivo += 1
                            elif k.tipo == 'negativo':
                                nuevo.negativo += 1
                            elif k.tipo == 'neutro':
                                nuevo.neutro += 1

                            l.servicios.append(nuevo)

                        else:
                            search2 = 0
                            for servis2 in l.servicios:
                                if servis2.nombre == k.servicio:
                                    search2 += 1
                                    servis2.total += 1
                                    if k.tipo == 'positivo':
                                        servis2.positivo += 1
                                    elif k.tipo == 'negativo':
                                        servis2.negativo += 1
                                    elif k.tipo == 'neutro':
                                        servis2.neutro += 1

                            if search2 == 0: #---> si no se encuentra nada, se crea un nuevo objeto y revisar si son positivos, negativos o neutro
                                nuevo = servicio(k.servicio)
                                nuevo.total += 1
                                if k.tipo == 'positivo':
                                    nuevo.positivo += 1
                                elif k.tipo == 'negativo':
                                    nuevo.negativo += 1
                                elif k.tipo == 'neutro':
                                    nuevo.neutro += 1

                                l.servicios.append(nuevo)

                if search == 0: #------> si no se encuentra nada procedemos a crear un nuevo objeto y revisar si son positivos, negativos o neutros
                    tmp = empresa(k.empresa)
                    tmp.total += 1
                    if k.tipo == 'positivo':
                        tmp.positivo += 1
                    elif k.tipo == 'negativo':
                        tmp.negativo += 1
                    elif k.tipo == 'neutro':
                        tmp.negativo += 1
                    
                    nuevo = servicio(k.servicio)
                    nuevo.total += 1

                    if k.tipo == 'positivo':
                        nuevo.positivo += 1
                    elif k.tipo == 'negativo':
                        nuevo.negativo += 1
                    elif k.tipo == 'neutro':
                        nuevo.neutro += 1
                    
                    tmp.servicios.append(nuevo)
                    self.empresas.append(tmp)

        #print('Total Mensajes: ', self.totalMensajes)
                
    def salidaXML(self):
        txt = '<?xml version="1.0"?>\n'
        txt += '<lista_respuestas>\n'
        txt += '\t<respuesta\n>'
        txt += '\t\t<fecha> '+ str(datetime.now().date())  + ' </fecha>\n'
        txt += '\t\t\t<mensajes>\n'
        txt += '\t\t\t\t<total> '+ str(self.totalMensajes) + ' </total>\n'
        txt += '\t\t\t\t<positivos> '+ str(self.mensajesPositivos) + ' </positivos>\n'
        txt += '\t\t\t\t<negativos> '+ str(self.mensajesNegativos) + ' </negativos>\n'
        txt += '\t\t\t\t<neutros> '+ str(self.mensajesNeutros) + ' </neutros>\n'
        txt += '\t\t\t</mensajes>\n'
        txt += '\t\t<analisis>\n'

        for empresaS in self.empresas:
            txt += '\t\t\t<empresa nombre=\"'+ empresaS.nombre+'\">\n'
            txt += '\t\t\t\t<mensajes>\n'
            txt += '\t\t\t\t\t<total> '+ str(empresaS.total) + ' </total>\n'
            txt += '\t\t\t\t\t<positivos> '+ str(empresaS.positivo) + ' </positivos>\n'
            txt += '\t\t\t\t\t<negativos> '+ str(empresaS.negativo) + ' </negativos>\n'
            txt += '\t\t\t\t\t<neutros> '+ str(empresaS.neutro) + ' </neutros>\n'
            txt += '\t\t\t\t</mensajes>\n'
            
            for servicioA in empresaS.servicios:
                txt += '\t\t\t\t<servicios>\n'
                txt += '\t\t\t\t\t<servicio nombre=\"'+ str(servicioA.nombre) +'\">\n'
                txt += '\t\t\t\t\t\t<mensajes>\n'
                txt += '\t\t\t\t\t\t\t<total> '+ str(servicioA.total) + ' </total>\n'
                txt += '\t\t\t\t\t\t\t<positivos> '+ str(servicioA.positivo) + ' </positivos>\n'
                txt += '\t\t\t\t\t\t\t<negativos> '+ str(servicioA.negativo) + ' </negativos>\n'
                txt += '\t\t\t\t\t\t\t<neutros> '+ str(servicioA.neutro) + ' </neutros>\n'
                txt += '\t\t\t\t\t\t</mensajes>\n'
                txt += '\t\t\t\t\t</servicio>\n'
                txt += '\t\t\t\t</servicios>\n'
            
            txt += '\t\t\t</empresa>\n'

        txt += '\t\t</analisis>\n'
        txt += '\t</respuesta>\n'
        txt += '</lista_respuestas>\n'
        return(txt)



                                                    






