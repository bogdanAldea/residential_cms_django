from django.db import models


class UtilType(models.TextChoices):
    mutual     = 'Mutual'
    individual = 'individual'