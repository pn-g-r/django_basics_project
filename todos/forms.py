from django import forms
from .models import Todo, Profile


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
