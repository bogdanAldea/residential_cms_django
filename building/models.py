from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Defined custom user model
    """
    phone_number = models.CharField(max_length=10, null=True, blank=True)


class Building(models.Model):
    """
    Main app model.
    Model takes a one to one relationship with a user who has group of administrator.
    """

    admin               = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    street_name         = models.CharField(max_length=100, null=True)
    street_number       = models.PositiveIntegerField()
    city                = models.CharField(max_length=100, null=True)
    county              = models.CharField(max_length=100, null=True)
    postal_code         = models.CharField(max_length=10, null=True)
    apartments_capacity = models.PositiveIntegerField()
    has_elevator        = models.BooleanField(default=False)

    # TODO add new field for files/documents/pdfs

    def __str__(self):
        return f"<{self.street_name}, {self.street_number}>"

    def __repr__(self):
        return f"<{self.street_name}, {self.street_number}>"


class Utility(models.Model):
    """
    Defines model that describes a general utility used bu either an entire building, or individually
    by an apartment object.
    """

    PROVIDERS = (
        ('City', 'City'),
        ('Private', 'Private')
    )

    TAX_TYPE = (
        (True, 'Per Person'),
        ('False', 'Per Apartment')
    )

    UTIL_TYPE = (
        ('Mutual', 'Mutual'),
        ('Individual', 'Individual')
    )

    name            = models.CharField(max_length=30, null=True)
    util_type       = models.CharField(max_length=20, null=True, choices=UTIL_TYPE)
    provider        = models.CharField(max_length=20, null=True, choices=PROVIDERS)
    contract_starts = models.DateField(null=True, blank=True)
    contract_ends   = models.DateField(null=True, blank=True)
    tax_or_wage     = models.FloatField(default=0, null=True)
    tax_type        = models.BooleanField(null=True, choices=TAX_TYPE)
    building        = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.name}: {self.building}"


class MainUtil(models.Model):
    """
    """

    util = models.ForeignKey(Utility, on_delete=models.CASCADE)
    index_counter = models.PositiveIntegerField(default=0, null=True)