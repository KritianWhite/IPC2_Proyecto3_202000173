from datetime import datetime

from Mensaje import Empresa, Servicio, Mensaje
import Manager


class Analizar:
    def __init__(self):
        self.xml = []
        self.mensajes = []
        self.empresas = []
        self.totalMensajes = 0
        self.mensajesPositivos = 0 #---> Total positivos
        self.mensajesNegativos = 0 #---> Total negativos
        self.mensajesNeutros = 0 #---> Total neutros


        #REPORTES
        self.reportePor_Fechas = {}
        self.reporteIntervalo_fechas = {}

    def recibirXML(self, xml):
        self.xml = xml
        self.mensajes = Manager.leerXML(xml)


    def mensajeNuevo(self, Lugaryfecha, usuario, redSocial):
        new = Mensaje(Lugaryfecha, usuario, redSocial)
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

    def Sampar_a_Listas(self):
        #----> suma del tipo de mensaje obtenido
        #self.totalMensajes = 0 #-----> establecemos la cantidad de mensajes en 0, para que no se vayan sumando mientras se caargan archivos
        for m in self.mensajes:
            self.totalMensajes += 1
            if m.tipo == 'positivo':
                self.mensajesPositivos += 1
            elif m.tipo == 'negativo': 
                self.mensajesNegativos += 1
            elif m.tipo == 'neutro':
                self.mensajesNeutros += 1
                #print('Cantidad de mensajes neutros: ',self.mensajesNeutros)
            m.fecha = datetime.strptime((str(m.fecha)), "%d/%m/%Y") #----> transformación de la fecha en formato de fecha
        #print('Total mensajes por fecha: ', self.totalMensajes)
        self.mensajes = sorted(self.mensajes, key=lambda x: x.fecha)

        #---> sumando la cantidad de mensajes sin importar su tipo
        for k in self.mensajes:
            if len(self.empresas) == 0:
                tmp = Empresa(k.empresa)
                tmp.total += 1
                if k.tipo == 'positivo':
                    tmp.positivo += 1
                elif k.tipo == 'negativo':
                    tmp.negativo += 1
                elif k.tipo == 'neutro':
                    tmp.neutro += 1

                tmp2 = Servicio(k.servicio)
                tmp2.total += 1

                if k.tipo == 'positivo':
                    tmp2.positivo += 1
                elif k.tipo == 'negativo':
                    tmp2.negativo += 1
                elif k.tipo == 'neutro':
                    tmp2.neutro += 1 

                tmp.servicios.append(tmp2)
                self.empresas.append(tmp)
            
            else:
                Encontrados = 0 #---- si la busqueda es igual a cero, volvemos a buscar en el mensaje
                for l in self.empresas:
                    if l.nombre == k.empresa:
                        Encontrados += 1
                        l.total += 1
                        if k.tipo == 'positivo':
                            l.positivo += 1
                        elif k.tipo == 'negativo':
                            l.negativo += 1
                        elif k.tipo == 'neutro':
                            l.neutro += 1

                        #---> Validar servicios si no hay servicios
                        if len(l.servicios) == 0:
                            tmp2 = Servicio(k.servicio) #-----> Se añade un servicio si la lista esta vacia
                            tmp2.total += 1
                            if k.tipo == 'positivo':
                                tmp2.positivo += 1
                            elif k.tipo == 'negativo':
                                tmp2.negativo += 1
                            elif k.tipo == 'neutro':
                                tmp2.neutro += 1

                            l.servicios.append(tmp2)

                        else:
                            Encontrados2 = 0
                            for servi in l.servicios:
                                if servi.nombre == k.servicio:
                                    Encontrados2 += 1
                                    servi.total += 1
                                    if k.tipo == 'positivo':
                                        servi.positivo += 1
                                    elif k.tipo == 'negativo':
                                        servi.negativo += 1
                                    elif k.tipo == 'neutro':
                                        servi.neutro += 1

                            if Encontrados2 == 0: #---> si no se encuentra nada, se crea un nuevo objeto y revisar si son positivos, negativos o neutro
                                tmp2 = Servicio(k.servicio)
                                tmp2.total += 1
                                if k.tipo == 'positivo':
                                    tmp2.positivo += 1
                                elif k.tipo == 'negativo':
                                    tmp2.negativo += 1
                                elif k.tipo == 'neutro':
                                    tmp2.neutro += 1

                                l.servicios.append(tmp2)
                    
                if Encontrados == 0: #------> si no se encuentra nada procedemos a crear un nuevo objeto y revisar si son positivos, negativos o neutros
                    tmp = Empresa(k.empresa)
                    tmp.total += 1
                    if k.tipo == 'positivo':
                        tmp.positivo += 1
                    elif k.tipo == 'negativo':
                        tmp.negativo += 1
                    elif k.tipo == 'neutro':
                        tmp.negativo += 1
                    
                    tmp2 = Servicio(k.servicio)
                    tmp2.total += 1

                    if k.tipo == 'positivo':
                        tmp2.positivo += 1
                    elif k.tipo == 'negativo':
                        tmp2.negativo += 1
                    elif k.tipo == 'neutro':
                        tmp2.neutro += 1
                    
                    tmp.servicios.append(tmp2)
                    self.empresas.append(tmp)

        #print('Total mensajes por servicio: ', l.servicios)
        #print('Total mensajes por empresa: ', self.empresas)

        #print('Total Mensajes: ', self.totalMensajes)
                
    def salidaXML(self):
        txt = '<?xml version="1.0"?>\n'
        txt += '<lista_respuestas>\n'
        txt += '<respuesta>\n'
        txt += '<fecha> '+ str(datetime.now().date())  + ' </fecha>\n'
        txt += '<mensajes>\n'
        txt += '<total> '+ str(self.totalMensajes) + ' </total>\n'
        txt += '<positivos> '+ str(self.mensajesPositivos) + ' </positivos>\n'
        txt += '<negativos> '+ str(self.mensajesNegativos) + ' </negativos>\n'
        txt += '<neutros> '+ str(self.mensajesNeutros) + ' </neutros>\n'
        txt += '</mensajes>\n'
        txt += '<analisis>\n'

        for empresaS in self.empresas:
            txt += '<empresa nombre=\"'+ str(empresaS.nombre)+'\">\n'
            txt += '<mensajes>\n'
            txt += '<total> '+ str(empresaS.total) + ' </total>\n'
            txt += '<positivos> '+ str(empresaS.positivo) + ' </positivos>\n'
            txt += '<negativos> '+ str(empresaS.negativo) + ' </negativos>\n'
            txt += '<neutros> '+ str(empresaS.neutro) + ' </neutros>\n'
            txt += '<mensajes>\n'
            
            for servicioA in empresaS.servicios:
                txt += '<servicios>\n'
                txt += '<servicio nombre=\"'+ str(servicioA.nombre) +'\">\n'
                txt += '<mensajes>\n'
                txt += '<total> '+ str(servicioA.total) + ' </total>\n'
                txt += '<positivos> '+ str(servicioA.positivo) + ' </positivos>\n'
                txt += '<negativos> '+ str(servicioA.negativo) + ' </negativos>\n'
                txt += '<neutros> '+ str(servicioA.neutro) + ' </neutros>\n'
                txt += '</mensajes>\n'
                txt += '</servicio>\n'
                txt += '</servicios>\n'
            
            txt += '</empresa>\n'

        txt += '</analisis>\n'
        txt += '</respuesta>\n'
        txt += '</lista_respuestas>\n'

        return(txt)

    def clasificaciónFecha(self, fecha, empresa):
        fecha = str(fecha).replace('-','/')
        fecha = datetime.strptime(fecha, "%Y/%m/%d")
        fecha = fecha.strftime("%d/%m/%Y")
        fecha = datetime.strptime(fecha, "%d/%m/%Y")

        lista = []
        if empresa == 'todas':
            for men in self.mensajes:
                if men.fecha == fecha:
                    buscar = 0
                    for clasificar in lista:
                        if clasificar['nombre'] == men.empresa:
                            clasificar['total'] += 1
                            if men.tipo == 'positivo':
                                clasificar['positivos'] += 1
                            elif men.tipo == 'negatio':
                                clasificar['negativos'] += 1
                            elif men.tipo == 'neutro':
                                clasificar['neutros'] += 1
                            buscar += 1
                    
                    if buscar == 0:
                        positivos = 0
                        negativos = 0
                        neutros = 0
                        if men.tipo == 'positivo':
                            positivos += 1
                        elif men.tipo == 'negativo':
                            negativo += 1
                        elif men.tipo == 'neutro':
                            neutro += 1
                        #Agregamos a diccionario
                        tmpD = {
                            'nombre':men.empresa,
                            'fecha': men.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutrales': neutros,
                        }
                        lista.append(tmpD)
        else:
            for men in self.mensajes:
                if (men.fecha == fecha) and (men.empresa == empresa):
                    print(men.fecha, empresa)
                    buscar = 0
                    for clasificar in lista:
                        if clasificar['nombre'] == men.empresa:
                            clasificar['total'] += 1
                            if men.tipo == 'positivo':
                                clasificar['positivos'] += 1
                            elif men.tipo == 'negativo':
                                clasificar['negativos'] += 1
                            elif men.tipo == 'neutro':
                                clasificar['neutros'] += 1
                            buscar += 1
                    if buscar == 0:
                        print(men.empresa)
                        positivos = 0
                        negativos = 0
                        neutros = 0
                        if men.tipo == 'positivo':
                            positivos += 1
                        elif men.tipo == 'negativo':
                            negativos += 1
                        elif men.tipo == 'neutro':
                            neutro += 1
                        
                        tmpD = {
                            'nombre':men.empresa,
                            'fecha': men.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutrales': neutros,
                        }
                        lista.append(tmpD)
        reportePor_Fechas = {
            'lista': lista,
            'fecha': fecha
        }         
        print(reportePor_Fechas)
        self.reportePor_Fechas = reportePor_Fechas
        return(reportePor_Fechas)

    def clasificarRango_Fecha(self, f1, f2, empresa):
        lista2 = []
        #----> pasando a formato de fecha ambas variables de fecha
        f1 = str(f1).replace('-','/')
        f1 = datetime.strptime(f1, "%Y/%m/%d")
        f1 = f1.strftime("%d/%m/%Y")
        f1 = datetime.strptime(f1, "%d/%m/%Y")

        f2 = str(f2).replace('-','/')
        f2 = datetime.strptime(f2, "%Y/%m/%d")
        f2 = f2.strftime("%d/%m/%Y")
        f2 = datetime.strptime(f2, "%d/%m/%Y")

        for men in self.mensajes:
            if (men.fecha >= f1) and (men.fecha <= f2):
                if empresa == 'todas':
                    buscar = 0
                    for i in lista2:
                        if (i['nombre'] == men.empresa) and (i['fecha'] == men.fecha):
                            buscar += 1
                    if buscar == 0:
                        positivos = 0
                        negativos = 0
                        neutros = 0
                        if men.tipo == 'positivo':
                            positivos += 1
                        elif men.tipo == 'negativo':
                            negativos += 1
                        elif men.tipo == 'neutro':
                            neutros += 1
                        tmpD = {
                            'nombre':men.empresa,
                            'fecha': men.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutrales': neutros,
                        }
                        lista2.append(tmpD)
                    else:
                        for i in lista2:
                            if (i['nombre'] == men.empresa) and (i['fecha'] == men.fecha):
                                i['total'] += 1
                                if men.tipo == 'positivo':
                                    i['positivo'] += 1
                                elif men.tipo == 'negativo':
                                    i['negativo'] += 1
                                elif men.tipo == 'neutro':
                                    i['neutro'] += 1
                else:
                    buscar = 0
                    for i in lista2:
                        if (i['nombre'] == men.empresa == empresa) and (i['fecha'] == men.fecha):
                            buscar += 1
                        if buscar == 0 and men.empresa == empresa:
                            positivos = 0
                            negativos = 0
                            neutros = 0
                            if men.tipo == 'positivo':
                                positivos += 1
                            elif men.tipo == 'negativo':
                                negativos += 1
                            elif men.tipo == 'neutro':
                                neutros += 1
                            
                            tmpD = {
                                'nombre':empresa,
                                'fecha': men.fecha,
                                'total': 1,
                                'positivos': positivos,
                                'negativos': negativos,
                                'neutrales': neutros,
                            }
                            lista2.append(tmpD)
                        else:
                            for i in lista2:
                                if i['nombre'] == empresa and i['fecha'] == men.fecha:
                                    i['total'] += 1
                                    if men.tipo == 'positivo':
                                        i['positivos'] += 1
                                    elif men.tipo == 'negativo':
                                        i['negativos'] += 1
                                    elif men.tipo == 'neutro':
                                        i['neutros'] += 1
        reporteIntervalo_Fechas = {
            'lista': lista2
        }
        self.reporteIntervalo_fechas = reporteIntervalo_Fechas
        return(reporteIntervalo_Fechas)

    def retornoEmpresas(self):
        diccionario = {

        }
        for e in self.empresas:
            print(e.nombre)
            diccionario.append(e.nombre)
        print(diccionario)
        return(diccionario)
