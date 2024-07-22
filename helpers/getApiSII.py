import requests

def get_data_by_api(rut, src_path):
    try:
        full_path = f'{src_path}{rut}.json'
        headers = {"accept": "application/json"}
        response = requests.get(full_path, headers=headers)
        response_json = response.json()
        
        if response_json['status'] == 'success':
            return {
                'actividades': response_json['data']['activities']
            }
        else:
            return {}
        
    except:
        print("Ha ocurrido un error al realizar consulta a API SII.\n")
        return {}