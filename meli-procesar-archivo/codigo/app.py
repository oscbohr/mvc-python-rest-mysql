'''
Created on 15/05/2022
Main de la app con FLASK
@author: oscarbohorquez
'''

from flask import Flask, jsonify, request
from servicio.servicioprocesararchivo import ServicioProcesarArchivo
from util.utilidades import MonitoringOS
import logging

app = Flask(__name__)
mon = MonitoringOS()
servicio_operac = ServicioProcesarArchivo()

@app.route("/api/v1/procesararchivo", methods=['POST'])
def procesar_archivo():
    '''
    Procesar archivo: Permite leer el archivo y procesarlo

    curl --header "Content-Type: application/json" --request POST \
         --data '{}' \
         http://localhost:5000/api/v1/procesararchivo

    :return: json
    '''
    #mon.monitoringConsole('app.py => procesar() Inicio')
    logging.info(mon.monitoring('app.py => procesar() Inicio'))
    print('app.py => procesar() Inicio')
    respProcArc = servicio_operac.procesarRegistros()
    responseHTTP = jsonify(respProcArc)
    logging.info(mon.monitoring('app.py => procesar() Fin'))
    #mon.monitoring('app.py => procesar() Fin')
    print()
    return responseHTTP, 200

@app.route("/api/v1/eliminarprocesoarchivo", methods=['DELETE'])
def eliminar_proceso():
    '''
    Procesar archivo: Permite leer el archivo y procesarlo

    curl --header "Content-Type: application/json" --request DELETE \
         --data '{}' \
         http://localhost:5000/api/v1/procesararchivo/delete

    :return: json
    '''
    #mon.monitoring('app.py => eliminar_proceso() Inicio')
    logging.info(mon.monitoring('app.py => eliminar_proceso() Inicio'))
    respDelete = servicio_operac.eliminarRegistros()
    responseHTTP = jsonify(respDelete)
    logging.info(mon.monitoring('app.py => eliminar_proceso() Fin'))
    return responseHTTP, 200

@app.route("/api/v1/procesararchivo", methods=['GET'])
def consultar():
    '''
    Consultar proceso: Permite obtener los registros procesos (registros bien)

    curl --header "Content-Type: application/json" --request GET\
         --data '{}' \
         http://localhost:5000/api/v1/procesararchivo?rows=valor

    :return: list{json}
    '''
    
    argumentos = request.args
    rows = int(argumentos.get('rows'))
    
    logging.info(mon.monitoring('app.py => consultar() Inicio'))
    lista_rows = servicio_operac.muestreoRegistros(rows)
    logging.info(mon.monitoring('app.py => consultar() Fin'))
    return jsonify(lista_rows), 200
    

if __name__ == '__main__':
    logging.basicConfig(filename='challengOMBR-Loggin.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Iniciando...')
    app.run( debug=True, port = 5000, host='0.0.0.0')
