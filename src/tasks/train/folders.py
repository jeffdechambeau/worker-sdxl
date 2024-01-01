import shutil
import os
import base64
import io
import requests
from PIL import Image

from utils.constants import TRAIN_DATA_DIR_BASE


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


def inspect_path(path):
    if not os.path.exists(path):
        print("The path does not exist.")
        return None

    if os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"File Size: {size} bytes")

        if path.endswith('.log'):
            with open(path, 'r') as file:
                contents = file.read()
                return {"size": size, "contents": contents}
        else:
            return {"size": size}

    elif os.path.isdir(path):
        contents = os.listdir(path)
        print("Directory contents:")
        for item in contents:
            print(item)
        return {"contents": contents}
    else:
        print("It is neither a file nor a directory.")
        return {"nothing": True}


def delete_training_folder(folder_path):
    if 'workspace/witit' not in folder_path:
        print(f"Invalid path: {folder_path}")
        return
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Successfully deleted the folder: {folder_path}")
        except Exception as e:
            print(f"Failed to delete the folder: {folder_path}. Reason: {e}")
    else:
        print(
            f"The specified path does not exist or is not a directory: {folder_path}")


def prepare_folder(username=None, images=None, token_name="ohwx", class_name="person", repeats=40):
    user_folder = os.path.join(TRAIN_DATA_DIR_BASE, username)
    images_folder = os.path.join(user_folder, "img")
    training_folder = os.path.join(
        images_folder, f"{repeats}_{token_name}_{class_name}")

    os.makedirs(training_folder, exist_ok=True)

    for i, image_string in enumerate(images):
        process_image(image_string, training_folder, i + 1)

    return user_folder
