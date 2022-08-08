from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import ModelChoiceField, TextInput

from .models import *


# class CustomerCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = 'Ex: Username'
#         self.fields['password'].help_text = 'Ex: 00000000'
#         self.fields['first_name'].help_text = 'Ex: Olha, Georgiy'
#         self.fields['last_name'].help_text = 'Ex: Petrosev'
#         self.fields['email'].help_text = 'Ex: email@email.com'
#         self.fields['phone_number'].help_text = 'Ex: 0689990723'


class CustomerCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='Username', widget=forms.TextInput)
    first_name = forms.CharField(label="Ім'я")
    last_name = forms.CharField(label='Прізвище: ')
    phone_number = forms.IntegerField(label='Номер телефону')
    email = forms.EmailField(label='Еmail', widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторити пароль', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CreateReviewForm(forms.ModelForm):
    mark = forms.CharField(label='Оцінка ')
    text = forms.Textarea()

    # def __init__(self, request, *args, **kwargs):
    #     super(CreateReviewForm, self).__init__(request, *args, **kwargs)
    #     self.fields['customer_id'].initial = request.user.id

    class Meta:
        model = Review
        # widgets = {'customer': forms.HiddenInput()}
        fields = ('mark', 'text')


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateOrderForm(forms.ModelForm):
    time_date_order = forms.DateTimeField(label='Час та дата на коли треба зробити замовлення: ', widget=DateTimeInput)
    cakes = forms.ModelMultipleChoiceField(
        queryset=Cake.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = OrderC
        fields = ('time_date_order', 'cakes')

    def save(self, commit=True):
        instance = super(CreateOrderForm, self).save(commit=True)
        instance.prise_sum = instance.cakes.aggregate(Sum('price'))['price__sum']
        instance.save()
        return instance
