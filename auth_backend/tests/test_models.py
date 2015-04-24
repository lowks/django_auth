from dateutil import parser
from django.test import TestCase
from model_mommy import mommy
import responses

from . import utils
from .. import models


class KagisoUserTest(TestCase):

    @responses.activate
    def test_create(self):
        # ------------------------
        # -------Arrange----------
        # ------------------------

        email = 'test@email.com'
        profile = {
            'is_superadmin': True
        }

        url, api_data = utils.mock_out_post_users(1, email, profile)
        # ------------------------
        # -------Act--------------
        # ------------------------

        user = mommy.make(
            models.KagisoUser,
            id=None,
            email=email,
            profile=profile
        )

        # ------------------------
        # -------Assert----------
        # ------------------------

        # Confirmation tokens are saved in memory only.
        assert user.confirmation_token == api_data['confirmation_token']

        result = models.KagisoUser.objects.get(id=user.id)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

        assert result.id == api_data['id']
        assert result.email == api_data['email']
        assert not result.email_confirmed
        assert result.confirmation_token is None
        assert result.profile == api_data['profile']
        assert result.date_joined == parser.parse(api_data['created'])
        assert result.modified == parser.parse(api_data['modified'])

    @responses.activate
    def test_update(self):
        # ------------------------
        # -------Arrange----------
        # ------------------------
        utils.mock_out_post_users(1, 'test@email.com')

        user = mommy.make(models.KagisoUser, id=None)

        email = 'test@email.com'
        profile = {
            'is_superadmin': True
        }

        url, api_data = utils.mock_out_put_users(1, email, profile)

        # ------------------------
        # -------Act--------------
        # ------------------------

        user.email = email
        user.profile = profile
        user.save()

        # ------------------------
        # -------Assert----------
        # ------------------------
        result = models.KagisoUser.objects.get(id=user.id)

        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == url

        assert result.id == api_data['id']
        assert result.email == api_data['email']
        assert result.profile == api_data['profile']
        assert result.modified == parser.parse(api_data['modified'])

    @responses.activate
    def test_delete(self):
        utils.mock_out_post_users(1, 'test@email.com')
        user = mommy.make(models.KagisoUser, id=None)
        url = utils.mock_out_delete_users(user.id)

        user.delete()

        user_deleted = not models.KagisoUser.objects.filter(
            id=user.id).exists()

        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == url

        assert user_deleted

    def test_get_full_name_returns_email(self):
        email = 'test@email.com'
        user = models.KagisoUser(email=email)

        assert user.get_full_name() == email

    def test_get_short_name_returns_email(self):
        email = 'test@email.com'
        user = models.KagisoUser(email=email)

        assert user.get_short_name() == email

    @responses.activate
    def test_confirm_email(self):
        _, post_data = utils.mock_out_post_users(1, 'test@email.com')
        user = mommy.make(models.KagisoUser, id=None)
        utils.mock_out_put_users(user.id, user.email, user.profile)
        url = utils.mock_out_post_confirm_email(user.id)

        user.confirm_email(post_data['confirmation_token'])

        assert len(responses.calls) == 3
        # Create user, confirm user, update user...
        assert responses.calls[1].request.url == url

        result = models.KagisoUser.objects.get(id=user.id)

        assert result.email_confirmed
        assert not result.confirmation_token
