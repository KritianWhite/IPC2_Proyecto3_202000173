#---------importación de librerias---------
from flask import Flask, jsonify, request
from flask_cors import CORS
#----------importación de clases-----------
from Leer import * 


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
    file = (request.get_data())
    doc = leerXML(file)
    return jsonify({'ok':True, 'msg':'Archivo XML leido correctamente'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
