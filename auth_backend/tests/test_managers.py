from dateutil import parser
from django.test import TestCase
import responses

from . import utils
from ..managers import AuthManager


class KagisoUserTest(TestCase):

    @responses.activate
    def test_create_user(self):
        email = 'test@email.com'
        password = 'random'
        profile = {
            'first_name': 'Fred'
        }
        url, api_data = utils.mock_out_post_users(1, email, profile)

        auth_manager = AuthManager()
        result = auth_manager.create_user(email, password, profile=profile)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

        assert result.id == api_data['id']
        assert result.email == email
        assert result.confirmation_token == api_data['confirmation_token']
        assert not result.email_confirmed
        assert result.profile == profile
        assert result.date_joined == parser.parse(api_data['created'])
        assert result.modified == parser.parse(api_data['modified'])

    @responses.activate
    def test_create_super_user(self):
        email = 'test@email.com'
        password = 'random'
        url, api_data = utils.mock_out_post_users(1, email)

        auth_manager = AuthManager()
        result = auth_manager.create_superuser(email, password)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

        assert result.email == email
        assert result.is_superuser
