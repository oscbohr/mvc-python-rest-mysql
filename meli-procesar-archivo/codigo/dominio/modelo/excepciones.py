'''
Created on 15/05/2022

@author: oscarbohorquez
'''

class ExceptionConfiguracionApp(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class RespuestaHTTPException(Exception):
    def __init__(self, statusCode, message):
        self.statusCode = statusCode
        self.message = message
        super().__init__(message)
        