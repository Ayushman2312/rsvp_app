from django.urls import path
from .views import HomeView, save_phone
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/save-phone/', save_phone, name='save_phone'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
