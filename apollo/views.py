from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth import login
from django import forms
from django.utils import timezone
from django.core.mail import send_mail
import random
# Create your views here.

def homepage(request):
    return render(request, 'apollo/welcome.html')

def emploginpage(request):
    if request.method == "POST":
        form = EmpLoginForm(request.POST)
        if form.is_valid():
            emp_id = request.POST.get('employee_id')
            pw = request.POST.get('password')
            if Employee.objects.filter(emp_id=emp_id, password=pw).count() == 1:
                messages.success(request, "Logged in successfully")
                return redirect("apollo:emphomepage")
        else:
            messages.error(request, "Invalid Login Credentials. Please try again.")
    else:
        form = EmpLoginForm
    return render(request=request, template_name="apollo/emplogin.html", context = {'form':form})


def patregisterpage(request):
    if request.method == "POST":
        input_data = request.POST.dict()
        input_data.pop("csrfmiddlewaretoken", None)
        input_data.pop("confirm_Password", None)
        input_data["room_type"] = Accomodation.objects.get(room_type=input_data["room_type"])
        pat = Patients(**input_data)
        form = NewUserForm(request.POST, instance = pat)
        if form.is_valid():
            user = form.save()
            user.save()
            room = Accomodation.objects.get(room_type=input_data["room_type"])
            room.no_of_beds_left = room.no_of_beds_left - 1
            room.save()
            messages.success(request, "Registration successful!!")
            return redirect("apollo:pathomepage")
        else:
            formnotvalid = True
            message = "Registration unsuccessful. Please make sure you enter valid details, and try again"
            messages.error(request, "Registration unsuccessful. Please make sure you enter valid details, and try again")
            return render(request, "apollo/patregister.html", context = {'form':form, 'check':formnotvalid, 'message':message})
    else:
        form = NewUserForm
    return render(request, 'apollo/patregister.html', context = {"form":form})

def patloginpage(request):
    if request.method == "POST":
        form = PatLoginForm(request.POST)
        if form.is_valid():
            patient_id = request.POST.get('patient_id')
            pw = request.POST.get('password')
            if Patients.objects.filter(patient_id=patient_id, password=pw).count() == 1:
                messages.success(request, "Logged in successfully")
                return redirect("apollo:pathomepage")
        else:
            messages.error(request, "Invalid Login Credentials. Please try again.")
    else:
        form = PatLoginForm
    return render(request=request, template_name="apollo/patlogin.html", context = {'form':form})

