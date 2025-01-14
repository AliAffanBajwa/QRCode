from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .utils import generate_and_save_qr_code
import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

class QRCodeView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', '')
        if not data:
            return Response(
                {"error": "No data provided for QR code generation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        qr_result = generate_and_save_qr_code(data)

        current_site = get_current_site(request)
        full_url = f"http://{current_site.domain}{qr_result['file_url']}"

        return Response({
            "message": "QR Code generated successfully.",
            "file_url": full_url  # Full URL including the domain
        }, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        filename = request.GET.get('filename', '')
        if not filename:
            return Response(
                {"error": "No filename provided to retrieve the QR code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', filename)
        if not os.path.exists(file_path):
            return Response(
                {"error": "The specified QR code does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
