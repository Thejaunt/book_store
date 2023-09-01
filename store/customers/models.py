from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    REQUIRED_FIELDS = ["email"]
