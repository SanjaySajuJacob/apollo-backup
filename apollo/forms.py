from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Patients, Accomodation, PatFinance, CovApply, Leave, Vaccines
from django.core.exceptions import ValidationError
from django.utils import timezone
import random, datetime


room_types = Accomodation.objects.filter(no_of_beds_left__gt = 0)
payment_methods = (('None', 'Please select an option'),('Net Banking', 'Net Banking'), ('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'))
results = (('None','-------'),('Positive','Positive'),('Negative','Negative'))
vaccine_name = Vaccines.objects.filter(vaccine_stock__gt = 0)


class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    def mobno(no):
        if len(no) != 10:
            raise ValidationError("Please enter a valid mobile number.")

    patient_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Patient ID', 'value': random.randint(10000, 99999), 'disabled':True}))
    patient_name =  forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Patient Name'}))
    age = forms.IntegerField(widget = forms.NumberInput(attrs = {'placeholder':'Age'}))
    phone_no = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Phone Number'}), validators = [mobno])
    profession = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Profession'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder':'Password'}))
    confirm_Password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder':'Confirm Password'}))
    room_type = forms.ModelChoiceField(queryset = room_types)

    class Meta:
        model = User
        fields = ("patient_id", "patient_name", "age", "phone_no", "profession", "password", "room_type", "confirm_Password")

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        user.patient_id = self.cleaned_data['patient_id']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password')
        pw2 = cleaned_data.get('confirm_Password')
        if pw1 and pw2 and pw1!=pw2:
            raise forms.ValidationError('Passwords don\'t match')


class EmpLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    employee_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Employee ID'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ("emp_id", "password")

    def save(self, commit = True):
        user = super(EmpLoginForm, self).save(commit = False)
        user.emp_id = self.cleaned_data['emp_id']
        if commit:
            user.save()
        return user

class PatLoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    patient_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Patient ID'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ("patient_id", "password")

    def save(self, commit = True):
        user = super(PatLoginForm, self).save(commit = False)
        user.patient_id = self.cleaned_data['patient_id']
        if commit:
            user.save()
        return user

class PaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    patient_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Patient ID'}))
    no_of_days = forms.IntegerField(widget = forms.NumberInput(attrs = {'placeholder':'No. of days stayed'}))
    payment_method = forms.ChoiceField(choices = payment_methods)

    class Meta:
        model = User
        fields = ("patient_id", "no_of_days", "payment_method")

    def save(self, commit = True):
        user = super(PaymentForm, self).save(commit = False)
        user.patient_id = self.cleaned_data['patient_id']
        if commit:
            user.save()
        return user

    def checkdays(self):
        days = self.cleaned_data.get('no_of_days')
        if (days <= 0):
            raise forms.ValidationError("No. of days is either negative or 0")
        return days

class CovidCare(ModelForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()

    def check(covid_test_result):
        if covid_test_result == "Positive":
            raise forms.ValidationError('Not elligible for vaccination')


    patient_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Patient ID'}))
    covid_test_result = forms.ChoiceField(choices=results,validators =[check])
    vaccine_name = forms.ModelChoiceField(queryset = vaccine_name)

    class Meta:
        model = User
        fields = ("patient_id", "covid_test_result","vaccine_name")

    def save(self, commit = True):
        user = super(CovidCare, self).save(commit = False)
        user.patient_id = self.cleaned_data['patient_id']
        if commit:
            user.save()
        return user

class LeaveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


    emp_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Employee ID'}))
    start_date = forms.DateField(widget = forms.TextInput(attrs = {'type': 'date'}))
    end_date = forms.DateField(widget = forms.TextInput(attrs = {'type': 'date'}))
    reason_for_leave = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Reason For Leave'}))

    class Meta:
        model = User
        fields = ("emp_id", "start_date", "end_date", "reason_for_leave")

    def save(self, commit = True):
        user = super(LeaveForm, self).save(commit = False)
        user.emp_id = self.cleaned_data['emp_id']
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        date1 = cleaned_data.get('start_date')
        date2 = cleaned_data.get('end_date')
        if date1 and date2 and (date1 > date2):
            raise ValidationError('Enter valid dates')

class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    email_id = forms.EmailField(widget = forms.EmailInput(attrs = {'placeholder':'Email ID'}))
    content = forms.CharField(widget = forms.Textarea({'placeholder':'Query', "id": "enhanced_textarea", 'toolbar':'Basic', 'height': 70, 'width': 430}))

    class Meta:
        model = User
        fields = ("email_id", "content")

class Empfinform(ModelForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()

    payment_id = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Payment ID'}))

    class Meta:
        model = User
        fields = ("payment_id",)

    def save(self, commit = True):
        user = super(Empfinform, self).save(commit = False)
        user.patient_id = self.cleaned_data['payment_id']
        if commit:
            user.save()
        return user
