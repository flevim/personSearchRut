from flask import Flask, jsonify, request
import cloudscraper
import requests
from rutpy import clean, validate, format_rut
from utils import get_fields, get_results, scrap_text_res
from helpers import getDataRutificador, getDataSII

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


@app.route('/')
def tutorial():
    return 'Hola. para utilizar esta API debes consultar por rut: /consulta?rut=12345678-9' 

@app.route('/consulta', methods=['GET'])
def request_data():
    rut_param = request.args.get('rut')
    
    if rut_param:
        return get_data_by_rut(rut_param)
    
    else:
        return jsonify({
            "status": 400,
            "error": "Debe indicar el parámetro: rut"
        }), 400

def get_data_by_rut(rut):
    data_scrapping_src = getDataRutificador.get_data_by_scrapping(rut, sources['rutificador'], headers_rutificador)
    data_api_src = getDataSII.getProfileSII(rut, sources['sii'], headers_sii)
    combined_data = {**data_scrapping_src, **data_api_src}
    
    return jsonify(combined_data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)

