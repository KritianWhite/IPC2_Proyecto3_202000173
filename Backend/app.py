from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS
from Manager import Adminstrador
from xml.etree import ElementTree as ET

app = Flask(__name__)
app.config["DEBUG"]=True

CORS(app)

admin = Adminstrador()

@app.route('/')
def home():
    return "Todo bien :D"

#Cargar Archivo

@app.route('/carga',methods=['POST'])
def agregarXML():
    xml=request.data.decode('utf-8')
    admin.recibirXML(xml)
    admin.clasificacionMensajes()
    return (jsonify({'ok':True}))

#-------> inicio endpoints
@app.route("/carga", methods = ["POST"])
def CargaMasiva ():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        admin.recorrerXMLl(raiz)
    return jsonify({'ok':True, 'data':raiz.text}),200

@app.route("/carga", methods = ["GET"])
def MostrarSalida():
    return ({'ok':False}),200

@app.route("/peticiones", methods =["GET"] )
def MostrrPetciones ():
    if len(admin.empresas) > 0:
        return jsonify({'data':True})
    else:
        return jsonify({'data':False})

@app.route('/consultar', methods = ['GET'])
def consultar():
    entrada = admin.xml
    salida = admin.salidaXML()
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    return jsonify(data)

@app.route('/generarPDF1', methods = ['POST'])
def pdf1():
    if request.method == "POST":

        entrada = admin.xml
        salida = admin.salidaXML()
        data = {
            'entrada' : entrada,
            'salida': salida
        }
        data = jsonify(data)

        return data

@app.route('/clasificar-por-fecha', methods = ['GET','POST'])
def clasificar():
    if request.method == 'GET':
        #json = request.get_json()
        empresas2 = []
        for em in admin.empresas:
            empresas2.append(em.nombre) 
        return jsonify ({'empresas':empresas2}) #--> solo nombre de empresas

    if request.method == 'POST':
        datos = request.json
        dictionary = admin.clasificacionFecha(datos['fecha'], datos ['empresa'])
        print(dictionary)
        return jsonify(dictionary)

@app.route('/resumen-por-rango', methods = ['GET','POST'])
def rango():
    #Si solo es un get, entondes retornara un listado de empresa para seleccionar
    if request.method == 'GET':
        #json = request.get_json()
        empresas2 = []
        for em in admin.empresas:
            empresas2.append(em.nombre)
        #Rettorna solo los nombre de las empresas
        return jsonify ({'empresas':empresas2})
    #Si es un post, entonces retornara los mensajes totales
    if request.method == 'POST':
        datos = request.json
        dictionary = admin.clasificacionRango_Fecha(datos['fecha1'],datos['fecha2'] , datos ['empresa'])
        print(dictionary)
        return jsonify(dictionary)

@app.route("/reporte2", methods = ['POST'])
def reporte2 ():
    return jsonify(admin.reporte2)

@app.route("/reporte3", methods = ['POST'])
def reporte3 ():
    return jsonify(admin.reporte3)

@app.route("/reporte4", methods = ['POST'])
def reporte4():
    #Se define la entrada como el XML enviado, pero lasalida como una funcion que procesa
    entrada = admin.nose
    salida = admin.reporte4
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    data = jsonify(data)
    return data
    

@app.route("/ayuda", methods = ['GET'])
def MostrarAyuda():
    return jsonify({'1. Nombre':'Christian Alessander Blanco González',
     '2. Carnet': 202000173,"Documentacion" : False})

#Iniciar el servidor
if __name__ == "__main__":
    app.run(port=4000,debug=True)    