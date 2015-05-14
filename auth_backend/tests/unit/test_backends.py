from django.test import TestCase
import responses

from . import mocks
from ...backends import KagisoBackend
from ...models import KagisoUser


class KagisoBackendTest(TestCase):

    @responses.activate
    def test_authenticate_valid_credentials_returns_user(self):
        email = 'test@email.com'
        password = 'random'
        profile = {
            'first_name': 'Fred'
        }
        url, api_data = mocks.mock_out_post_users(
            1,
            email,
            profile=profile
        )
        user = KagisoUser.objects.create_user(
            email, password, profile=profile)
        url = mocks.mock_out_post_sessions(email, password, 200)

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == url

        assert isinstance(result, KagisoUser)
        assert result.id == user.id

    @responses.activate
    def test_authenticate_user_does_not_exist_locally_returns_none(self):
        email = 'test@email.com'
        password = 'random'

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        assert len(responses.calls) == 0

        assert not result

    @responses.activate
    def test_authenticate_invalid_credentials_returns_none(self):
        email = 'test@email.com'
        password = 'incorrect'
        url, api_data = mocks.mock_out_post_users(1, email)
        KagisoUser.objects.create_user(email, password)
        url = mocks.mock_out_post_sessions(email, password, 404)

        backend = KagisoBackend()
        result = backend.authenticate(email, password)

        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == url

        assert not result
