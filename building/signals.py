from django.db.models.signals import post_save
from building.models import Building, Utility, MainUtil
from apartment.models import Apartment, PowerSupply, MutualUtility


def initialize_utilities(instance):
    utils_to_create = [
        Utility(name='Cold Water', provider='City', building=instance, util_type='Individual'),
        Utility(name='Hot Water', provider='City', building=instance, util_type='Individual'),
        Utility(name='Gas Power', provider='City', building=instance, util_type='Individual'),
        Utility(name='Heating Power', provider='City', building=instance, util_type='Individual'),
    ]
    Utility.objects.bulk_create(utils_to_create)


def initialize_building(sender, instance, created, **kwargs):
    """
    Signal listens for a new building instance being created.
    When new instance was created, the signal triggers function and creates a given number of apartments
    that was set with the building instance.
    """

    if created:

        # default utils used independently by each building.
        initialize_utilities(instance)

        # apartment capacity set by the building instance when created
        apartments_to_create = instance.apartments_capacity

        # list of utility objects created above filtered by the instance of the sender(newly created object)
        utilities = Utility.objects.filter(building=instance)

        for util in utilities:
            MainUtil.objects.create(util=util)

        # create new apartment objects
        for number in range(1, apartments_to_create+1):
            Apartment.objects.create(number_id=number, building=instance)


def initialize_apartment(sender, instance, created, **kwargs):
    """
    Signal listens for a new apartment instance being created.
    When new instance was created, the signal triggers function and creates a given number power supplies.
    """
    if created:
        # default utils used independently by each apartment in the building.
        utilities = Utility.objects.filter(building=instance.building)

        # for each created apartment, add an individual utility
        for util in utilities:
            PowerSupply.objects.create(apartment=instance, utility=util)


post_save.connect(initialize_building, sender=Building)
post_save.connect(initialize_apartment, sender=Apartment)