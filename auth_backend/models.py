from dateutil import parser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from jsonfield import JSONField

from . import auth_api_client
from .managers import AuthManager

# TODO: possible fields to add to CAS
# first_name, last_name, is_staff, is_superadmin


class KagisoUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=250, unique=True)
    profile = JSONField(null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()
    modified = models.DateTimeField()

    confirmation_token = None
    raw_password = None

    objects = AuthManager()

    @property
    def is_staff(self):
        # TODO: Implement
        return False

    @property
    def is_superadmin(self):
        # TODO: implement
        return False

    def get_full_name(self):
        return self.email

    def get_shortname(self):
        return self.email

    def set_password(self, raw_password):
        # We don't want to save passwords locally
        self.set_unusable_password()
        self.raw_password = raw_password
        # TODO: Update password on CAS?

    def save(self, *args, **kwargs):
        if not self.id:
            self._create_user_in_db_and_cas()
        else:
            self._update_user_in_cas()

        super().save()

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


@receiver(pre_delete, sender=KagisoUser)
def delete_user_from_cas(sender, instance, using, **kwargs):
    status, data = auth_api_client.call(
        'users/{id}'.format(id=instance.id), 'DELETE')
    assert status == 204
