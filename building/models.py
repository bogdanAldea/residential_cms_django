from django.db import models
from django.contrib.auth.models import AbstractUser


# Define custom user model
class User(AbstractUser):
    # is_admin    = models.BooleanField(default=True)
    # is_tenant   = models.BooleanField(default=False)
    pass


# Create main parent app models
class Building(models.Model):

    admin                       = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    address                     = models.CharField(max_length=100, null=True)
    number_of_apartments        = models.IntegerField()

    def __str__(self):
        return self.address


# Defined apartment model.
class Apartment(models.Model):
    PAYMENT_STATUS = (
        (True, 'Paid'),
        (False, 'Unpaid')
    )

    building                = models.ForeignKey(Building, on_delete=models.CASCADE)
    tenant                  = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    number_of_persons       = models.IntegerField(default=0)
    payment_status          = models.BooleanField(default=True, null=True, choices=PAYMENT_STATUS)
    current_month_payment   = models.FloatField(default=0)
    debt                    = models.FloatField(default=0)

    def __str__(self):
        return f'Apartment {self.pk}'


# Defines utility model
class Utility(models.Model):

    PROVIDERS = (
        ('City', 'City'),
        ('Private', 'Private')
    )

    name = models.CharField(max_length=50, null=True)
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    contract_starts = models.DateField(null=True, blank=True)
    contract_ends = models.DateField(null=True, blank=True)
    util_tax_wage = models.FloatField(default=0, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


"""
Defines mutual utility model. Each model points to a created utility object 
with the pre defined type of 'mutual'.
"""
class MutualUtil(models.Model):

    apartment = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    common_util = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    util_type = models.CharField(default='Mutual', max_length=20)

    def __str__(self):
        return f'{self.common_util.name}: {self.apartment}'


"""
Defines individual utility model. Each model points to a created utility object 
with the pre defined type of 'individual'.
"""
class IndividualUtil(models.Model):

    STATUS = (
        (True, 'Active'),
        (False, 'Disabled')
    )

    apartment = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    individual_util = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    util_type = models.CharField(default='Individual', max_length=20)

    def __str__(self):
        return f'{self.individual_util.name}: {self.apartment}'


# Defined feature model
class Feature(models.Model):

    name = models.CharField(max_length=50, null=True)
    feature_tax = models.FloatField(default=0, null=True)
    building = models.ForeignKey(Building, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Defines feature -> apartment intermediary model. Each model points to a created feature object
class FeatureLinked(models.Model):

    apartment = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    related_feature = models.ForeignKey(Feature, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.related_feature.name}: {self.apartment}'