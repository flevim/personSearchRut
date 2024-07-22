from rutpy import clean, validate, format_rut
import cloudscraper
import requests
from utils import get_results

def get_data_by_scrapping(rut, src_path, headers):
    full_path = f'{src_path}/rut'
    
    if not validate(rut):
        return {
            'status': 400,
            'error': 'Rut invalido.'
        }
    
    rut = format_rut(rut)

    payload = {'term': rut}
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session, debug=True)
    
    req = scraper.post(full_path, headers=headers, data=payload)
    if req.status_code == 200:
        results = get_results(req)
        if not results:
            return {
                'status': 404,
                'error': 'No se han encontrado resultados',
            }
        
        return {
            'status': 200,
            'error': None,
            'nombre': results[0]['nombre'],
            'rut': results[0]['rut'],
            'sexo': results[0]['sexo'],
            'direccion': results[0]['direccion'],
            'ciudad/comuna': results[0]['ciudad']
        }
    else:
        return {'response': req.text}