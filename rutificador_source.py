from data_source import DataSource
from rutpy import clean, validate, format_rut
import cloudscraper
import requests
from utils import get_results

class RutificadorSource(DataSource):
    def __init__ (self, rut, src_path, headers):
        self.rut = rut
        self.src_path = src_path
        self.headers = headers
    
    def get_profile(self):
        full_path = f'{self.src_path}/rut'
        
        
        rut = format_rut(self.rut)
        
        payload = {'term': rut}
        session = requests.Session()
        # https://github.com/VeNoMouS/cloudscraper -> bypass Cloudflare's anti-bot page
        scraper = cloudscraper.create_scraper(sess=session, debug=True)

        try: 
            req = scraper.post(full_path, headers=self.headers, data=payload, timeout=10)
        
            if req.status_code == 200:
                results = get_results(req)
            
                if not results:
                    return {
                        'status': 404,
                        'data': {
                            'error': 'No se han encontrado resultados'
                        }
                        
                    }
                
                document, dv = results[0]['rut'].split('-')
                return {
                    'status': 200, 
                    'data': {
                        'error': None,
                        'nombre': results[0]['nombre'],
                        'document': clean(document),
                        'dv': dv,
                        'sexo': results[0]['sexo'],
                        'direccion': results[0]['direccion'],
                        'ciudad/comuna': results[0]['ciudad']
                    }
                    
                }
            else:
                return {'status': 400,
                        'data': {
                            'error': 'Ha ocurrido un error al realizar consulta.'
                        } 
                    }
        
        except requests.exceptions.Timeout:
            return {
                    'status': 400,
                    'data': {
                        'error': "Timeout en la solicitud",
                        'nombre': None,
                        'document': None,
                        'dv': None,
                        'sexo': None,
                        'direccion': None,
                        'ciudad/comuna': None
                    }
                    
                }
        
        