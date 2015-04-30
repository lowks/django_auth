from dateutil import parser
from django.test import TestCase
from model_mommy import mommy
import responses

from . import mocks, utils
from ... import models


class KagisoUserTest(TestCase):

    @responses.activate
    def test_create(self):
        # ------------------------
        # -------Arrange----------
        # ------------------------

        email = utils.random_email()
        profile = {
            'is_superadmin': True
        }

        url, api_data = mocks.mock_out_post_users(1, email, profile)
        # ------------------------
        # -------Act--------------
        # ------------------------

        user = mommy.make(
            models.KagisoUser,
            id=None,
            email=email,
            profile=profile,
        )

        # ------------------------
        # -------Assert----------
        # ------------------------

        # Confirmation tokens are saved in memory only.
        assert user.confirmation_token == api_data['confirmation_token']

        result = models.KagisoUser.objects.get(id=user.id)

        if not responses.deactivated:
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
        mocks.mock_out_post_users(1, utils.random_email())

        user = mommy.make(models.KagisoUser, id=None)

        email = utils.random_email()
        profile = {
            'is_superadmin': True
        }

        url, api_data = mocks.mock_out_put_users(1, email, profile)

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

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert result.id == api_data['id']
        assert result.email == api_data['email']
        assert result.profile == api_data['profile']
        assert result.modified == parser.parse(api_data['modified'])

    @responses.activate
    def test_delete(self):
        mocks.mock_out_post_users(1, utils.random_email())
        user = mommy.make(models.KagisoUser, id=None)
        url = mocks.mock_out_delete_users(user.id)

        user.delete()

        user_deleted = not models.KagisoUser.objects.filter(
            id=user.id).exists()

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert user_deleted

    def test_get_full_name_returns_email(self):
        email = utils.random_email()
        user = models.KagisoUser(email=email)

        assert user.get_full_name() == email

    def test_get_short_name_returns_email(self):
        email = utils.random_email()
        user = models.KagisoUser(email=email)

        assert user.get_short_name() == email

    def test_set_password(self):
        user = models.KagisoUser()
        password = 'my_password'

        user.set_password(password)

        assert user.raw_password == password

    @responses.activate
    def test_confirm_email(self):
        _, post_data = mocks.mock_out_post_users(1, utils.random_email())
        user = mommy.make(models.KagisoUser, id=None)
        mocks.mock_out_put_users(user.id, user.email, user.profile)
        url = mocks.mock_out_post_confirm_email(user.id)

        user.confirm_email(post_data['confirmation_token'])

        if not responses.deactivated:
            assert len(responses.calls) == 3
            # Create user, confirm user, update user...
            assert responses.calls[1].request.url == url

        result = models.KagisoUser.objects.get(id=user.id)

        assert result.email_confirmed
        assert not result.confirmation_token

    @responses.activate
    def test_record_sign_out(self):
        id = 1
        _, post_data = mocks.mock_out_post_users(id, utils.random_email())
        user = mommy.make(models.KagisoUser, id=None)
        url = mocks.mock_out_delete_sessions(id)

        did_sign_out = user.record_sign_out()

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert did_sign_out

    @responses.activate
    def test_generate_reset_password_token(self):
        _, post_data = mocks.mock_out_post_users(1, utils.random_email())
        user = mommy.make(models.KagisoUser, id=None)
        url, data = mocks.mock_out_get_reset_password(user.id)

        reset_password_token = user.generate_reset_password_token()

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert reset_password_token == data['reset_password_token']  # noqa

    @responses.activate
    def test_reset_password(self):
        _, post_data = mocks.mock_out_post_users(1, utils.random_email())
        user = mommy.make(models.KagisoUser, id=None)
        url = mocks.mock_out_post_reset_password(user.id)

        did_password_reset = user.reset_password('new_password', 'test_token')

        if not responses.deactivated:
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == url

        assert did_password_reset
