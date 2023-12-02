
import os
import base64
import io
import requests
from PIL import Image
pretrained_model_path = "/workspace/stable-diffusion-webui/models/Stable-diffusion/runDiffusionXL.safetensors"
train_data_dir_base = '/workspace/witit-custom/active_training'
logging_dir = "/workspace/logs/"
script_path = '/workspace/kohya_ss/sdxl_train.py'


def prepare_folder(username, images):
    for image_string in images:
        image_name = None

        if 'http://' in image_string or 'https://' in image_string:
            image_name = image_string.split('/')[-1]
            try:
                response = requests.get(image_string)
                response.raise_for_status()
                image_data = response.content
            except requests.RequestException as e:
                print(f"Error downloading {image_string}: {e}")
                continue

        elif 'data:image' in image_string:
            base64_data = image_string.split(',')[1]
            try:
                image_data = base64.b64decode(base64_data)
            except base64.binascii.Error as e:
                print(f"Error decoding base64 image: {e}")
                continue

            image_name = f"image_{len(images)}.jpg"

        if image_data:
            try:
                image = Image.open(io.BytesIO(image_data))
                image = image.convert('RGB')
                output_dir = os.path.join(train_data_dir_base, username, 'img')
                os.makedirs(output_dir, exist_ok=True)
                image_path = os.path.join(output_dir, image_name)
                image.save(image_path)
                print(f"Saved image to {image_path}")
            except Exception as e:
                print(f"Error processing image: {e}")


def make_command_from_json(json_data):
    command = []
    for key, value in json_data.items():
        if key == "script":
            command.append(f'"{value}"')
        else:
            if isinstance(value, bool):
                if value:
                    command.append(f"--{key}")
            else:
                command.append(f"--{key}")
                if value or value == 0:
                    if isinstance(value, dict):
                        nested_args = []
                        for nested_key, nested_value in value.items():
                            nested_args.append(f"{nested_key}={nested_value}")
                        command.append(f'{ " ".join(nested_args) }')
                    else:
                        if isinstance(value, str) and not value.isdigit():
                            command.append(f'"{value}"')
                        elif isinstance(value, float):
                            command.append(f'"{value}"')
                        else:

                            command.append(str(value))
    return f'accelerate launch {" ".join(command)}'


def make_train_command(username="undefined", resolution="512,512"):
    train_data_dir = f'{train_data_dir_base}/{username}/img/'
    output_dir = f'/workspace/witit-custom/checkpoints/{username}'

    config = {
        "num_cpu_threads_per_process": 4,
        "script": script_path,
        "pretrained_model_name_or_path": pretrained_model_path,
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
        "max_train_steps": 80,
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
        "bucket_reso_steps": 64,
        "shuffle_caption": True,
        "caption_extension": ".txt",
        "noise_offset": 0.0,
        "max_grad_norm": 0.0
    }

    command = make_command_from_json(config)
    print(command)
    return command


def run_training(input_json):
    print("input_json", input_json)
    username = input_json['username']
    images = input_json['images']

    # prepare_folder(username, images)
    # training_command = make_train_command(username)
    # print(training_command)
    return {"output": True}
    # "id": training_command}
