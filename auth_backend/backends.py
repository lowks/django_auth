from django.contrib.auth.backends import ModelBackend

from . import auth_api_client
from .models import KagisoUser


class KagisoBackend(ModelBackend):

    def authenticate(self, email, password, username=None, **kwargs):
        # Django calls our backend with username='xyz', password='abc'
        # e.g. credentials = {'username': 'Fred', 'password': 'open'}
        # authenticate(**credentials), even though we set USERNAME_FIELD to
        # 'email' in models.py.
        # So we have to hack around it:
        # https://github.com/django/django/blob/master/django/contrib/auth/__init__.py#L74

        if username:
            email = username

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
