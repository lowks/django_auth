from django.conf import settings

CAS_TOKEN = getattr(settings, 'CAS_TOKEN', 'CHANGEME')
CAS_SOURCE_ID = getattr(settings, 'CAS_SOURCE_ID', 'CHANGEME')
CAS_BASE_URL = getattr(settings, 'CAS_BASE_URL', 'https://auth.kagiso.io/api/v1')  # noqa
