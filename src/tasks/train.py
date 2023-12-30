import subprocess
import os
import shlex
import uuid

from utils.folders import inspect_path, delete_training_folder
from utils.images import process_image
from utils.webhooks import send_webhook_notification
from utils.shell import make_command_from_json
from utils.io import make_success_payload, make_error_payload, delete_checkpoint, load_config

SCRIPT_PATH = os.environ.get(
    'SCRIPT_PATH', '/workspace/kohya_ss/sdxl_train.py')
TRAIN_DATA_DIR_BASE = os.environ.get(
    'TRAIN_DATA_DIR_BASE', '/workspace/witit-custom/active_training')
PRETRAINED_MODEL_PATH = os.environ.get(
    'PRETRAINED_MODEL_PATH', '/workspace/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors')
LOGGING_DIR = os.environ.get('LOGGING_DIR', '/workspace/logs/')
CONFIG_PATH = os.environ.get('CONFIG_PATH', '/workspace/config/kohya_ss.json')
MAX_CPU_THREADS = os.environ.get('MAX_CPU_THREADS', 4)


def make_train_command(json):
    output_name = f"{str(uuid.uuid4())}-{json['username']}"
    train_data_dir = os.path.join(TRAIN_DATA_DIR_BASE, json['username'], "img")

    del json['username']
    del json['images']
    del json['job_id']
    del json['webhook']
    del json['api_name']

    config = {
        "num_cpu_threads_per_process": MAX_CPU_THREADS,
        "script": SCRIPT_PATH,
        "train_data_dir": train_data_dir,
        **load_config(CONFIG_PATH),
        **json
    }

    command = make_command_from_json(config)

    output_file = f'{config["output_dir"]}/{output_name}.safetensors'
    final_command = f"accelerate launch {command}"
    return final_command, output_file


def prepare_folder(username=None, images=None, token_name="ohwx", class_name="person", repeats=40):
    user_folder = os.path.join(TRAIN_DATA_DIR_BASE, username)
    images_folder = os.path.join(user_folder, "img")
    training_folder = os.path.join(
        images_folder, f"{repeats}_{token_name}_{class_name}")

    os.makedirs(training_folder, exist_ok=True)

    for i, image_string in enumerate(images):
        process_image(image_string, training_folder, i + 1)

    return user_folder, images_folder, training_folder


def run_training(json):
    job_id = json.get('job_id')
    webhook = json.get('webhook')

    user_folder, images_folder, training_folder = prepare_folder(
        username=json['username'], images=json['images'], token_name=json['token'], class_name=json['class'])

    training_command, output_file = make_train_command(json)

    print(f"""
            username: {json['username']}
            resolution: {json['resolution']}
            token_name: {json['token_name']}
            class_name: {json['class_name']}
            model_path: {json['model_path']}
            output_file: {output_file} 
            user_folder: {user_folder}
            images_folder: {images_folder}
            training_folder: {training_folder}
            training_command: {training_command}
    """)

    try:
        os.makedirs(LOGGING_DIR, exist_ok=True)
        with open(f'{LOGGING_DIR}/kohya_ss.log', 'w') as log_file:
            subprocess.run(training_command, shell=True,
                           stdout=log_file, stderr=subprocess.STDOUT, check=True)

        delete_training_folder(user_folder)

        result = make_success_payload(
            json['username'], json['token'], json['class'], output_file, job_id)

        print(f"Training finished: {output_file}")

    except Exception as e:
        delete_training_folder(user_folder)
        result = make_error_payload(e, job_id)

    if webhook:
        send_webhook_notification(webhook, result)

    return result


def training_handler(data):
    inspect = data.get('inspect_path')
    if inspect:
        return inspect_path(inspect)

    checkpoint_to_delete = data.get('checkpoint_to_delete')
    if checkpoint_to_delete:
        return delete_checkpoint(checkpoint_to_delete)

    return run_training(data)
