from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Defined custom user model
    """
    phone_number = models.CharField(max_length=10, null=True, blank=True)


class Building(models.Model):
    """
    Main app model.
    Model takes a one to one relationship with a user who has group of administrator.
    """

    admin               = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    street_name         = models.CharField(max_length=100, null=True)
    street_number       = models.PositiveIntegerField()
    postal_code         = models.CharField(max_length=10, null=True)
    apartments_capacity = models.PositiveIntegerField()

    def __repr__(self):
        return f"{self.street_name}, {self.street_number}"