import subprocess
import os

from utils.shell import make_train_command
from utils.folders import inspect_path, delete_training_folder
from utils.images import process_image

train_data_dir_base = '/workspace/witit-custom/active_training'
logging_dir = "/workspace/logs/"


def prepare_folder(username, images, token_name, class_name, train_data_dir_base=train_data_dir_base, repeats=40):
    user_folder = os.path.join(train_data_dir_base, username)
    images_folder = os.path.join(user_folder, "img")
    training_folder = os.path.join(
        images_folder, f"{repeats}_{token_name}_{class_name}")
    os.makedirs(training_folder, exist_ok=True)

    for i, image_string in enumerate(images):
        process_image(image_string, training_folder, i + 1)

    return user_folder, images_folder, training_folder


def run_training(input_json):
    inspect = input_json.get('inspect_path')
    if inspect:
        return inspect_path(inspect)

    username = input_json['username']
    images = input_json['images']
    resolution = input_json['training_resolution']
    token_name = input_json['token']
    class_name = input_json['class']
    model_path = input_json['model_path']
    images_folder = os.path.join(train_data_dir_base, username, "img")

    user_folder, images_folder, training_folder = prepare_folder(
        username, images, token_name, class_name)

    training_command = f"accelerate launch {make_train_command(username, resolution, images_folder, model_path)}"
    # full_command = f"""source /venv/bin/activate && {training_command} && deactivate"""

    print(f"User folder: {user_folder}")
    print(f"Images folder: {images_folder}")
    print(f"Training folder: {training_folder}")
    print(f"Full training command: {full_command}")

    try:
        os.makedirs(logging_dir, exist_ok=True)
        subprocess.run(
            f"bash -c '{training_command}' > /workspace/logs/kohya_ss.log 2>&1 ", shell=True, check=True)

        print("Training finished.")
        output_file = f'/workspace/witit-custom/checkpoints/{username}/{username}.safetensors'

        delete_training_folder(user_folder)
        return {"status": "success", "custom_checkpoint_path": output_file}

    except subprocess.CalledProcessError as e:
        delete_training_folder(user_folder)
        print(f"Error running training: {e}")
        return {"status": "error", "error": str(e)}
