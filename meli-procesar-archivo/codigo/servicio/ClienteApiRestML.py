'''
Created on 16/05/2022

@author: oscarbohorquez
'''
import concurrent.futures
import datetime
import requests;
import traceback
from util.utilidades import ConfigProperties
from dominio.modelo.excepciones import ExceptionConfiguracionApp,\
    RespuestaHTTPException
from repositorio.modelo.entidades import ItemProcesoResp, ItemsRechazadosTB,\
    ItemsProcesadosTB
from repositorio.abstractas.impl.RepositorioML import RepositorioML

class ClienteApiRestML(object):
    '''
    classdocs Cliente para consumir el API de Mercado Libre (ML)
    ''' 
    #URL primaria de ML (consultar items)
    __url_primaria = ''
    '''
    URL Secundarias de ML. Se dicen secundarias ya que dependen del resultado de la ulr primaria
    '''
    __url_secundaria =[]
    #Objeto para traer la configuracion de parametros para: Archivos, DB, api, etc
    __config_params = ConfigProperties()
    #Repositorio para persistir
    __repositorio = RepositorioML()
    

    def __init__(self):
        '''
        Constructor Obtiene la URLs a consultar
        '''
        try:
            self.__url_primaria = self.__config_params.get_param_apiML('url_primaria')
            self.__url_secundaria = self.__config_params.get_param_apiML('url_secundarias').split(',')
        except KeyError as err:
            print(f'Error {err}')
            raise ExceptionConfiguracionApp("Exception de Configuración. Revisar el archivo de config.properties. "+ str(type(err))+str(err)) 
        

    def consultarItemsML(self, lista_ids):
        '''
        Metodo para consultar la información: Con {lista_ids} lanza {max_workers} para llamar al metodo que realiza 
            el consumo de la {url_primaria} en paralelo.
            :param lista_ids Lista de {site+ID} 
        '''
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(self.__config_params.get_param_apiML('hilos_primario'))) as executor:
            # Inicie las operaciones de consulta y marque cada future con su siteID
            future_to_siteID = {executor.submit(self.__consumirApiItems, siteID): siteID for siteID in lista_ids}
            for future in concurrent.futures.as_completed(future_to_siteID):
                siteID = future_to_siteID[future]
                try:
                    data = future.result()
                except Exception as err:
                    print(f'Error ThreadPoolExecutor Primario ==> {err}')
                    print(traceback.print_exc())
    
                    
    def __consumirApiItems(self, siteID):
        '''
        Permite realizar el consumo de {url_primaria (itemsML)}. Valida que por lo menos tenga el tag <price> y <start_time>
            para marcarlo como viable (para consumir url_secundaria). Crea una lista {item_proceso_resp} con la info solicitada (price, seller_id, category_id, etc)
        :param siteID: Input del servicio ur_items
        '''
        args = {'ids' : siteID}
        item_proceso_resp = ItemProcesoResp()
        response = requests.get(self.__url_primaria, args)     
        if response.status_code == 200:
            payload = response.json()
            lista_tags = payload[0]
            body = lista_tags['body']
            mensaje = ''
            try :
                item_proceso_resp.set_siteID(siteID)
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            try:
                item_proceso_resp.set_price(body['price'])
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            try:
                item_proceso_resp.set_start_time(body['start_time'])
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            try:
                item_proceso_resp.set_item_categoria(body['category_id'])
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            try:
                item_proceso_resp.set_item_moneda(body['currency_id'])
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            try:
                item_proceso_resp.set_item_vendedor(int(body['seller_id']))
            except Exception as err:
                mensaje = ' ' + mensaje + ' ' + str(err)
            item_proceso_resp.set_mensaje('Response sin <<tag>>' + mensaje.strip())
            item_proceso_resp.set_is_completo(item_proceso_resp.get_price() is not None and len(item_proceso_resp.get_start_time()) >0)
            
            self.__prepararApisSecundarias(item_proceso_resp)
            
        elif response.status_code == 404:
            raise RespuestaHTTPException(response.status_code,"Error al llamar al servicio solicitado: ")
        return None
    
    
    def __prepararApisSecundarias(self, item_procesos_resp):
        '''
        Permite preparar el consumo de {url_secundarias (categorias, monedas, user de ML)} concurrentemente dada la cantidad de {max_workers} . 
            Crea los endPoints finales para cada {item_procesos_resp}. 
        :param item_procesos_resp: contiene informacion (categoria_id, seller_id, etc) para input de {url_secundaria}
        '''
        #Es un item viable si contiene como minimo el tag <price> y <start_time>. 
        #Si no es viable se va a rechazados.
        if item_procesos_resp.get_is_completo():
            url_completa = []
            for item in self.__url_secundaria:
                if 'categories' in item:
                    url_completa.append(item + item_procesos_resp.get_item_categoria())
                elif 'currencies' in item:
                    url_completa.append(item + item_procesos_resp.get_item_moneda())
                elif 'users' in item:
                    url_completa.append(item + str(item_procesos_resp.get_item_vendedor()))
            
            item_tabla = ItemsProcesadosTB()
            item_tabla.site = item_procesos_resp.get_siteID()[0: 3]
            item_tabla.siteID = int(item_procesos_resp.get_siteID()[3:len(item_procesos_resp.get_siteID())])
            item_tabla.price = item_procesos_resp.get_price()
            item_tabla.start_time = item_procesos_resp.get_start_time()
            item_tabla.id = None
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(self.__config_params.get_param_apiML('hilos_secundario'))) as executor:
                future_to_url = {executor.submit(self.__consumirApisSecundarias, url, item_procesos_resp, item_tabla): url for url in url_completa}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as err:
                        print(f'Error ThreadPoolExecutor Secundario ==> {err} ')
                        traceback.print_exc()
            self.__salvarProcesadosDB(item_tabla)
        else:
            self.__salvarRechazadosDB(item_procesos_resp)
        
    
    def __consumirApisSecundarias(self, url, item_procesos_resp, item_tabla):
        '''
        Permite consumir las apis secundarias (categorias, monedas, vendedores)
        :param item_procesos_resp input de api
        :param item_tabla: Representa un registro en procesados
        '''
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()  
            if 'categories' in url:
                item_tabla.name = payload['name']
            elif 'currencies' in url:
                item_tabla.description = payload['description']
            elif 'users' in url:
                lista_tags = payload[0]
                body = lista_tags['body']
                item_tabla.nickname = body['nickname']
            
        elif response.status_code == 404:
            raise RespuestaHTTPException(response.status_code,"Error al llamar al servicio solicitado: ")
        
    
    def __salvarRechazadosDB(self, item_procesos_resp):
        '''
        Permite persistir en la tabla de rechazados
        :param item_procesos_resp informacion a persistir
        '''
        item_rechazado_tb = ItemsRechazadosTB(None, item_procesos_resp.get_siteID(), item_procesos_resp.get_mensaje(), datetime.datetime.now())
        self.__repositorio.persistirItem(item_rechazado_tb)
    
        
    def __salvarProcesadosDB(self, item_tabla):
        '''
        Permite persistir en la tabla de procesados
        :param item_tabla Registro de la tabla
        '''
        self.__repositorio.persistirItem(item_tabla)
         
         
            
        
    
    
            