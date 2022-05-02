
import lxml.etree

with open('Entrada.xml', encoding="utf-8") as data:
    a = data.read()

doc = lxml.etree.fromstring(a)
print(doc.xpath("//sentimientos_positivos/palabra/text()"))
#print(doc.xpath("//sentimientos_negativos/palabra/text()"))
#print(doc.xpath("//lista_mensajes/mensaje/text()"))