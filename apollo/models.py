from django.db import models
import datetime
from django.db.models.fields import BooleanField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length = 100, primary_key = True)
    emp_name = models.CharField(max_length = 100)
    designation = models.CharField(max_length = 100)
    department = models.CharField(max_length = 100)
    password = models.CharField(max_length = 1000, default = "")
    def __str__(self):
        return self.emp_id

class Accomodation(models.Model):
    room_type = models.CharField(max_length = 100, primary_key = True)
    no_of_beds_left = models.IntegerField(default = 100)
    cost = models.IntegerField(default = 10000)
    def __str__(self):
        return self.room_type

class Patients(models.Model):
    patient_id = models.CharField(max_length = 100, primary_key = True)
    patient_name = models.CharField(max_length = 100)
    room_type = models.ForeignKey(Accomodation, on_delete = models.CASCADE)
    age = models.IntegerField(default = 0)
    phone_no = models.IntegerField(default = 9999999999)
    profession = models.CharField(max_length = 100)
    last_login = models.DateTimeField('Last Login', default = timezone.now())
    password = models.CharField(max_length = 1000, default = "")
    def __str__(self):
        return self.patient_id

class EmpFinance(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
    salary = models.IntegerField(default = 10000)
    def __str__(self):
        return str(self.emp_id)

class PatFinance(models.Model):
    patient_id = models.ForeignKey(Patients, on_delete = models.CASCADE)
    payment_method = models.CharField(max_length = 100)
    amount_paid = models.IntegerField(default = 0)
    date = models.DateField('payment_date')
    payment_id = models.CharField(max_length = 100,primary_key=True)
    is_paid = BooleanField(default=True)
    def __str__(self):
        return self.payment_id

class Vaccines(models.Model):
    vaccine_name = models.CharField(max_length = 100, primary_key = True)
    vaccine_stock = models.IntegerField(default = 100)
    vaccine_cost = models.IntegerField(default = 1000)
    def __str__(self):
        return self.vaccine_name

class CovApply(models.Model):
    patient_id = models.ForeignKey(Patients, on_delete = models.CASCADE)
    vaccine_name = models.ForeignKey(Vaccines, on_delete = models.CASCADE)
    covid_test_result = models.CharField(max_length = 10)
    def __str__(self):
        return str(self.patient_id)

class Leave(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    reason_for_leave = models.CharField(max_length = 1000)
    def __str__(self):
        return str(self.emp_id)
