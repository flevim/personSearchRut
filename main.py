from flask import Flask, jsonify, request
import cloudscraper
import requests
from rutpy import clean, validate, format_rut
from utils import get_fields, get_results, scrap_text_res
from sii_source import SIISource
from rutificador_source import RutificadorSource
from source_fetcher import SourceFetcher

# config 
app = Flask(__name__)
app.json.sort_keys = False
port = 5000

# HTTP config 
headers_rutificador = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

headers_sii = { "Content-Type": "application/x-www-form-urlencoded" }
sources = {
    'rutificador': 'https://www.nombrerutyfirma.com',
    'sii': 'https://zeus.sii.cl/cvc_cgi/stc/getstc',
}


@app.route('/consulta', methods=['GET'])
def request_data():
    rut_param = request.args.get('rut')
    if rut_param:
        if not validate(rut_param.lstrip('0')):
            return {
                'status': 400,
                'data': {
                    'error': 'Rut invalido.'
                }
                
        }
    
        return get_data_by_rut(rut_param)
    
    else:
        return jsonify({
            "status": 400,
            "error": "Debe indicar el parámetro: rut"
        }), 400

def get_data_by_rut(rut):
    rutificador_src = RutificadorSource(rut, sources['rutificador'], headers_rutificador)
    sii_src = SIISource(rut, sources['sii'], headers_sii)
    source_fetcher = SourceFetcher()
    
    #source_fetcher.add_source(rutificador_src)
    source_fetcher.add_source(sii_src)
    profile = source_fetcher.fetch_source(rut)

    return jsonify(profile), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)

