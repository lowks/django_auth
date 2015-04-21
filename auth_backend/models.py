from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
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
    date_joined = models.DateTimeField(auto_now_add=True)

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
        if self.id:
            self._create_for_db_and_cas()
        else:
            self.update_cas_user()

        super().save()

    def _create_for_db_and_cas(self):
        payload = {
            'email': self.email,
            'password': self.raw_password,
            'profile': self.profile,
        }

        status, data = auth_api_client.call('users', 'POST', payload)

        if status == 409:
            pass
            # TODO: throw conflict error

        if status != 201:
            pass
            # TODO: throw error

        self.id = data['id']
        self.confirmation_token = data['confirmation_token']
        self.date_joined = data['date_joined']

    def _update_cas_user(self):
        pass
