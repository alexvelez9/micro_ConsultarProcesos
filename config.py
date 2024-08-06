import os
from dotenv import load_dotenv


"""carga archivo donde se encuentran las variables de entorno."""
dotenv_file_path = os.path.join(os.path.dirname(__name__), '.env')
if os.path.exists(dotenv_file_path):
    load_dotenv(dotenv_file_path)


class Config:
    """Clase para la cargar las variables de entorno.

    Keyword arguments:
    argument -- None
    Return: None
    """
    pass


class DevelopmentConfig(Config):
    """Clase para cargar la variable de ambiente de desarrollo.

    Keyword arguments:
    argument -- None
    Return: None
    """
    ENV = "development"


class ProductionConfig(Config):
    """Clase para cargar la variable de ambiente de produccion.

    Keyword arguments:
    argument -- None
    Return: None
    """
    ENV = "production"
