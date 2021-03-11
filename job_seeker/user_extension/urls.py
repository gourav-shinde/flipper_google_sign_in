from django.contrib import admin
from django.urls import path,include
from .views import login_view,new_registration,Wait,verification

app_name="user_extension"

urlpatterns = [
    path("login",login_view,name="Login"),
    path('register',new_registration,name="newregister"),
    path('wait',Wait,name="wait"),
    path('activate/<uidb64>/<token>',verification,name="activate"),
]
