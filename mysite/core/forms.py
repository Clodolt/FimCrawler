from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Journal


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class JournalSelectionForm(forms.ModelForm):
    not_interested = forms.ModelMultipleChoiceField(
            queryset=Journal.objects,
            widget=forms.CheckboxSelectMultiple,
            required=False,
    label = "Hier können Sie auswählen bei welchen Zeitschriften Sie nicht über Neuerscheinungen informiert werden wollen")
    class Meta:
        model = Profile
        fields = ['not_interested']
