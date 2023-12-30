
def format_arg(value):
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def make_command_from_json(json_data):
    print("json_data", json_data)
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
