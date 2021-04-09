from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CreateUSerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateResidentialForm(ModelForm):
    class Meta:
        model   = Building
        fields  = ['address', 'apartments_capacity']


class CreateUtilityForm(ModelForm):
    class Meta:
        model = Utility
        fields = '__all__'
        exclude = ['building']