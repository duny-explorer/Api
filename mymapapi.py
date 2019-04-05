from PIL import Image
import requests
from io import BytesIO


def geocode(address):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
    
    response = requests.get(geocoder_request, params={"geocode": address, "format": "json"})

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return toponym[0]["GeoObject"] if toponym else None


def get_coord(address):
    toponym = geocode(address)
    if not toponym:
        return(None, None)

    return ",".join(toponym["Point"]["pos"].split(" "))


def get_spn(address):
    toponym = geocode(address)
    ll = get_coord(address)
    
    if not toponym or not ll:
        return(None, None)
 
    envelope = toponym["boundedBy"]["Envelope"]
    x1,y1 = envelope["lowerCorner"].split(" ")
    x2,y2 = envelope["upperCorner"].split(" ")
    spn = "{0},{1}".format(abs(float(x1) - float(x2)) / 2.0, abs(float(y1) - float(y2)) / 2.0)
    return (ll, spn)


def find_org(ll, spn, request, locale="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
    "apikey": api_key,
    "text": request,
    "lang": locale,
    "ll": ll,
    "spn:" :spn,
    "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))
    
    organization = json_response["features"][0]
    return organization


def get_file_map(params):
    map_request = "https://static-maps.yandex.ru/1.x/"
    response = requests.get(map_request, params=params)

    if not response:
        print(response.status_code, "(", response.reason, ")")
        return None

    return Image.open(BytesIO(response.content))
    
              
              
      
    
    

  










