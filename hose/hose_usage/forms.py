from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import HoseUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = HoseUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = HoseUser
        fields = ('username', 'email')
