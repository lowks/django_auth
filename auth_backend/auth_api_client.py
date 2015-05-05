import json
import logging

import requests

from . import settings

logger = logging.getLogger('django')

AUTH_HEADERS = {
    'AUTHORIZATION': 'Token {0}'.format(settings.CAS_TOKEN),
    'SOURCE-ID': settings.CAS_SOURCE_ID,
}
BASE_URL = settings.CAS_BASE_URL


def call(endpoint, method='GET', payload=None):
    fn = requests.get
    if method == 'POST':
        fn = requests.post
    elif method == 'PUT':
        fn = requests.put
    elif method == 'DELETE':
        fn = requests.delete

    url = '{base_url}/{endpoint}/.json'.format(
        base_url=BASE_URL, endpoint=endpoint)

    request = fn(url, headers=AUTH_HEADERS, json=payload)

    logger.debug('method={0}'.format(method))
    logger.debug('url={0}'.format(url))
    logger.debug('headers={0}'.format(AUTH_HEADERS))
    logger.debug('payload={0}'.format(payload))
    logger.debug('json={0}'.format(json.dumps(payload)))

    _raise_if_4xx_or_5xx_but_not_404(request)

    json_data = {}
    try:
        json_data = request.json()
    except ValueError:
        # Requests chokes on empty body
        pass

    return request.status_code, json_data


def _raise_if_4xx_or_5xx_but_not_404(request):
    try:
        logger.debug('response={0}'.format(request.json()))
    except ValueError:
        # requests chokes on empty json body
        pass
    if not request.status_code == 404:
        request.raise_for_status()
