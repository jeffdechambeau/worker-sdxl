
script_path = '/kohya_ss/sdxl_train.py'
pretrained_model_path = "/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"


def format_arg(value):
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def make_command_from_json_alt(json_data):
    command = []
    for key, value in json_data.items():
        if key == "script":
            command.append(f'"{value}"')
        elif isinstance(value, bool):
            if value:
                command.append(f"--{key}")
        elif isinstance(value, (int, float, str)) and value:
            command.append(f"--{key} {format_arg(value)}")
        elif isinstance(value, dict):
            nested_args = ' '.join(
                f"{nested_key}={format_arg(nested_value)}" for nested_key, nested_value in value.items())
            command.append(f"--{key} {nested_args}")

    return ' '.join(command)


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
    return f' {" ".join(command)}'


def make_train_command(username="undefined", resolution="512,512", train_data_dir="/workspace/witit-custom/active_training", model_path=pretrained_model_path):
    output_dir = f'/workspace/witit-custom/checkpoints/{username}'
    print(f"Output dir: {output_dir}")

    config = {
        "script": script_path,
        "num_cpu_threads_per_process": 4,
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
    command2 = make_caption_command(config)
    print(f"Commands do {'' if command == command2 else 'not'} match")
    return command


def make_caption_command(directory):
    command = f"python3 finetune/make_captions_by_git.py --batch_size='1' --max_data_loader_n_workers='2' --max_length='75' --caption_extension='.txt' '{directory}'"
    return command
