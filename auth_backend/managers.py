from django.contrib.auth.models import BaseUserManager

from .models import KagisoUser


class AuthManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):
        user = KagisoUser(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        return self.create_user(email, password, is_superuser=True)
