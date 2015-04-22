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
            'demographics': None,
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

        result = mommy.make(models.KagisoUser, email=email, profile=profile)

        # ------------------------
        # -------Assert----------
        # ------------------------
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

        assert result.id == data['id']
        assert result.email == data['email']
        assert result.confirmation_token == data['confirmation_token']
        assert result.profile == data['profile']
        assert result.date_joined == parser.parse(data['created'])
