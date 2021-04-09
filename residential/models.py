from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Defined custom user models with distinct roles
    """
    pass


class Building(models.Model):
    """
    Defined main model that encapsulates the whole app.
    Model takes a one to one relationship with a user that has admin privileges.
    """

    admin                   = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    address                 = models.CharField(max_length=100, null=True)
    apartments_capacity     = models.PositiveIntegerField()

    # cold water main index
    cold_water_main_index       = models.IntegerField(default=0, null=True)
    # hot water main index
    hot_water_main_index        = models.IntegerField(default=0, null=True)
    # gas power main index
    gas_power_main_index        = models.IntegerField(default=0, null=True)
    # heating power main index
    heating_power_main_index    = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.address


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
        (False, 'Per Apartment')
    )

    UTIL_TYPE = (
        ('Mutual', 'Mutual'),
        ('Individual', 'Individual')
    )

    name                = models.CharField(max_length=30, null=True)
    util_type           = models.CharField(max_length=20, null=True, choices=UTIL_TYPE)
    provider            = models.CharField(max_length=20, null=True, choices=PROVIDERS)
    contract_starts     = models.DateField(null=True, blank=True)
    contract_ends       = models.DateField(null=True, blank=True)
    tax_or_wage         = models.FloatField(default=0, null=True)
    tax_type            = models.BooleanField(null=True, choices=TAX_TYPE)
    building            = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}: {self.building}'


class Feature(models.Model):
    """
    Defines model that describes a general feature.
    It takes a one to many relationship with the building it's assigned to.
    """
    name        = models.CharField(max_length=30, null=True)
    tax         = models.FloatField(default=0, null=True)
    building    = models.ForeignKey(Building, null=True, on_delete=models.CASCADE)