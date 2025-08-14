from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Tip 


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["contenu"]


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # We can keep the fields by default (username, password 1, password 2)
        fields = UserCreationForm.Meta.fields
