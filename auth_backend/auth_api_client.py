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

    request = None
    request = fn(url, headers=AUTH_HEADERS, data=json.dumps(payload))

    _raise_if_4xx_or_5xx(request)

    return request.status_code, request.json()


def _raise_if_4xx_or_5xx(request):
    request.raise_for_status()
