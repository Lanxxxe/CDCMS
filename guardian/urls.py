from django.urls import path
from guardian.views import *

urlpatterns = [
    path('', dashboard, name='guardian_dashboard'),
    path('announcement', announcement, name='guardian_announcement'),
]
