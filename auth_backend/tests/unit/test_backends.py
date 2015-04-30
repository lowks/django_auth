from django.test import TestCase
import responses

from . import mocks, utils
from ...backends import KagisoBackend
from ...models import KagisoUser


class KagisoBackendTest(TestCase):

    @responses.activate
    def test_authenticate_valid_credentials_returns_user(self):
        email = utils.random_email()
        password = 'random'
        profile = {
            'first_name': 'Fred'
        }
        url, api_data = mocks.mock_out_post_users(1, email, profile)
        user = KagisoUser.objects.create_user(
            email, password, profile=profile)
        url = mocks.mock_out_post_sessions(email, password, 200)

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert isinstance(result, KagisoUser)
        assert result.id == user.id

    @responses.activate
    def test_authenticate_user_does_not_exist_locally_returns_none(self):
        email = utils.random_email()
        password = 'random'

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        if not responses.deactivated:
            assert len(responses.calls) == 0

        assert not result

    @responses.activate
    def test_authenticate_invalid_credentials_returns_none(self):
        email = utils.random_email()
        password = 'incorrect'
        profile = {
            'first_name': 'Fred'
        }
        url, api_data = mocks.mock_out_post_users(1, email, profile)
        KagisoUser.objects.create_user(
            email, password, profile=profile)
        url = mocks.mock_out_post_sessions(email, password, 404)

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert not result
