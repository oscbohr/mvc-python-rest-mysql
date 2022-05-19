'''
Created on 16/05/2022

@author: oscarbohorquez
'''
import abc

class IRepositorioML(metaclass=abc.ABCMeta):
    '''
        classdocs Interface para las operaciones en el repositorio:
        - Procesar salvarRegistrados
        - Eliminar los registros
        - Retornar un muestreo del items procesados
    '''
    @abc.abstractmethod
    def persistirLista(self, list_id_rechazos):
        '''
        Permite salvar una lista en la tabla "ItemsRechazados 
        '''
    @abc.abstractmethod
    def eliminarRegistros(self):
        '''
        Permite eliminar los datos de la tabla ItemsProcesados
        
        '''
        
    @abc.abstractclassmethod
    def persistirItem(self, item_tabla):
        '''
        Permite insertar un solo registro en la tabla "ItemsRechazados
        '''

    @abc.abstractclassmethod
    def consultarItems(self, rows):
        '''
        Permite insertar un solo registro en la tabla "ItemsRechazados
        '''