def paymentpage(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid() and Patients.objects.filter(patient_id = request.POST.get('patient_id')).exists():
            paid = True
            patient_id = Patients.objects.get(patient_id=request.POST.get('patient_id'))
            room = Patients.objects.values('room_type').filter(patient_id=patient_id)
            days = request.POST.get('no_of_days')
            accomodate = Accomodation.objects.get(room_type = room[0]["room_type"])
            patfin = PatFinance()
            patfin.amount_paid = int(days)*int((accomodate.cost))
            patfin.patient_id = patient_id
            patfin.payment_method = request.POST.get('payment_method')
            patfin.date = timezone.now()
            patfin.payment_id = random.randint(1000, 9999)
            patfin.save()
            message = "The total cost and your Payment ID are as shown. Kindly go to the payment counter to make your payment. Thank you."
            return render(request, 'apollo/payment.html', context = {'paid':paid, 'message':message, 'cost':patfin.amount_paid, 'payment_id':patfin.payment_id, 'form':form})
        else:
            message = "Invalid details entered. Please try again."
            notpaid = True
            return render(request, 'apollo/payment.html', context = {'message':message, 'notpaid':notpaid})
    else:
        form = PaymentForm
        return render(request, 'apollo/payment.html', context = {'form':form})

def covidcare(request):
    if request.method == "POST":
        form = CovidCare(request.POST)
        if form.is_valid() and Patients.objects.filter(patient_id=request.POST.get('patient_id')).exists():
            cov = CovApply()
            covid_test_result = request.POST.get('covid_test_result')
            vaccine_name = request.POST.get('vaccine_name')
            vacc = Vaccines.objects.get(vaccine_name=request.POST.get("vaccine_name"))
            vacc.vaccine_stock = vacc.vaccine_stock -1
            vacc.save()
            if CovApply.objects.filter(patient_id=request.POST.get('patient_id')).count() == 0:
                patient_id=Patients.objects.get(patient_id=request.POST.get('patient_id'))
                cov.patient_id = patient_id
                cov.vaccine_name = vacc
                cov.covid_test_result = request.POST.get("covid_test_result")
                cov.save()
                messages.success(request, "Application was successful")
                return redirect("apollo:pathomepage")
            elif CovApply.objects.filter(patient_id=request.POST.get('patient_id')).count() == 1:
                isapplied = True
                message = "User has already applied"
                return render(request, 'apollo/covidcare.html',context = {'message': message, 'isapplied':isapplied})
        else:
            messages.error(request, "Invalid creds")
            return render(request=request, template_name="apollo/covidcare.html", context = {'form':form})
    else:
        form = CovidCare
    return render(request=request, template_name="apollo/covidcare.html", context = {'form':form})

def pathomepage(request):
    return render(request, 'apollo/pathomepage.html')

def emphomepage(request):
    return render(request, 'apollo/emphomepage.html')

def leavepage(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid() and Employee.objects.filter(emp_id=request.POST.get('emp_id')).exists():
            leave = Leave()
            leave.emp_id = Employee.objects.get(emp_id=request.POST.get('emp_id'))
            leave.start_date = request.POST.get('start_date')
            leave.end_date = request.POST.get('end_date')
            leave.reason_for_leave = request.POST.get('reason_for_leave')
            leave.save()
            return render(request, 'apollo/leavepage.html', context = {'form':form, 'approved':'True', 'message':'Your leave request has been submitted'})
        else:
            return render(request, 'apollo/leavepage.html', context = {'form':form, 'not_approved':'True','message':'Please enter valid details.'})
    else:
        form = LeaveForm
    return render(request, 'apollo/leavepage.html', context = {'form':form})

def contactus(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email_id')
            content = request.POST.get('content')
            send_mail("Mail from Hospital", content, email, ['jayanand.jayan2020@vitstudent.ac.in'])
            message = "Your mail has been sent! We will try to get in touch with you as soon as possible."
            sent = True
            return render(request, 'apollo/contactus.html', context = {'form':form, 'message':message, 'sent':sent})
        else:
            notsent = True
            message = "Looks like there was an error in filling the form. Please retry."
            return render(request, 'apollo/contactus.html', context = {'form':form, 'message':message, 'notsent':notsent})
    else:
        form = ContactForm
        return render(request, 'apollo/contactus.html', context = {'form':form})

def payverifiy(request):
    if request.method == "POST":
        form = Empfinform(request.POST)
        if form.is_valid():
            if PatFinance.objects.filter(payment_id=request.POST.get('payment_id')).count() == 1:
                inst = PatFinance.objects.values('is_paid').filter(payment_id__exact = request.POST.get('payment_id'))
                if inst[0]['is_paid'] == True:
                    message = "The payment has already been accepted"
                    ispaid = True
                    return render(request, 'apollo/payverify.html',{'form':form,'ispaid':ispaid, 'message':message})
                else:
                    isnotpaid=True
                    inst.update(is_paid =True)
                    pat_id = PatFinance.objects.values('patient_id').filter(payment_id__exact = request.POST.get('payment_id'))
                    cost = PatFinance.objects.values('amount_paid').filter(payment_id__exact = request.POST.get('payment_id'))
                    pay_method=PatFinance.objects.values('payment_method').filter(payment_id__exact = request.POST.get('payment_id'))
                    return render(request, 'apollo/payverify.html', context = {'form':form,'pat_id':pat_id[0]['patient_id'],'cost':cost[0]['amount_paid'],'pay_method':pay_method[0]['payment_method'],'isnotpaid':isnotpaid})
            else:
                message = "The payment ID does not exist."
                isnotverified = True
                return render(request, 'apollo/payverify.html',{'form':form,'isnotverified':isnotverified,'message':message})
        else:
            messages.error(request, "Something went wrong. Please try again")
    else:
        form = Empfinform
    return render(request, 'apollo/payverify.html', context = {'form':form})

def aboutus(request):
    return render(request,'apollo/aboutus.html')
