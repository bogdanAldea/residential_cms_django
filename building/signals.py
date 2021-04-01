from django.db.models.signals import post_save
from .models import Building, Apartment, Utility, IndividualUtil
from .config import UtilType


def generate_apartments(sender, instance, created, **kwargs):
    if created:
        utils_to_create = [
            Utility(name='Cold water', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Hot water', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Gas power', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Heating power', provider='City', building=instance, util_type=UtilType.individual)
        ]
        Utility.objects.bulk_create(utils_to_create)

        apartment_to_create = instance.number_of_apartments
        utilities = Utility.objects.filter(building=instance)
        for number in range(1, apartment_to_create+1):
            apartment = Apartment.objects.create(
                id=number,
                building=instance
            )
            for util in utilities:
                IndividualUtil.objects.create(
                    apartment=apartment,
                    individual_util=util
                )


post_save.connect(generate_apartments, sender=Building)

