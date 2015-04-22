import json

from dateutil import parser
from django.test import TestCase
from model_mommy import mommy
import responses

from .. import models


class KagisoUserTest(TestCase):

    @responses.activate
    def test_create(self):
        # ------------------------
        # -------Arrange----------
        # ------------------------

        url = 'https://auth.kagiso.io/api/v1/users/.json'
        email = 'test@email.com'
        profile = {
            'is_superadmin': True
        }

        data = {
            'id': 49,
            'email': email,
            'confirmation_token': '49:1YkTO2:1VuxvGJre66xqQj6rkEXewmVs08',
            'email_confirmed': None,
            'profile': profile,
            'created': '2015-04-21T08:18:30.368602Z',
            'modified': '2015-04-21T08:18:30.374410Z'
        }

        responses.add(
            responses.POST,
            url,
            body=json.dumps(data),
            status=201,
        )

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
        assert user.confirmation_token == data['confirmation_token']

        result = models.KagisoUser.objects.get(id=user.id)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

        assert result.id == data['id']
        assert result.email == data['email']
        assert result.confirmation_token is None
        assert result.profile == data['profile']
        assert result.date_joined == parser.parse(data['created'])
        assert result.modified == parser.parse(data['modified'])

    @responses.activate
    def test_update(self):
        # ------------------------
        # -------Arrange----------
        # ------------------------

        url = 'https://auth.kagiso.io/api/v1/users/.json'

        data = {
            'id': 1,
            'email': 'test@email.com',
            'confirmation_token': '49:1YkTO2:1VuxvGJre66xqQj6rkEXewmVs08',
            'email_confirmed': None,
            'profile': None,
            'created': '2015-04-21T08:18:30.368602Z',
            'modified': '2015-04-21T08:18:30.374410Z'
        }

        responses.add(
            responses.POST,
            url,
            body=json.dumps(data),
            status=201,
        )
        user = mommy.make(models.KagisoUser, id=None)

        url = 'https://auth.kagiso.io/api/v1/users/1/.json'
        email = 'test@email.com'
        profile = {
            'is_superadmin': True
        }

        data = {
            'id': 1,
            'email': email,
            'profile': profile,
            'created': '2015-04-21T08:18:30.368602Z',
            'modified': '2015-04-21T08:18:30.374410Z'
        }

        responses.add(
            responses.PUT,
            url,
            body=json.dumps(data),
            status=200,
        )

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

        assert result.id == data['id']
        assert result.email == data['email']
        assert result.profile == data['profile']
        assert result.modified == parser.parse(data['modified'])

    @responses.activate
    def test_delete(self):
        email = 'test@email.com'
        # ------------------------
        # -------Arrange----------
        # ------------------------

        user = models.KagisoUser(email=email)
        url = 'https://auth.kagiso.io/api/v1/users/.json'

        data = {
            'id': 1,
            'email': 'test@email.com',
            'confirmation_token': '49:1YkTO2:1VuxvGJre66xqQj6rkEXewmVs08',
            'email_confirmed': None,
            'profile': None,
            'created': '2015-04-21T08:18:30.368602Z',
            'modified': '2015-04-21T08:18:30.374410Z'
        }

        responses.add(
            responses.POST,
            url,
            body=json.dumps(data),
            status=201,
        )
        user = mommy.make(models.KagisoUser, id=None)

        url = 'https://auth.kagiso.io/api/v1/users/1/.json'

        responses.add(
            responses.DELETE,
            url,
            body=json.dumps(data),
            status=204,
        )

        # ------------------------
        # -------Act--------------
        # ------------------------

        user.delete()

        # ------------------------
        # -------Assert----------
        # ------------------------
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
