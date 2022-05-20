'''
Created on 15/05/2022
Implementación de la capa de servicios
@author: oscarbohorquez
'''
from dominio.abstractas.intefacesNegocio import IOperacionesServices
from dominio.modelo.entry_points import ResponseHttpProcesadorArchivo,\
    ResponseHttpItemProcesado
from dominio.modelo.excepciones import ExceptionConfiguracionApp
from servicio.servicioarchivos import ServicioArchivos
from repositorio.abstractas.impl.RepositorioML import RepositorioML
from util.utilidades import ConfigProperties, MonitoringOS
from repositorio.modelo.entidades import ItemsRechazadosTB
import pandas as m_pandas
import datetime
import time
from servicio.ClienteApiRestML import ClienteApiRestML
import logging

class ServicioProcesarArchivo(IOperacionesServices):
    '''
    Operacion de negocio para 
    - Procesar el archivo (inserta rechazados
    - Eliminar el procesamiento
    - Retornar un muestreo
    classdocs
    '''
    __param_archivo = ['ruta', 'formato', 'separador', 'encoding', 'chunksize'] 
    srv_archivo = ServicioArchivos()
    __repositorio = RepositorioML()
    config_params = ConfigProperties()
    __cliente_api_ml = ClienteApiRestML()
    __mon = MonitoringOS()
    
    def procesarRegistros(self):
        '''
        Metodo para procesar un archivo. Realiza la lectura del archivo por medio de bloques determinado por {chunksize}.
            - Por cada bloque realiza la validación de tipo de dato de (id y site), si no corresponden se van a rechazados. 
            Si son viables, se llama a {ClienteApiRestML} para que inicie el consumo de apisML
        '''
        # Empezar a contar el tiempo del procesamiento del archivo.
        start_time = time.time()
        #Cantidad de registros leidos
        contador = 0
        try:
            logging.info(self.__mon.monitoring('ServicioProcesarArchivo.py ==> procesarRegistros() inicio'))
            archivo = self.srv_archivo.crearArchivo(self.config_params.get_param_archivo(self.__param_archivo[0]), self.config_params.get_param_archivo(self.__param_archivo[1]), \
                        self.config_params.get_param_archivo(self.__param_archivo[2]), self.config_params.get_param_archivo(self.__param_archivo[3]))
            #Lectura del archivo por bloques utilizando {pandas}
            with m_pandas.read_csv(archivo.nombre_archivo + '.' + archivo.formato_archivo, encoding=archivo.encoding_archivo, 
                                   sep=archivo.separador_archivo, chunksize=int(self.config_params.get_param_archivo(self.__param_archivo[-1])) , 
                                   header=0) as reader:            
                for chunk in reader:
                    list_id_procesar = []
                    list_id_rechazos = []

                    for row in chunk.itertuples():
                        contador += 1
                        if str(row.id).strip().isnumeric() :
                            list_id_procesar.append(str(row.site) + str(row.id))
                        else:
                            list_id_rechazos.append(str(row.site) + str(row.id))
                    self.__salvarRechazadosDB(list_id_rechazos)
                    logging.info('Procesando lote de ' + str(len(list_id_procesar)) + ' registros en ' + str(self.config_params.get_param_apiML('hilos_primario')) + ' hilos ')
                    self.__cliente_api_ml.consultarItemsML(list_id_procesar)
        except KeyError as err:
            print(f'Error {err}')
            raise ExceptionConfiguracionApp("Exception de Configuración. Revisar el archivo de config.properties. "+ str(type(err))+str(err))
        except FileNotFoundError as err:
            print(f'Error {err}')
            raise ExceptionConfiguracionApp("Exception de Configuración. Revisar el archivo de config.properties para la ruta del archivo. "+ str(type(err))+str(err))
        finally:
            respHttp = ResponseHttpProcesadorArchivo(True, (time.time() - start_time), contador, 'Ok')     
        self.__mon.monitoring('ServicioProcesarArchivo.py ==> procesarRegistros() Fin')       
        return respHttp
        
    
    def eliminarRegistros(self):
        '''
        Permite eliminar los cargues (realiza un delete All en la BD)
        '''
        self.__mon.monitoring('ServicioProcesarArchivo.py ==> eliminarRegistros() Inicio')
        start_time = time.time()
        rows_delete = self.__repositorio.eliminarRegistros()
        
        self.__mon.monitoring('ServicioProcesarArchivo.py ==> eliminarRegistros() Fin')
        return ResponseHttpProcesadorArchivo(True, (time.time() - start_time), rows_delete, 'Ok')
    
    def muestreoRegistros(self, rows):
        '''
        Permite retornar una lista de tamaño {rows} de registros procesados        
        '''
        self.__mon.monitoring('ServicioProcesarArchivo.py ==> muestreoRegistros() Inicio')
        lista_response = []
        lista_tabla = self.__repositorio.consultarItems(rows)
        for item_tb in lista_tabla:
            lista_response.append(ResponseHttpItemProcesado(item_tb.get_site(), 
                            item_tb.get_site_id(), item_tb.get_price(), item_tb.get_start_time(), 
                            item_tb.get_description(), item_tb.get_name(), item_tb.get_nickname()))
        self.__mon.monitoring('ServicioProcesarArchivo.py ==> muestreoRegistros() Inicio')
        return lista_response

    def __salvarRechazadosDB(self, list_rechazos):
        '''
        Permite insetar en la tabla de rechazados        
        '''
        lista_tb_rechazados = []
        for id_rechazo in list_rechazos:
            lista_tb_rechazados.append(ItemsRechazadosTB(None, id_rechazo, "Tipo de Dato", datetime.datetime.now()))
        self.__repositorio.persistirLista(lista_tb_rechazados)
    
    
    