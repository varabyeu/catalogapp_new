"""
Module imports django forms to create order form
"""

from django import forms
from django.contrib.auth.models import User

from .models import Order, UserClass


class OrderForm(forms.ModelForm):
    """Class to make order form in views (MakeOrderView)"""

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
           'user', 'order_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User with login {username} not found')
        user = User.objects.filter(username=username).first
        # if user:
        #     if not user.check_password(password):
        #         raise forms.ValidationError('Password is incorrect')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    position = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Submit password'
        self.fields['position'].label = 'Position'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        # self.fields['organization'].label = 'Organization'

    # def clean_organization(self):
    #     organization = self.cleaned_data['organization']
    #     admitted_organization = ['Stroytechengineering', 'Daterminova']
    #     if organization not in admitted_organization:
    #         raise forms.ValidationError(f'Registration with {organization} is impossible')
    #     return organization

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Name {username} is already in use')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(f'Passwords is not equal')


    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'confirm_password',
            'position',
            'first_name',
            'last_name',
            # 'organization'
        ]



