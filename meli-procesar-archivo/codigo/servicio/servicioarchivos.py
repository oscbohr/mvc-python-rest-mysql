'''
Created on 15/05/2022

@author: oscarbohorquez
'''
from dominio.abstractas.intefacesNegocio import IArchivosLectura
from dominio.modelo.entry_points import ArchivoLectura

class ServicioArchivos(IArchivosLectura):
    '''
    Operacion de negocio para 
        - Procesar el archivo
        - Eliminar el procesamiento
        - Retornar un muestreo
    classdocs
    '''

    def crearArchivo(self, nombre, formato, separador, encoding):
        return ArchivoLectura(nombre, formato, separador, encoding)
    