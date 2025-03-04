from django.urls import path, include
from landing.views import *

urlpatterns = [
    path('', home, name='home'),
    path('enroll', enroll, name='enroll'),
]
