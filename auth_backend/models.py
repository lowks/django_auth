from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

# TODO: possible fields to add to CAS
# first_name, last_name, is_staff, is_superadmin


class KagisoUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

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
        # TODO: Update password on CAS?
