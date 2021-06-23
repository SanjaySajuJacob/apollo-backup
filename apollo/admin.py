from django.contrib import admin
from django.db import models
from .models import *
# Register your models here.
class AccomodationAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['room_type', 'no_of_beds_left', 'cost']})]

class CovApplyAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['patient_id', 'vaccine_name', 'covid_test_result']})]

class EmpFinanceAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['emp_id', 'salary']})]

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['emp_id', 'emp_name', 'designation', 'department', 'password']})]

class PatFinanceAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['patient_id', 'payment_method', 'amount_paid', 'date', 'payment_id','is_paid']})]

class PatientsAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['patient_id', 'patient_name', 'room_type', 'age', 'phone_no', 'profession', 'password']})]

class VaccinesAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['vaccine_name', 'vaccine_stock', 'vaccine_cost']})]

class LeaveAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['emp_id', 'start_date', 'end_date', 'reason_for_leave']})]

admin.site.register(Accomodation, AccomodationAdmin)
admin.site.register(CovApply, CovApplyAdmin)
admin.site.register(EmpFinance, EmpFinanceAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PatFinance, PatFinanceAdmin)
admin.site.register(Patients, PatientsAdmin)
admin.site.register(Vaccines, VaccinesAdmin)
admin.site.register(Leave, LeaveAdmin)
