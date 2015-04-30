from dateutil import parser
from django.test import TestCase
import responses

from . import mocks, utils
from ...models import KagisoUser


class KagisoUserTest(TestCase):

    @responses.activate
    def test_create_user(self):
        email = utils.random_email()
        password = 'random'
        profile = {
            'first_name': 'Fred'
        }
        url, api_data = mocks.mock_out_post_users(1, email, profile)

        result = KagisoUser.objects.create_user(
            email, password, profile=profile)

        if not responses.deactivated:
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
        email = utils.random_email()
        password = 'random'
        url, api_data = mocks.mock_out_post_users(1, email)

        result = KagisoUser.objects.create_superuser(email, password)

        if not responses.deactivated:
            assert len(responses.calls) == 1
            assert responses.calls[0].request.url == url

        assert result.email == email
        assert result.is_superuser
