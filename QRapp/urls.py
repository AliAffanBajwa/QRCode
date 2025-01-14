from django.urls import path
from .views import QRCodeView

urlpatterns = [
    path('generate-qr/', QRCodeView.as_view(), name='generate-qr'),
]
