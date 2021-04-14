from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import (
        Building, Utility
)

User = get_user_model()

class CreateUSerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'password1', 'password2']


class CreateTenant(CreateUSerForm):
    class Meta(CreateUSerForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']


class ResidentialForm(ModelForm):
    class Meta:
        model   = Building
        fields  = ['address', 'apartments_capacity']


class UtilityForm(ModelForm):
    class Meta:
        model = Utility
        fields = '__all__'
        exclude = ['building']


class UpdateUtilityForm(ModelForm):
    class Meta:
        model = Utility
        fields = '__all__'
        exclude = ['building', 'util_type', 'tax_type']