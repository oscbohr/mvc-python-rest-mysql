'''
Created on 15/05/2022

@author: oscarbohorquez
'''
import configparser
import psutil

class ConfigProperties(object):
    '''
    Configuración de parametros del sistema
    classdocs
    '''
    __archivo_params = []
    __db_params = []
    __api_meli = []

    def __init__(self):
        '''
        Constructor
        '''
        config = configparser.ConfigParser()
        config.read('config.properties')
        self.__archivo_params = config['archivo']
        self.__db_params = config['db']
        self.__api_meli = config['api_meli']
        
    def get_param_archivo(self, mKey):
        '''
        Permite obtener el valor del parametro
        '''
        mValor = self.__archivo_params[mKey]
        return mValor
    
    def get_param_db(self, mKey):
        '''
        Permite obtener el valor del parametro
        '''
        mValor = self.__db_params[mKey]
        return mValor
    
    def get_param_apiML(self, mKey):
        '''
        Permite obtener el valor del parametro
        '''
        mValor = self.__api_meli[mKey]
        return mValor
    
    
class MonitoringOS(object):
    
    def monitoring(self, artefacto):
        cad1 = artefacto + '\n\t\tPorcentaje de uso de CPU : ' + str(psutil.cpu_percent(1)) +  '\n\tRAM memory % usada:' + str(psutil.virtual_memory()[2])
        return cad1
        
    def monitoringConsole(self, artefacto):
        print('*************************************************')
        print('',artefacto,'')
        print('*************************************************')
        print('Porcentaje de uso de CPU : ', psutil.cpu_percent(1)) 
        print('RAM memory % usada:', psutil.virtual_memory()[2])
        

        
    