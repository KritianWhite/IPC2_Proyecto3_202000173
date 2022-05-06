'''
import lxml.etree

with open('Entrada.xml', encoding="utf-8") as data:
    a = data.read()

doc = lxml.etree.fromstring(a)
print(doc.xpath("//sentimientos_positivos/palabra/text()"))
#print(doc.xpath("//sentimientos_negativos/palabra/text()"))
#print(doc.xpath("//lista_mensajes/mensaje/text()"))
'''

'''
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
txt += '\t\t\t<empresa nombre=\"'+ empresaS.nombre+'\">\n'
txt += '\t\t\t\t<mensajes>\n'
txt += '\t\t\t\t\t<total> '+ str(empresaS.total) + ' </total>\n'
txt += '\t\t\t\t\t<positivos> '+ str(empresaS.positivo) + ' </positivos>\n'
txt += '\t\t\t\t\t<negativos> '+ str(empresaS.negativo) + ' </negativos>\n'
txt += '\t\t\t\t\t<neutros> '+ str(empresaS.neutro) + ' </neutros>\n'
txt += '\t\t\t\t</mensajes>\n'
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
'''