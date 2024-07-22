import requests
import json  
import base64
from bs4 import BeautifulSoup
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def getCaptchaSII():
    try: 
        resp = requests.get("https://zeus.sii.cl/cvc_cgi/stc/CViewCaptcha.cgi?oper=0")
        resp.raise_for_status()
    
    except requests.RequestException as e: 
        return None, None, f"Error al consultar solicitud http: {str(e)}"
    
    try: 
        body = resp.content
        print(body)   
    except Exception as e:
        return None, None, f"Error al obtener cuerpo de la respuesta: {str(e)}"
    
    try:
        data = json.loads(body)
        code = data.get('txtCaptcha', '')
    except (json.JSONDecodeError, KeyError) as e:
        return None, None, f"Error al deserializar información de respuesta HTTP: {str(e)}"
    
    try:
        code_decoded = base64.b64decode(code)
    except base64.binascii.Error as e:
        return None, None, f"Error al decodificar en base64 código de Captcha: {str(e)}"
    
    if len(code_decoded) < 40:
        return None, None, "Código del captcha es muy pequeño"
    
    return code, code_decoded[36:40].decode('utf-8'), None



def getProfileSII(rut, path, headers):
    source_path = path
    code, captcha, error = getCaptchaSII()    
    if error:
        return f"Error: {error}"

    rut_digits, dv = rut.split('-')
    
    form_data = {
        'RUT': rut_digits,
        'DV': dv,
        'txt_captcha': code,
        'txt_code': captcha,
        'PRG': 'STC',
        'OPC': 'NOR'
    }
    
    try:
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.post(
            source_path,
            headers=headers,
            data=form_data
        )
        response.raise_for_status()
        
    except requests.RequestException as e: 
        return f"Error al consultar solicitud http: {str(e)}"
    
    try: 
        body = response.content
        #print(body)   
    except Exception as e:
        return f"Error al obtener cuerpo de la respuesta: {str(e)}"
    
    if response.status_code != 200: 
        return f"Estado de la respuesta no favorable: {response.status_code}"
    
    return scrapSIIProfile(body)
        
def clean(element):
    return element.get_text(strip=True) if element else ""

def scrapSIIProfile(req):
    layout = "%d-%m-%Y"
    
    try:
        soup = BeautifulSoup(req, "html.parser")
    except Exception as e:
        raise Exception("No se ha podido parsear perfil de SII") from e 
    
    name = clean(soup.select_one("#contenedor > div:nth-child(4)"))
    if name == "**":
        # No record found
        return {"name": "", "activities": []}
    
    activities = []
    tables = soup.find_all('table', {'class': 'tabla'})
    if not(len(tables)): 
        return {"nombre": name, "actividades": activities}
    
    rows = tables[0].find_all('tr')

    
    #rows = soup.select("#contenedor > table.tabla:nth-child(27) > tbody:nth-child(1) > tr")
    #print(f"rows: {rows}")
    for i, row in enumerate(rows):
        if i == 0:
            # Skip header
            continue
        try:
            code = int(clean(row.select_one("td:nth-child(2)")))
            date = clean(row.select_one("td:nth-child(5)"))
        except ValueError:
            return None

        activity = {
            "nombre": clean(row.select_one("td:nth-child(1)")),
            "codigo": code,
            "categoria": clean(row.select_one("td:nth-child(3)")),
            "afecta IVA": clean(row.select_one("td:nth-child(4)")) == "Si",
            "fecha": date,
        }
        activities.append(activity)

    return {"nombre": name, "actividades": activities}

    

    
         
    