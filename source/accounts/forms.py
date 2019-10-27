from django import forms


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', required=True)
    password = forms.CharField(max_length=100, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confrim = forms.CharField(max_length=100, label='Password Comfirm', required=True,
                               widget=forms.PasswordInput)
