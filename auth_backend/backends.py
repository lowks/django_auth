from django.contrib.auth.backends import ModelBackend

from . import auth_api_client
from .models import KagisoUser


class KagisoBackend(ModelBackend):

    def authenticate(self, email, password, **kwargs):
        user = KagisoUser.objects.filter(email=email).first()

        if not user:
            return

        payload = {
            'email': email,
            'password': password,
        }

        status, data = auth_api_client.call('sessions', 'POST', payload)

        if status == 200:
            return user
