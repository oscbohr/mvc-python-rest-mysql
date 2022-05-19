'''
Created on 15/05/2022

@author: oscarbohorquez
'''
from repositorio.db import DataSourceMySQL
from sqlalchemy import Column, Integer, Float, String, DateTime

class ItemsRechazadosTB(DataSourceMySQL.Base):
    '''
    classdocs Representa la tabla {ItemsRechazados}
    '''
    __tablename__ = 'ItemsRechazados'
    id = Column(Integer, primary_key = True)
    siteID = Column(String)
    comentario = Column(String)
    fecha_proceso = Column(DateTime)

    def __init__(self, id, siteID, comentario, fecha_proceso): 
        '''
        Constructor Incia parametros
        '''
        self.id = id
        self.siteID = siteID
        self.comentario = comentario
        self.fecha_proceso = fecha_proceso
        
    ''' Metodo que muestra el contendido del objeto '''
    def __str__(self):
        return f'Tipo={type(self)}, id={self.id}, siteID={self.siteID}, Comentario={self.comentario}, Fecha={self.fecha_proceso}'


#***************************************************************************************************************
class ItemsProcesadosTB(DataSourceMySQL.Base):
    '''
    classdocs Representa la tabla {ItemsProcesados}
    '''
    __tablename__ = 'ItemsProcesados'
    id = Column(Integer, primary_key = True)
    site = Column(String)
    siteID = Column(Integer)
    price = Column(Float)
    start_time = Column(String)
    name = Column(String)
    description = Column(String)
    nickname = Column(String)
    
    def get_site(self):
        return self.site

    def get_site_id(self):
        return self.siteID

    def get_price(self):
        return self.price

    def get_start_time(self):
        return self.start_time

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_nickname(self):
        return self.nickname

    def set_site(self, value):
        self.site = value

    def set_site_id(self, value):
        self.siteID = value

    def set_price(self, value):
        self.price = value

    def set_start_time(self, value):
        self.start_time = value

    def set_name(self, value):
        self.name = value

    def set_description(self, value):
        self.description = value

    def set_nickname(self, value):
        self.nickname = value
        
    def __str__(self):
        return f'Tipo={type(self)}, site={self.site}, siteID={self.siteID}, Price={self.price}, Start_time={self.start_time}, Name={self.name}, Description={self.description}, Nickname={self.nickname}'
    
    
#***************************************************************************************************************
class ItemProcesoResp():
    '''
    Constructor Representa un DTO de la tabla {ItemsProcesadosTB}
    '''
    
    #Atributos
    __siteID = ''
    __price = None
    __start_time = ''
    __item_categoria = ''
    __item_moneda = ''
    __item_vendedor = None
    __mensaje = ''
    __is_completo = True

    ''' getter/setter'''
    def get_siteID(self):
        return self.__siteID
    
    def get_price(self):
        return self.__price

    def get_start_time(self):
        return self.__start_time

    def get_item_categoria(self):
        return self.__item_categoria

    def get_item_moneda(self):
        return self.__item_moneda

    def get_item_vendedor(self):
        return self.__item_vendedor
    
    def get_mensaje(self):
        return self.__mensaje
    
    def get_is_completo(self):
        return self.__is_completo

    def set_siteID(self, value):
        self.__siteID = value
        
    def set_price(self, value):
        self.__price = value

    def set_start_time(self, value):
        self.__start_time = value

    def set_item_categoria(self, value):
        self.__item_categoria = value

    def set_item_moneda(self, value):
        self.__item_moneda = value

    def set_item_vendedor(self, value):
        self.__item_vendedor = value
    
    def set_mensaje(self, value):
        self.__mensaje = value
        
    def set_is_completo(self, is_completo):
        self.__is_completo = is_completo
        
    ''' Metodo que muestra el contendido del objeto '''
    def __str__(self):
        return f'SiteID={self.__siteID}, Price={self.__price}, StartTime={self.__start_time}, CategoryID={self.__item_categoria}, MonedaID={self.__item_moneda}, VendedorID={self.__item_vendedor}, Mensaje={self.__mensaje}, IsCompleto={self.__is_completo}'
