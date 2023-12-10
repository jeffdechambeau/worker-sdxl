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


def make_caption_command(directory):
    command = f"python3 finetune/make_captions_by_git.py --batch_size='1' --max_data_loader_n_workers='2' --max_length='75' --caption_extension='.txt' '{directory}'"
    return command
