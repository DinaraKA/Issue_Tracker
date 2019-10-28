from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First name', required=False)
    last_name = forms.CharField(max_length=100, label='Last name', required=False)
    username = forms.CharField(max_length=100, label='Username', required=True)
    password = forms.CharField(max_length=20, min_length=8, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=20, min_length=8, label='Password Comfirm', required=True,
                               widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('User with this email already exists',
                                  code='user_email_exists')
        except User.DoesNotExist:
            return email


    def clean_username(self):
        username=self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('User with this username already exists',
                              code='user_username_exists')
        except User.DoesNotExist:
            return username


    def clean(self):
        super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']

        if not first_name and not last_name:
            raise ValidationError('First name or last name should be filled',
                                  code='no_first_and_last_name')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match',
                                  code='passwords_do_not_match')

        return self.cleaned_data

