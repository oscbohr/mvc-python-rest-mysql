'''
Created on 15/05/2022
Inteface 
@author: oscarbohorquez
'''
import abc

class IArchivosLectura(metaclass=abc.ABCMeta):
    '''
    classdocs Interface para archivos
    '''
    @abc.abstractmethod
    def crearArchivo(self, nombre, formato, separador, encoding):
        '''
        Permite crear archivos con diferentes formatos, separadores y encoding
        '''
        
class IOperacionesServices(metaclass=abc.ABCMeta):
    '''
    classdocs Interface para las operaciones de Negocio:
        - Procesar Archivo
        - Eliminar los registros
        - Retornar un muestreo del items procesados
    '''
    @abc.abstractmethod
    def procesarRegistros(self):
        '''
        Permite crear archivos con diferentes formatos, separadores y encoding
        '''
        
    @abc.abstractmethod
    def eliminarRegistros(self):
        '''
        Permite eliminar los registros de un proceso
        '''
    
    @abc.abstractmethod
    def muestreoRegistros(self, cantidad_registros=100):
        '''
        Permite retornar un muestreo de data procesada
        '''
        
        