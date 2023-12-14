import subprocess
import os

from utils.folders import inspect_path, delete_training_folder
from utils.images import process_image
from utils.webhooks import send_webhook_notification
from utils.shell import make_command_from_json

script_path = '/workspace/kohya_ss/sdxl_train.py'
train_data_dir_base = '/workspace/witit-custom/active_training'
pretrained_model_path = "/workspace/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"
checkpoint_output_path = "/workspace/witit-custom/checkpoints"
logging_dir = "/workspace/logs/"


def make_train_command(username="undefined", resolution="512,512", train_data_dir="/workspace/witit-custom/active_training", model_path=pretrained_model_path):
    output_dir = f'/workspace/witit-custom/checkpoints/'
    print(f"Output dir: {output_dir}")

    config = {
        "num_cpu_threads_per_process": 4,
        "script": script_path,
        "pretrained_model_name_or_path": model_path,
        "train_data_dir": train_data_dir,
        "resolution": resolution,
        "output_dir": output_dir,
        "output_name": username,
        "enable_bucket": True,
        "min_bucket_reso": 256,
        "max_bucket_reso": 1024,
        "logging_dir": "/workspace/logs/",
        "save_model_as": "safetensors",
        "lr_scheduler_num_cycles": 1,
        "max_token_length": 150,
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
        "max_grad_norm": 0.0
    }

    command = make_command_from_json(config)

    print(f"""Created training command:
          
          {command}

          """)

    return f"accelerate launch {command}"


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

    username = input_json['username']
    images = input_json['images']
    resolution = input_json['training_resolution']
    token_name = input_json['token']
    class_name = input_json['class']
    model_path = input_json['model_path']

    images_folder = os.path.join(train_data_dir_base, username, "img")
    training_command = make_train_command(
        username, resolution, images_folder, model_path)
    output_file = f'{checkpoint_output_path}/{username}.safetensors'
    user_folder, images_folder, training_folder = prepare_folder(
        username, images, token_name, class_name)

    print(f"User folder: {user_folder}")
    print(f"Images folder: {images_folder}")
    print(f"Training folder: {training_folder}")
    print(f"Full training command: {training_command}")

    try:
        os.makedirs(logging_dir, exist_ok=True)

        # Using 'tee' to duplicate the output to both log file and container shell
        subprocess.run(
            f"bash -c '{training_command} | tee /workspace/logs/kohya_ss.log 2>&1'", shell=True, check=True)

        print(f"Training finished: {output_file}")
        delete_training_folder(user_folder)

        result = {
            "status": "success",
            "custom_checkpoint_path": output_file,
            "username": username,
            "token": token_name,
            "class": class_name,
            "cleanup_complete": True
        }

    except Exception as e:
        delete_training_folder(user_folder)
        result = {
            "status": "error",
            "error": str(e),
            "cleanup_complete": True
        }
        print(f"Error running training: {e}")

    if 'webhook' in input_json:
        send_webhook_notification(input_json['webhook'], result)

    return result


def delete_checkpoint(delete_path):
    if "witit-custom/checkpoints" not in delete_path:
        return {
            "status": "error",
            "error": "Invalid delete path"
        }
    try:
        os.remove(delete_path)
        return {
            "status": "success",
            "deleted_path": delete_path
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def training_handler(data):
    inspect = data.get('inspect_path')
    checkpoint_to_delete = data.get('checkpoint_to_delete')

    if inspect:
        return inspect_path(inspect)

    if checkpoint_to_delete:
        return delete_checkpoint(checkpoint_to_delete)

    return run_training(data)
