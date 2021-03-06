from django.urls import path
from . import views

urlpatterns = [
    path('',views.regandlogin),
    path('registration',views.registration),     
    path('login',views.login),
    path('logout',views.logout), 
    path('pass',views.inpage),
    path('create_property', views.create_property),
    path('property_all', views.all_properties),
    path('property/<int:property_id>', views.property_detail),
    path('property/delete/<int:property_id>', views.delete_property),
    path('property/page/<int:property_id>', views.update_property),
    path('property/page/edit/<int:property_id>', views.edit_property),
    path('property/like/<int:property_id>', views.like_property),
    path('property/unlike/<int:property_id>', views.unlike_property),
    path('liked_properties', views.liked_properties),
]