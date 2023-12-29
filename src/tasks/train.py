import subprocess
import os
import shlex
import uuid

from utils.folders import inspect_path, delete_training_folder
from utils.images import process_image
from utils.webhooks import send_webhook_notification
from utils.shell import make_command_from_json
from utils.io import make_success_payload, make_error_payload, unpack_json, delete_checkpoint, load_config

SCRIPT_PATH = '/workspace/kohya_ss/sdxl_train.py'
TRAIN_DATA_DIR_BASE = '/workspace/witit-custom/active_training'
PRETRAINED_MODEL_PATH = "/workspace/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"
LOGGING_DIR = "/workspace/logs/"
CONFIG_PATH = "/workspace/config/kohya_ss.json"


def make_train_command(username,  resolution="512,512", model_path=PRETRAINED_MODEL_PATH, epochs=3, save_every_n_epochs=3, batch_size=1, learning_rate=0.0001):
    output_name = f"{str(uuid.uuid4())}-{username}"

    config = {
        "script": SCRIPT_PATH,
        **load_config(CONFIG_PATH),
        "pretrained_model_name_or_path": model_path,
        "train_data_dir": os.path.join(TRAIN_DATA_DIR_BASE, username, "img"),
        "resolution": resolution,
        "output_name": output_name,
        "max_train_epochs": epochs,
        "save_every_n_epochs": save_every_n_epochs,
        "train_batch_size": batch_size,
        "learning_rate": learning_rate
    }

    command = make_command_from_json(config)

    output_file = f'{config["output_dir"]}/{output_name}.safetensors'
    final_command = f"accelerate launch {command}"
    return final_command, output_file


def prepare_folder(username, images, token_name, class_name, repeats=40):
    user_folder = os.path.join(TRAIN_DATA_DIR_BASE, username)
    images_folder = os.path.join(user_folder, "img")
    training_folder = os.path.join(
        images_folder, f"{repeats}_{token_name}_{class_name}")

    os.makedirs(training_folder, exist_ok=True)

    for i, image_string in enumerate(images):
        process_image(image_string, training_folder, i + 1)

    return user_folder, images_folder, training_folder


def run_training(input_json):
    username, images, resolution, token_name, class_name, model_path, job_id, save_every_n_epochs, epochs, batch_size, learning_rate = unpack_json(
        input_json)

    user_folder, images_folder, training_folder = prepare_folder(
        username, images, token_name, class_name)

    training_command, output_file = make_train_command(
        username,  resolution, model_path, epochs, save_every_n_epochs, batch_size, learning_rate)

    print(f"""
            username: {username}
            resolution: {resolution}
            token_name: {token_name}
            class_name: {class_name}
            model_path: {model_path}
            output_file: {output_file} 
            user_folder: {user_folder}
            images_folder: {images_folder}
            training_folder: {training_folder}
            training_command: {training_command}
    """)

    try:
        os.makedirs(LOGGING_DIR, exist_ok=True)

        # training_command_list = shlex.split(training_command)

        with open(f'{LOGGING_DIR}/kohya_ss.log', 'w') as log_file:
            subprocess.run(training_command, shell=True,
                           stdout=log_file, stderr=subprocess.STDOUT, check=True)

        delete_training_folder(user_folder)
        result = make_success_payload(
            username, token_name, class_name, output_file, job_id)
        print(f"Training finished: {output_file}")

    except Exception as e:
        delete_training_folder(user_folder)
        result = make_error_payload(e, job_id)

    if 'webhook' in input_json:
        send_webhook_notification(input_json['webhook'], result)

    return result


def training_handler(data):
    inspect = data.get('inspect_path')
    if inspect:
        return inspect_path(inspect)

    checkpoint_to_delete = data.get('checkpoint_to_delete')
    if checkpoint_to_delete:
        return delete_checkpoint(checkpoint_to_delete)

    return run_training(data)
