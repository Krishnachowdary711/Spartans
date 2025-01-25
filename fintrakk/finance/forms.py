from django import forms
from .models import Transaction, Account, Category
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'type', 'amount', 'description', 'date']  # Include the date field
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']