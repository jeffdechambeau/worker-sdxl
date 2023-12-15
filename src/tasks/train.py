import subprocess
import os
import shlex

from utils.folders import inspect_path, delete_training_folder
from utils.images import process_image
from utils.webhooks import send_webhook_notification
from utils.shell import make_command_from_json
from utils.io import make_success_payload, make_error_payload, unpack_json, delete_checkpoint

SCRIPT_PATH = '/workspace/kohya_ss/sdxl_train.py'
TRAIN_DATA_DIR_BASE = '/workspace/witit-custom/active_training'
PRETRAINED_MODEL_PATH = "/workspace/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"
CHECKPOINT_OUTPUT_PATH = "/workspace/witit-custom/checkpoints"
LOGGING_DIR = "/workspace/logs/"


def make_train_command(username,  train_data_dir, resolution="512,512", model_path=PRETRAINED_MODEL_PATH):

    config = {
        "num_cpu_threads_per_process": 4,
        "script": SCRIPT_PATH,
        "resolution": resolution,
        "output_name": username,
        "output_dir": CHECKPOINT_OUTPUT_PATH,
        "logging_dir": LOGGING_DIR,
        "pretrained_model_name_or_path": model_path,
        "train_data_dir": train_data_dir,
        "enable_bucket": True,
        "min_bucket_reso": 256,
        "max_bucket_reso": 1024,
        "save_model_as": "safetensors",
        "lr_scheduler_num_cycles": 1,
        "max_data_loader_n_workers": 0,
        "learning_rate_te1": 0.0,
        "learning_rate_te2": 0.0,
        "learning_rate": 1e-06,
        "lr_scheduler": "constant",
        "lr_warmup_steps": 0,
        "train_batch_size": 4,
        "max_train_steps": 100,
        "save_every_n_epochs": 1,
        "mixed_precision": "bf16",
        "save_precision": "fp16",
        "cache_latents": True,
        "cache_latents_to_disk": True,
        "optimizer_type": "Adafactor",
        "optimizer_args": {
            "scale_parameter": "True",
            "relative_step": "True",
            "warmup_init": "True",
            "weight_decay": "2"
        },
        "max_token_length": 150,
        "keep_tokens": 1,
        "caption_dropout_rate": 0.1,
        "bucket_reso_steps": 32,
        "shuffle_caption": True,
        "caption_extension": ".txt",
        "noise_offset": 0.0,
        "max_grad_norm": 0.0,
    }

    command = make_command_from_json(config)

    print(f"""Created training command:
          
          {command}

          """)

    output_file = f'{CHECKPOINT_OUTPUT_PATH}/{username}.safetensors'
    final_command = f"accelerate launch {command}"
    return final_command, output_file


def prepare_folder(username, images, token_name, class_name, train_data_dir_base=TRAIN_DATA_DIR_BASE, repeats=40):
    user_folder = os.path.join(train_data_dir_base, username)
    images_folder = os.path.join(user_folder, "img")
    training_folder = os.path.join(
        images_folder, f"{repeats}_{token_name}_{class_name}")
    os.makedirs(training_folder, exist_ok=True)

    for i, image_string in enumerate(images):
        process_image(image_string, training_folder, i + 1)

    return user_folder, images_folder, training_folder


def run_training(input_json):

    username, images, resolution, token_name, class_name, model_path = unpack_json(
        input_json)

    user_folder, images_folder, training_folder = prepare_folder(
        username, images, token_name, class_name)

    training_command, output_file = make_train_command(
        username, images_folder, resolution, model_path)

    print(f"""
            username: {username}
            resolution: {resolution}
            token_name: {token_name}
            class_name: {class_name}
            model_path: {model_path}
            user_folder: {user_folder}
            images_folder: {images_folder}
            training_folder: {training_folder}
            training_command: {training_command}
    """)

    try:
        os.makedirs(LOGGING_DIR, exist_ok=True)

        training_command_list = shlex.split(training_command)
        with open(f'{LOGGING_DIR}/kohya_ss.log', 'w') as log_file:
            subprocess.run(training_command_list,
                           stdout=log_file, stderr=subprocess.STDOUT)

        delete_training_folder(user_folder)
        result = make_success_payload()
        print(f"Training finished: {output_file}")

    except Exception as e:
        delete_training_folder(user_folder)
        result = make_error_payload(e)

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
