import json

import requests

AUTH_HEADERS = {
    'AUTHORIZATION': 'Token: xyz',
    'SOURCE_ID': 22
}
BASE_URL = 'https://auth.kagiso.io'


def call(endpoint, method='GET', payload=None):
    fn = requests.get
    if method == 'POST':
        fn = requests.post
    elif method == 'PUT':
        fn = requests.put
    elif method == 'DELETE':
        fn = requests.delete

    url = '{base_url}/api/v1/{endpoint}/.json'.format(
        base_url=BASE_URL, endpoint=endpoint)

    request = fn(url, headers=AUTH_HEADERS, data=json.dumps(payload))

    _raise_if_4xx_or_5xx(request)

    json_data = {}
    try:
        json_data = request.json()
    except ValueError:
        # Requests chokes on empty body
        pass

    return request.status_code, json_data


def _raise_if_4xx_or_5xx(request):
    request.raise_for_status()
