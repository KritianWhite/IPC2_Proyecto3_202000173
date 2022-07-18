
from os import remove
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
    return "Esto funciona :D"

@app.route('/recibir', methods=['GET'])
def imprimir():
    if request.method == 'GET':
        mensajes2 = []
        diccionario = {}
        for mensaje in admin.mensajes:
            diccionario = {
                'lugar' : mensaje.lugar,
                'fecha' : mensaje.fecha,
                'hora' : mensaje.hora,
                'usuario' : mensaje.user,
                'red' : mensaje.red,
                'empresa' : mensaje.empresa,
                'servicio' : mensaje.servicio,
                'contenido' : ' '.join(mensaje.contenido),
                'tipo' : mensaje.tipo
            }
            mensajes2.append(diccionario)
    return  jsonify({'ok':True}, mensajes2)

#Cargar Archivo
@app.route('/CargaMasiva',methods=['POST'])
def Carguita():
    xml=request.data.decode('utf-8')
    admin.recibirXML(xml)
    admin.clasificacionMensajes()
    return (jsonify({'ok':True}))

#-------> inicio endpoints

@app.route("/CargaMasiva", methods=["GET"])
def Carguita2():
    try:
        file = open('BaseDatos.xml', 'r')
        admin.recibirXML(file.read())
        admin.clasificacionMensajes()
        return jsonify({'ok':True, 'msg': admin.salidaXML()}), 200
    except:
        return ({'ok':False, 'msg': 'Algo ocurrió'})

@app.route('/reset',methods=['POST'])
def reset():
    admin.mensajes = []
    admin.empresas = []
    admin.xml = []
    admin.totalMensajes =0
    admin.totalPositivos = 0
    admin.totalNegativos = 0
    admin.totalNeutros = 0
    admin.nose = []
    admin.reporte2 = {}
    admin.reporte3 = {}
    admin.reporte4 = []
    remove("BaseDatos.xml")
    return(jsonify({'ok': True, 'msg':'Reseteo con éxito :D'})), 200


@app.route("/CargaMasiva", methods=["GET"])
def MostrarSalida():
    return ({'ok':False}),200


@app.route("/peticiones", methods=["GET"] )
def MostrrPetciones ():
    if len(admin.empresas) > 0:
        return jsonify({'data':True}), 200
    else:
        return jsonify({'data':False})

@app.route('/consultar', methods=['GET'])
def consultar():
    entrada = admin.xml
    salida = admin.salidaXML()
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    return jsonify(data)

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
        dictionary = admin.clasificacionFecha(datos['date'], datos ['empresa'])
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
        dictionary = admin.clasificacionRango_Fecha(datos['date1'],datos['date1'] , datos ['empresa'])
        print(dictionary)
        return jsonify(dictionary)


@app.route('/generarPDF1', methods = ['POST'])
def pdf1():
    if request.method == "POST":

        entrada = admin.xml
        salida = admin.salidaXML()
        data = {
            'entrada' : entrada,
            'salida': salida
        }

        return jsonify(data)



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
    
@app.route("/prueba-de-mensaje", methods = ['GET'])
def prueba1():
    return jsonify({'ok':'True'})

@app.route("/prueba-de-mensaje", methods = ['POST'])
def prueba2():
    xml2 = request.data.decode('utf-8')
    admin.prueba_mensaje(xml2)
    entrada = str(xml2)
    admin.reporte40 = entrada
    salida = admin.prueba_mensaje(xml2)
    return jsonify({'entrada':entrada, 'salida':salida})

@app.route("/ayuda", methods = ['GET'])
def MostrarAyuda():
    return jsonify({'1. Nombre':'Christian Alessander Blanco González',
     '2. Carnet': 202000173,"Documentacion" : False})

     

#Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True, port=4000)    