from django.db.models.signals import post_save
from residential.models import Building, Utility, MainUtil
from apartment.models import Apartment, IndividualUtil, MutualUtil


def init_building(sender, instance, created, **kwargs):
    """
    Signal listens for a new building instance being created.
    When new instance was created, the signal triggers function and creates a given number of apartments
    that was set with the building instance.
    """

    if created:
        # default utils used independently by each apartment in the building.
        utils_to_create = [
            Utility(name='Cold Water', provider='City', building=instance, util_type='Individual'),
            Utility(name='Hot Water', provider='City', building=instance, util_type='Individual'),
            Utility(name='Gas power', provider='City', building=instance, util_type='Individual'),
            Utility(name='Heating power', provider='City', building=instance, util_type='Individual')
        ]

        Utility.objects.bulk_create(utils_to_create)

        # apartment capacity set by the building instance when created
        apartments_to_create = instance.apartments_capacity

        # list of utility objects created above filtered by the instance of the sender(newly created object)
        utilities = Utility.objects.filter(building=instance)

        for util in utilities:
            MainUtil.objects.create(util=util)

        # create new apartment objects
        for number in range(1, apartments_to_create+1):
            apartment = Apartment.objects.create(id=number, building=instance)

            # for each created apartment, add an individual utility
            for util in utilities:
                IndividualUtil.objects.create(apartment=apartment, util=util)


# trigger function at the post save action, when a new building objects is created
post_save.connect(init_building, sender=Building)


def generate_utils(sender, instance, created, **kwargs):
    """
    Signal listens for a new Utility instance being created
    and triggers creation of a new utility for each apartment.
    """

    if created:
        building = instance.building
        apartments = Apartment.objects.filter(building=building)

        for apartment in apartments:
            MutualUtil.objects.create(apartment=apartment, util=instance)


# trigger function at the post save action, when a new utility objects is created
post_save.connect(generate_utils, sender=Utility)
