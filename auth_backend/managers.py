from django.contrib.auth.models import BaseUserManager


class AuthManager(BaseUserManager):

    def create_user(self, email, password=None):
        pass

    def create_superuser(self, email, password):
        pass
