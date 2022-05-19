'''
Created on 16/05/2022

@author: oscarbohorquez
'''
from repositorio.abstractas.IRepositorioML import IRepositorioML
from repositorio.modelo.entidades import ItemsRechazadosTB, ItemsProcesadosTB
from repositorio.db import DataSourceMySQL


class RepositorioML(IRepositorioML):
    '''
    classdocs Repositorio sobre la Fuente de Datos para realizar
        las diferentes operaciones
    '''
    __repositorio = DataSourceMySQL()

    def persistirLista(self, lista_tb_rechazados):
        '''
        Permite persistir los items rechazados
        '''
        for item_tabla in lista_tb_rechazados:
            self.persistirItem(item_tabla)
        
    def eliminarRegistros(self):
        session = self.__repositorio.session_factory();
        rows_delete  = int(session.query(ItemsRechazadosTB).delete()) + int(session.query(ItemsProcesadosTB).delete())
        session.commit()
        return rows_delete
        
    def persistirItem(self, item_tabla):
        session = self.__repositorio.session_factory();
        session.add(item_tabla)
        session.commit()
        
    def consultarItems(self, rows):
        session = self.__repositorio.session_factory();
        lista_procesados = session.query(ItemsProcesadosTB).limit(int(rows)).all()
        return lista_procesados
    
        
    