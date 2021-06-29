from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Building

UserModel = get_user_model()


class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'password1', 'password2'
        )


class ResidentialRegistrationForm(ModelForm):
    class Meta:
        model = Building
        fields = (
            'street_name', 'street_number', 'city', 'county',
            'postal_code', 'apartments_capacity', 'has_elevator'
        )