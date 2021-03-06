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
            'age': 15,
        }
        password = 'my_password'

        user = mommy.prepare(
            models.KagisoUser,
            id=None,
            email=email,
            first_name='George',
            last_name='Smith',
            is_staff=True,
            is_superuser=True,
            profile=profile,
        )
        user.set_password(password)
        user.save()

        result = models.KagisoUser.objects.get(id=user.id)

        assert result.email == user.email
        assert result.first_name == user.first_name
        assert result.last_name == user.last_name
        assert result.is_staff
        assert result.is_superuser
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
        new_first_name = 'Fred'
        new_last_name = 'Jones'
        new_profile = {
            'age': 50,
        }

        user.email = new_email
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.is_staff = False
        user.is_superuser = False
        user.profile = new_profile
        user.save()

        updated_result = models.KagisoUser.objects.get(id=user.id)

        assert updated_result.email == new_email
        assert updated_result.first_name == new_first_name
        assert updated_result.last_name == new_last_name
        assert not updated_result.is_staff
        assert not updated_result.is_superuser
        assert updated_result.profile == new_profile

        # ----- Sign out the user -----
        signed_out = user.record_sign_out()
        assert signed_out

        # ----- Delete user -----
        updated_result.delete()

    def test_reset_password(self):
        # ----- Create the user -----
        email = utils.random_email()

        user = mommy.prepare(
            models.KagisoUser,
            id=None,
            email=email,
        )
        user.set_password('password')
        user.save()

        # ----- Reset the password -----
        new_password = 'new_password'
        token = user.generate_reset_password_token()
        did_password_reset = user.reset_password(new_password, token)
        assert did_password_reset

        # ----- Can the user still sign in? -----
        auth_backend = KagisoBackend()
        result = auth_backend.authenticate(user.email, new_password)
        assert result == user
