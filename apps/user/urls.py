from django.urls import path
from . import views
urlpatterns=[
    path('login/', views.login),
    path('reg/',views.register),
    path('login_pwd/',views.login_pwd),

]