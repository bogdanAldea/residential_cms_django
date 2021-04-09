from django.contrib import admin
from .models import *


admin.site.register(Tenant)
admin.site.register(Apartment)
admin.site.register(MutualUtil)
admin.site.register(IndividualUtil)
