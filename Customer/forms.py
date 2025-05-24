# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile, StaffProfile, CustomUser



class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Add form-control class and placeholders for password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

        


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


