from bs4 import BeautifulSoup


def get_fields(data):
    data = data.find_all('td')

    fields = {
        'nombre': data[0].text,
        'rut': data[1].text,
        'sexo': data[2].text,
        'direccion': data[3].text,
        'ciudad': data[4].text
    }
    print(data)
    return fields

def scrap_text_res(response):
    soup = BeautifulSoup(response, 'html.parser')
    data_table = soup.find('tbody').find_all('tr')
    return [get_fields(res) for res in data_table]

def get_results(req):
    results = scrap_text_res(req.text)
    return results

