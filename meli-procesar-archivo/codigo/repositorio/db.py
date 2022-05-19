'''
Created on 15/05/2022

@author: oscarbohorquez
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util.utilidades import ConfigProperties
from dominio.modelo.excepciones import ExceptionConfiguracionApp


class DataSourceMySQL(object):
    '''
    classdocs Representa el DataSource a la fuente de datos
    '''
    __config_params = ConfigProperties()
    __SessionFactory = None
    __engine = None
    Base = declarative_base()
    
    def __init__(self):
        '''
        Constructor
        '''
        print('CRANDOOOOOOOOOOOOOOOOOOOOO')
        try:
            self.__engine = create_engine(self.__config_params.get_param_db('url'), pool_size = int(self.__config_params.get_param_db('pool_size')))
            self.__SessionFactory= sessionmaker(bind=self.__engine)
        except KeyError as err:
            print(f'Error {err}')
            raise ExceptionConfiguracionApp("Exception de Configuración. Revisar el archivo de config.properties. "+ str(type(err))+str(err)) 
        
        
    def session_factory(self):
        '''
        Retorna una session del DataSource
        '''
        self.Base.metadata.create_all(self.__engine)
        return self.__SessionFactory()
        