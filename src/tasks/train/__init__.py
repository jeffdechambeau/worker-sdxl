
import subprocess
import os
import uuid

from utils.config import load_config
from utils.webhooks import send_webhook_notification
from utils.constants import MAX_CPU_THREADS, SCRIPT_PATH, KOHYA_CONFIG_PATH, TRAIN_DATA_DIR_BASE, LOGGING_DIR, RUNPOD_ID

from .folders import inspect_path, delete_training_folder, prepare_folder
from .shell import make_command_from_json
from .io import make_success_payload, make_error_payload, delete_checkpoint


def make_train_command(input_json):
    json = input_json.copy()
    output_name = f"{str(uuid.uuid4())}-{json['username']}"
    train_data_dir = os.path.join(TRAIN_DATA_DIR_BASE, json['username'], "img")

    keys_to_remove = [
        'inspect_path',
        'checkpoint_to_delete',
        'num_cpu_threads_per_process',
        'script',
        'train_data_dir',
        'username',
        'images',
        'job_id',
        'webhook',
        'api_name',
        "token",
        "class"
    ]

    for key in keys_to_remove:
        if key in json:
            del json[key]

    config = {
        "num_cpu_threads_per_process": MAX_CPU_THREADS,
        "script": SCRIPT_PATH,
        "train_data_dir": train_data_dir,
        "output_name": output_name,
        **load_config(KOHYA_CONFIG_PATH),
        **json
    }

    command = make_command_from_json(config)
    output_file = f'{config["output_dir"]}/{output_name}.safetensors'
    final_command = f"accelerate launch {command}"

    print(f"""
            username: {input_json['username']}
            token: {input_json['token']}
            class_name: {input_json['class']}
            resolution: {config['resolution']}
            model: {config['pretrained_model_name_or_path']}
            output_file: {output_file} 
            training_folder: {train_data_dir}
            training_command: {final_command}""")

    return final_command, output_file


def run_training(json):
    job_id = json.get('job_id')
    webhook = json.get('webhook')

    user_folder = prepare_folder(
        username=json['username'], images=json['images'], token_name=json['token'], class_name=json['class'])

    training_command, output_file = make_train_command(json)

    try:
        os.makedirs(LOGGING_DIR, exist_ok=True)
        with open(f'{LOGGING_DIR}/{RUNPOD_ID}-kohya_ss.log', 'w') as log_file:
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
