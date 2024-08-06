import os
import logging
from flask import Blueprint, request
from requests.exceptions import HTTPError
import requests
from shared.database.basedatos import database


LOG = logging.getLogger(__name__)
consultarprocesos_bp = Blueprint('consultarprocesos', __name__)


def armarurl(idtenant: str, sw_next_page: bool, nextPageKey: str):
    if sw_next_page:
        url = f'''{os.environ['URLINICIO']}{os.environ['IP']}:{
            os.environ['PUERTO']}{os.environ['LLAMADA_ROUTER']}{idtenant}&api={
                os.environ['APIPROCESOSNEXTPAGE']}{nextPageKey}'''

    if not sw_next_page:
        url = f'''{os.environ['URLINICIO']}{os.environ['IP']}:{
            os.environ['PUERTO']}{os.environ['LLAMADA_ROUTER']}{idtenant}&api={
                os.environ['APIPROCESOS']}'''

    return url


def Consultar_procesos(idtenant: str, sw_next_page: bool, nextPageKey: str):
    try:
        url = armarurl(idtenant, sw_next_page, nextPageKey)
        response = requests.request('GET', url)
        response.raise_for_status
    except TimeoutError as tO_err:
        LOG.error(f'Error de timeout al consumir la api. {tO_err}')
    except HTTPError as http_err:
        LOG.error(f'Error al consumir la api. {http_err}')
    except Exception as err:
        LOG.error(f'Error al consumir la api. {err}')
    else:
        return response.status_code, response.json()


def validarnextpage(nextPageKey):
    try:
        sw_next_page = True
        if nextPageKey == '' or nextPageKey is None:
            sw_next_page = False
    except Exception as err:
        sw_next_page = False
        LOG.error(f'Error al consumir la api. {err}')
    else:
        return sw_next_page


def guardarbd(data, status_code):
    LOG.info(f'Codigo respuesta: {status_code}')
    try:
        db = database()
        db.ingresardatos(data)
    except Exception as err:
        LOG.error(f'Error al invocar la base de datos. {err}')


@consultarprocesos_bp.route('/procesos', methods=['GET'])
def procesos():
    try:
        idtenant = request.args.get('idtenant', '''Falta indicar el tenant
                                    a conectar''')
        status_code, respuesta = Consultar_procesos(idtenant, False, '')
        guardarbd(respuesta.get('entities'), status_code)
        nextPageKey = respuesta.get('nextPageKey')
        sw_nextpage = validarnextpage(nextPageKey)

        while sw_nextpage is True:
            if nextPageKey is not None:
                nextPageKey = nextPageKey.replace('=', '(%3D)')

            status_code, respuesta = Consultar_procesos(idtenant, sw_nextpage,
                                                        nextPageKey)
            guardarbd(respuesta.get('entities'), status_code)
            nextPageKey = respuesta.get('nextPageKey')
            if nextPageKey is not None:
                nextPageKey = nextPageKey.replace('=', '(%3D)')
                sw_nextpage = validarnextpage(nextPageKey)

            if nextPageKey is None:
                sw_nextpage = False
    except Exception as err:
        error = f'Error al consumir la api. {err}'
        LOG.error(error)
        respuesta = error.json()
    else:
        return respuesta
