
import os
import subprocess

from .session import automatic_session
from utils.constants import LOCAL_URL
from utils.config import load_config


def softlink_checkpoint(checkpoint_path):
    filename = os.path.basename(checkpoint_path)
    softlink_path = f"/workspace/stable-diffusion-webui/models/Stable-diffusion/{filename}"

    if os.path.exists(softlink_path):
        return softlink_path
    try:
        subprocess.run(["ln", "-s", checkpoint_path, softlink_path])
        print(f"Softlinked user checkpoint to {softlink_path}")
        return softlink_path
    except Exception as err:
        print("Error: ", err)


def softlink_model_from_name(model_name):
    full_path = f"/workspace/witit-custom/checkpoints/{model_name}.safetensors"
    if not os.path.exists(full_path):
        print(f"Checkpoint {model_name} not found")
        raise Exception(f"Checkpoint {model_name} not found")
    softlink_path = softlink_checkpoint(full_path)
    return softlink_path


def refresh_checkpoints():
    try:
        response = automatic_session.post(
            f'{LOCAL_URL}/sdapi/v1/refresh-checkpoints')
        response.raise_for_status()

        checkpoints = automatic_session.get(
            f'{LOCAL_URL}/sdapi/v1/sd-models').json()
        return checkpoints

    except Exception as err:
        print("Error: ", err)
        return None


def refresh_vae():
    try:
        response = automatic_session.post(
            f'{LOCAL_URL}/sdapi/v1/refresh-vae')
        response.raise_for_status()

    except Exception as err:
        print("Error: ", err)
        return None


def handle_override_settings(json_data):
    default_config = load_config("/workspace/config/webui.json")
    override_settings = default_config.get("override_settings")

    if 'override_settings' not in json_data:
        return {**json_data, "override_settings": override_settings}
    else:
        for key, value in override_settings.items():
            if key not in json_data.get("override_settings"):
                json_data["override_settings"][key] = value
        return json_data


def find_model(model_name):
    checkpoints = refresh_checkpoints()
    match = None
    for c in checkpoints:
        if c['model_name'] == model_name:
            match = c
            print("Found matching checkpoint:", match)
            break
    return match


def load_and_tidy_model_name(json_data):
    model_name = json_data.get("override_settings").get("sd_model_checkpoint")
    return model_name.replace(".safetensors", "")


def handle_checkpoint(json_data):
    json_data = handle_override_settings(json_data)
    model_name = load_and_tidy_model_name(json_data)
    match = find_model(model_name)

    if match:
        return json_data, None

    print("No matching checkpoint found, softlinking user checkpoint")
    softlink_path = softlink_model_from_name(model_name)
    match = find_model(model_name)

    if match:
        return json_data, softlink_path
    else:
        print(f"Checkpoint {model_name} not found")
        os.remove(softlink_path)
        raise Exception(f"Checkpoint {model_name} not found")
