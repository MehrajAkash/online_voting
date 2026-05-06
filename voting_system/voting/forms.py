from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vote


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None
    )

    def __init__(self, election, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['candidate'].queryset = election.candidates.all()