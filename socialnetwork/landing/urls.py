from django.urls import path 
from landing.views import Index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

