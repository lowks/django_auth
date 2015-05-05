from django.test import TestCase
from model_mommy import mommy

from . import utils
from ... import models
from ...backends import KagisoBackend


class KagisoUserTest(TestCase):

    def test_user(self):
        # ----- Create user -----
        email = utils.random_email()
        profile = {
            'first_name': 'Fred',
        }
        password = 'my_password'

        user = mommy.prepare(
            models.KagisoUser,
            id=None,
            email=email,
            profile=profile,
        )
        user.set_password(password)
        user.save()

        result = models.KagisoUser.objects.get(id=user.id)

        assert result.email == email
        assert not result.confirmation_token
        assert result.profile == profile

        # ----- Confirm user -----
        assert not user.email_confirmed
        user.confirm_email(user.confirmation_token)
        assert user.email_confirmed

        # ----- Can the user sign in? -----
        auth_backend = KagisoBackend()
        signed_in_user = auth_backend.authenticate(user.email, password)
        assert signed_in_user == user

        # ----- Update user -----
        new_email = utils.random_email()
        new_profile = {
            'first_name': 'George',
        }

        user.email = new_email
        user.profile = new_profile
        user.save()

        updated_result = models.KagisoUser.objects.get(id=user.id)

        assert updated_result.email == new_email
        assert updated_result.profile == new_profile

        # ----- Sign out the user -----
        signed_out = user.record_sign_out()
        assert signed_out

        # ----- Delete user -----
        updated_result.delete()

    def test_reset_password(self):
        # ----- Reset the password -----
        email = utils.random_email()

        user = mommy.prepare(
            models.KagisoUser,
            id=None,
            email=email,
        )
        user.set_password('password')
        user.save()

        new_password = 'new_password'
        token = user.generate_reset_password_token()
        did_password_reset = user.reset_password(new_password, token)
        assert did_password_reset

        # ----- Can the user still sign in? -----
        auth_backend = KagisoBackend()
        result = auth_backend.authenticate(user.email, new_password)
        assert result == user
