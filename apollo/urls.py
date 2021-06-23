from django.urls import path
from . import views

app_name = 'apollo'
urlpatterns = [
                path('', views.homepage, name = 'homepage'),
                path('emploginpage', views.emploginpage, name = 'emploginpage'),
                path('patregister', views.patregisterpage, name = 'patregisterpage'),
                path('patlogin', views.patloginpage, name = 'patloginpage'),
                path('payment', views.paymentpage, name = 'paymentpage'),
                path('covidcare', views.covidcare, name = 'covidcare'),
                path('pathomepage',views.pathomepage, name = 'pathomepage'),
                path('leavepage', views.leavepage, name = 'leavepage'),
                path('emphomepage', views.emphomepage, name = 'emphomepage'),
                path('contactus', views.contactus, name = 'contactpage'),
                path('payverifiy',views.payverifiy, name ='payverifiy'),
                path('aboutus',views.aboutus,name = 'aboutus'),
]
