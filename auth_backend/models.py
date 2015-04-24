from dateutil import parser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from jsonfield import JSONField

from . import auth_api_client
from .managers import AuthManager

# TODO: possible fields to add to CAS:
# first_name, last_name, is_staff, is_superuser


class KagisoUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=250, unique=True)
    email_confirmed = models.DateTimeField(null=True)
    profile = JSONField(null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()
    modified = models.DateTimeField()

    confirmation_token = None
    raw_password = None

    objects = AuthManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def set_password(self, raw_password):
        # We don't want to save passwords locally
        self.set_unusable_password()
        # Save them in memory only
        self.raw_password = raw_password

    def confirm_email(self, confirmation_token):
        payload = {'confirmation_token': confirmation_token}
        endpoint = 'users/{id}/confirm_email'.format(id=self.id)
        status, data = auth_api_client.call(endpoint, 'POST', payload)

        assert status == 204

        self.confirmation_token = None
        self.email_confirmed = timezone.now()
        self.save()

    def generate_reset_password_token(self):
        endpoint = 'users/{id}/reset_password'.format(id=self.id)
        status, data = auth_api_client.call(endpoint, 'GET')

        assert status == 200

        return data['reset_password_token']

    def reset_password(self, password, reset_password_token):
        payload = {
            'reset_password_token': reset_password_token,
            'password': password,
        }
        endpoint = 'users/{id}/reset_password'.format(id=self.id)
        status, _ = auth_api_client.call(endpoint, 'POST', payload)

        return status == 200

    def _create_user_in_db_and_cas(self):
        payload = {
            'email': self.email,
            'password': self.raw_password,
            'profile': self.profile,
        }

        status, data = auth_api_client.call('users', 'POST', payload)

        assert status == 201

        self.id = data['id']
        self.email = data['email']
        self.profile = data['profile']
        self.confirmation_token = data['confirmation_token']
        self.date_joined = parser.parse(data['created'])
        self.modified = parser.parse(data['modified'])

    def _update_user_in_cas(self):
        payload = {
            'email': self.email,
            'profile': self.profile,
        }

        status, data = auth_api_client.call(
            'users/{id}'.format(id=self.id), 'PUT', payload)

        assert status == 200

        self.email = data['email']
        self.profile = data['profile']
        self.modified = parser.parse(data['modified'])

    def __str__(self):
        return self.email  # pragma: no cover


@receiver(pre_delete, sender=KagisoUser)
def delete_user_from_cas(sender, instance, *args, **kwargs):
    status, data = auth_api_client.call(
        'users/{id}'.format(id=instance.id), 'DELETE')
    assert status == 204


@receiver(pre_save, sender=KagisoUser)
def save_user_to_cas(sender, instance, *args, **kwargs):
    if not instance.id:
        instance._create_user_in_db_and_cas()
    else:
        instance._update_user_in_cas()
