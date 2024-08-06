import os
from pymongo import MongoClient
import logging


class database():

    def __init__(self) -> None:
        """Configuracion de la base de datos en mongo

        Keyword arguments:
        argument -- None
        Return: bd (Base de datos en MOngo)
                problemas (coleccion en la base de datos)
        """
        self.__LOG = logging.getLogger(__name__)
        try:
            mongo_uri = f'''mongodb://{os.environ['HOST_DB']}:{
                os.environ['PUERTO_DB']}/{os.environ['NOMBRE_DB']}'''
            client_db = MongoClient(mongo_uri)
            # Base de datos en mongoDB
            bd = client_db[os.environ['NOMBRE_DB']]
            # Coleccion en la base de datos de MongoDB
            self.__coleccion = bd[os.environ['NOMBRE_COLECCION_DB']]
        except Exception as err:
            self.__LOG.error(f'Error al inicializar la base de datos. {err}')

    def ingresardatos(self, datos):
        self.__coleccion.insert_many(datos)
