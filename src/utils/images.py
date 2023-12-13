import os
import base64
import io
import requests
from PIL import Image


def process_image(image_string, output_dir, image_index):
    image_name = f"image_{image_index}.jpg"
    image_data = None

    if 'http://' in image_string or 'https://' in image_string:
        try:
            response = requests.get(image_string)
            response.raise_for_status()
            image_data = response.content
        except requests.RequestException as e:
            print(f"Error downloading {image_string}: {e}")
            return None

    elif 'data:image' in image_string:
        try:
            base64_data = image_string.split(',')[1]
            image_data = base64.b64decode(base64_data)
        except base64.binascii.Error as e:
            print(f"Error decoding base64 image: {e}")
            return None

    if image_data:
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')
            image_path = os.path.join(output_dir, image_name)
            image.save(image_path)
            print(f"Saved image to {image_path}")
            return image_path
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
