'''
Created on 15/05/2022

@author: oscarbohorquez
'''
from dataclasses import dataclass
from _datetime import datetime
import string


@dataclass(unsafe_hash=True)
class ArchivoLectura(object):
    '''
    classdocs Representa el archivo a leer
    '''
    
    #Atributos clase
    __nombreArchivo = ''
    __formatoArchivo =''
    __separadorArchivo = ''
    __encodingArchivo = ''
    
    '''
    Constructor
    '''
    def __init__(self, nombreArchivo, formatoArchivo, separadorArchivo, encodingArchivo):
        self.__nombreArchivo = nombreArchivo
        self.__formatoArchivo = formatoArchivo
        self.__separadorArchivo = separadorArchivo
        self.__encodingArchivo = encodingArchivo
    
    ''' getter/setter '''
    @property
    def nombre_archivo(self):
        return self.__nombreArchivo
    
    @nombre_archivo.setter
    def nombre_archivo(self, nombreArch):
        self.__nombreArchivo = nombreArch
        
    @property
    def formato_archivo(self):
        return self.__formatoArchivo
    
    @formato_archivo.setter
    def formato_archivo(self, formatoArch):
        self.__formatoArchivo= formatoArch
        
    @property
    def separador_archivo(self):
        return self.__separadorArchivo

    @separador_archivo.setter
    def separador_archivo(self, separadorArch):
        self.__separadorArchivo= separadorArch
        
    @property
    def encoding_archivo(self):
        return self.__encodingArchivo

    @encoding_archivo.setter
    def encoding_archivo(self, encodingArch):
        self.__encodingArchivo = encodingArch
        
    ''' Metodo que muestra el contendido del objeto '''
    def __str__(self):
        return f'Tipo={type(self)}, Nombre={self.__nombreArchivo}, Formato={self.__formatoArchivo}, Separador={self.__separadorArchivo}, Encoding={self.__encodingArchivo}'
        
    
    
@dataclass(unsafe_hash=True)
class ResponseHttpProcesadorArchivo:
    '''
    Representa un json de response http 
    '''
    procesado : bool
    tiempo: datetime
    cantidad: int
    mensaje: string
    
@dataclass(unsafe_hash=True)    
class ResponseHttpItemProcesado:
    '''
    Representa un registro de ItemsProcesadosTB serializado para JSON
    '''
    site : string
    siteID : int
    price : float
    start_time : string
    name : string
    description : string
    nickname : string
