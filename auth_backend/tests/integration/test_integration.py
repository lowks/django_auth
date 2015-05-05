from django.test import TestCase
from model_mommy import mommy

from . import utils
from ... import models


class KagisoUserTest(TestCase):

    def test_user(self):
        # ----- Create user -----
        email = utils.random_email()
        profile = {
            'first_name': 'Fred',
        }

        user = mommy.make(
            models.KagisoUser,
            id=None,
            email=email,
            profile=profile,
        )

        result = models.KagisoUser.objects.get(id=user.id)

        assert result.email == email
        assert not result.confirmation_token
        assert result.profile == profile

        # ----- Confirm user -----
        assert not user.email_confirmed
        user.confirm_email(user.confirmation_token)
        assert user.email_confirmed

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

        # ----- Delete user -----
        updated_result.delete()
