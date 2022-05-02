#---------importación de librerias---------
from flask import Flask, jsonify, request
from xml.etree import ElementTree as ET
import lxml.etree
from flask_cors import CORS
import re

#----------importación de clases-----------
from ObjMensajes import Mensajes


lista_Positivos = []
lista_Negativos = []
lista_Mensajes = []

#------Cargar y leer archivo xml....... como variable global
#with open('Entrada.xml', encoding='utf-8') as data:
#    file = data.read()
#doc = lxml.etree.fromstring(file)



app = Flask(__name__)
CORS(app)

#-------------pruebas----------------
@app.route('/', methods=['GET'])
def rutaInicial():
    return 'Esto funciona'

@app.route('/', methods=['POST'])
def rutaGuardar():
    objjeto = {"Mensaje": "Prueba en flask"}
    return(jsonify(objjeto))


#------------Funcionalidad--------------
@app.route('/leerXML', methods=['POST'])
def cargarMensajes():
    xml = request.data.decode('utf-8')
    root = ET.XML(xml)
    print(root.tag)
    global doc
    doc = lxml.etree.fromstring(xml)
    lista_Positivos = doc.xpath("//sentimientos_positivos/palabra/text()")
    lista_Negativos = doc.xpath("//sentimientos_negativos/palabra/text()")
    lista_Mensajes = doc.xpath("//lista_mensajes/mensaje/text()")
    nombreEmpresa = doc.xpath("//empresa/nombre/text()")
    #print(lista_Positivos)
    #print(lista_Negativos)
    #print(lista_Mensajes)
    print(doc.xpath("//servicio/alias/text()"))

    return jsonify({'ok':True, 'msg':'Archivo XML leido correctamente'}), 200

@app.route('/obtenerxml', methods=['GET'])
def obternerMensajes():
    listax = doc.xpath("//nombre/text()")
    print(listax)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
