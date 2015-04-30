import responses

responses.activate = lambda f: f

from ..unit.test_auth_api_client import *  # noqa
from ..unit.test_backends import *  # noqa
from ..unit.test_managers import *  # noqa
from ..unit.test_models import *  # noqa
