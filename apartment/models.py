from django.db import models
from residential.models import *


class Tenant(models.Model):
    """
    Defined tenant profile model for user. Profile allows users to view their assigned apartment
    object and gives control over some functionalities.
    """

    tenant      = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=50, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    email       = models.EmailField(null=True, blank=True)
    phone       = models.CharField(max_length=10, null=True, blank=True)

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
    tenant                  = models.OneToOneField(Tenant, null=True, blank=True, on_delete=models.SET_NULL)
    persons                 = models.PositiveIntegerField(default=0)
    payment_status          = models.BooleanField(default=True, null=True,  choices=PAYMENT_STATUS)
    debt                    = models.FloatField(default=0)

    def __str__(self):
        return f'Apartment {self.id}'

    @property
    def get_persons(self):
        return self.persons

    def get_total_individual_utils(self):
        total = 0
        for util in self.individualutil_set.all():
            total += util.get_monthly_payment()
        return total

    def get_total_mutual_utils(self):
        total = 0
        for util in self.mutualutil_set.all():
            total += util.get_monthly_payment()
        return total

    def current_month_payment(self):
        mutual      = self.get_total_mutual_utils()
        individual  = self.get_total_individual_utils()
        return mutual + individual


class MutualUtil(models.Model):
    """
    Defines mutual utility model. Each model points to a created utility object
    with the pre defined type of 'mutual'.
    """
    ...

    apartment       = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    util            = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.util.name}: {self.apartment}'

    def get_monthly_payment(self):
        util_type   = self.util.get_util_type
        tax_wage    = self.util.get_tax_wage
        persons     = self.apartment.get_persons
        capacity    = self.apartment.building.get_capacity

        payment = float()
        if util_type    == 'Per Person':
            payment = persons * tax_wage

        elif util_type  == 'Per Apartment':
            try:
                payment = tax_wage / capacity
            except ZeroDivisionError:
                payment = float(0)

        return payment


class IndividualUtil(models.Model):
    """
    Defines individual utility model. Each model points to a created utility object
    with the pre defined type of 'individual'.
    """
    ...

    STATUS = (
        (True, 'Active'),
        (False, 'Disabled')
    )

    apartment           = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    util                = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    index_counter       = models.IntegerField(default=0, null=True)
    status              = models.BooleanField(default=False, null=True, blank=True, choices=STATUS)

    def __str__(self):
        return f'{self.util.name}: {self.apartment}'

    def get_monthly_payment(self):
        return self.index_counter * self.util.get_tax_wage