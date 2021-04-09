from django.db import models
from residential.models import *


class Tenant(models.Model):
    """
    Defined tenant profile model for user with "is_tenant" role. Profile allows users to view their assigned apartment
    object and gives control over some functionalities.
    """

    tenant      = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=50, null=True)
    last_name   = models.CharField(max_length=50, null=True)
    email       = models.EmailField(null=True)
    phone       = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} Profile'


class Apartment(models.Model):
    """
    Defined model that represent an apartment. It takes a one to many relationship with
    the parent model (Building model) and a one to one relationship whit a user that hasn't
    admin privileges.
    """

    PAYMENT_STATUS = (
        (True, 'Paid'),
        (False, 'Unpaid')
    )

    building                = models.ForeignKey(Building, on_delete=models.CASCADE)
    tenant                  = models.OneToOneField(Tenant, null=True, blank=True, on_delete=models.CASCADE)
    persons                 = models.PositiveIntegerField(default=0)
    payment_status          = models.BooleanField(default=True, null=True,  choices=PAYMENT_STATUS)
    current_month_payment   = models.FloatField(default=0)
    debt                    = models.FloatField(default=0)

    def __str__(self):
        return f'Apartment {self.id}'


class MutualUtil(models.Model):
    """
    Defines mutual utility model. Each model points to a created utility object
    with the pre defined type of 'mutual'.
    """

    apartment       = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    util            = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    monthly_payment = models.FloatField(default=0, null=True)

    def __str__(self):
        return f'{self.util.name}: {self.apartment}'


class IndividualUtil(models.Model):
    """
    Defines individual utility model. Each model points to a created utility object
    with the pre defined type of 'individual'.
    """

    STATUS = (
        (True, 'Active'),
        (False, 'Disabled')
    )

    apartment           = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    util                = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    monthly_payment     = models.FloatField(default=0, null=True)
    index_counter       = models.IntegerField(default=0, null=True)
    status              = models.BooleanField(default=False, null=True, blank=True, choices=STATUS)

    def __str__(self):
        return f'{self.util.name}: {self.apartment}'