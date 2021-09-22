from django.urls import path
from . import views

app_name = 'log'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
