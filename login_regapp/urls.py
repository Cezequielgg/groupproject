from django.urls import path
from . import views

urlpatterns = [
    path('',views.regandlogin),
    path('registration',views.registration),     
    path('login',views.login),
    path('logout',views.logout), 
    path('pass',views.inpage),
    path('newtrip',views.newtrip),
    path('delete/<int:id>',views.delete)
]