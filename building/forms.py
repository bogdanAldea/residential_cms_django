from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'password1', 'password2'
        )