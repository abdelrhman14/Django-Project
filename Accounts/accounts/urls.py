from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('profile/<slug:slug>',views.profile,name='profile'),
    path('edit/<slug:slug>',views.profile_edit,name='editprofile'),
    path('contact/',views.contact,name='contact'),
   
]