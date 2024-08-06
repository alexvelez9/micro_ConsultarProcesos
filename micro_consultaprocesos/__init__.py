import os
import logging
from flask import Flask
from blueprints.consultaprocesos.consultaprocesos import (
    consultarprocesos_bp
    )


def configure_logging():
    # register root logging
    try:
        logging.basicConfig(level=logging.DEBUG,
                            encoding=os.environ['ENCODINGLOG'],
                            format=os.environ['LOGFORMAT'],
                            datefmt=os.environ['DATEFORMAT'],
                            filename=os.environ['PATHLOGFILE'],
                            filemode=os.environ['FILEMODE'])
    except FileNotFoundError as fnferr:
        print(f'''Error en DynatraceStatus.__init__.configure_logging():
               {fnferr}''')


def register_bluprints(app):
    """Automagically register all blueprint packages
    Just take a look in the blueprints directory.
    """
    with app.app_context():
        """Aca se registran los blueprints"""
        app.register_blueprint(consultarprocesos_bp)
    return None


def create_app():
    """Crea la aplicacion, es aca donde se conecta toda la app

    Keyword arguments:
    argument -- None
    Return: None
    """
    app = Flask(__name__)
    app.config.from_object(os.environ['CONFIG_SETUP'])
    configure_logging()
    register_bluprints(app)

    return app
