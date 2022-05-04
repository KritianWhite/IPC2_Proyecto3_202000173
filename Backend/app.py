#---------importación de librerias---------
from django.urls import clear_script_prefix
from flask import Flask, jsonify, request
from flask_cors import CORS
#----------importación de clases-----------
from Leer import * 


app = Flask(__name__)
CORS(app)

admin = Analizar()

#-------------pruebas----------------
@app.route('/', methods=['GET'])
def rutaInicial():
    return 'Esto funciona'

@app.route('/', methods=['POST'])
def rutaGuardar():
    objjeto = {"Mensaje": "Prueba en flask"}
    return(jsonify(objjeto))


#------------Funcionalidad--------------
@app.route('/home', methods=['POST'])
def cargarMensajes():
    #file = (request.get_data())
    file = request.data.decode('utf-8')
    doc = leerXML(file) #-----> doc returna una lista de objetos de los mensajes
    #admin.recibirXML(file)
    #admin.Sampar_a_Listas()

    return jsonify({'ok':True, 'msg':'Archivo XML leido correctamente'}), 200

@app.route('/home', methods=['GET'])
def obtenerSalia():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000, debug=True)
