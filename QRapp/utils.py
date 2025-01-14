import qrcode
import os
import shortuuid
from django.conf import settings
from io import BytesIO
import urllib.parse

def generate_and_save_qr_code(data):
    # Encode the data into a Google search URL
    search_query = urllib.parse.quote(data)  # URL encode the search query
    google_search_url = f"https://www.google.com/search?q={search_query}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(google_search_url)  # Use the Google search URL
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Generate a unique filename using shortuuid
    filename = f"{shortuuid.uuid()}.png"

    # Create the file path
    file_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    img.save(file_path)

    # Save the image in memory for returning in the response
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    return {
        "file_url": f"{settings.MEDIA_URL}qr_codes/{filename}",
        "image_data": img_io.getvalue(),  # Getting the image byte data
    }
