from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Defined custom user models with distinct roles
    """
    phone = models.CharField(max_length=10, null=True, blank=True)


class Building(models.Model):
    """
    Defined main model that encapsulates the whole app.
    Model takes a one to one relationship with a user that has admin privileges.
    """

    admin                   = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    address                 = models.CharField(max_length=100, null=True)
    apartments_capacity     = models.PositiveIntegerField()

    def __str__(self):
        return self.address

    @property
    def get_capacity(self):
        return self.apartments_capacity

    def total_expenses(self):
        total_expenses = 0
        for apartment in self.apartment_set.all():
            total_expenses += apartment.current_month_payment()
        return total_expenses


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

    @property
    def get_util_type(self):
        return self.util_type

    @property
    def get_tax_wage(self):
        return self.tax_or_wage


class MainUtil(models.Model):
    util = models.ForeignKey(Utility, on_delete=models.CASCADE)
    index_counter = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.util.name} counter'


class Feature(models.Model):
    """
    Defines model that describes a general feature.
    It takes a one to many relationship with the building it's assigned to.
    """
    name        = models.CharField(max_length=30, null=True)
    tax         = models.FloatField(default=0, null=True)
    building    = models.ForeignKey(Building, null=True, on_delete=models.CASCADE)