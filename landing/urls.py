from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from landing.views import *

urlpatterns = [
    path('', home, name='home'),
    path('enroll', enroll, name='enroll'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)