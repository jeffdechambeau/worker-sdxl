
import os
import subprocess

from .session import automatic_session

from utils.constants import LOCAL_URL


def softlink_checkpoint(checkpoint_path):

    filename = os.path.basename(checkpoint_path)
    [model_name, ext] = os.path.splitext(filename)

    softlink_path = f"/workspace/stable-diffusion-webui/models/Stable-diffusion/{filename}"

    if os.path.exists(softlink_path):
        os.remove(softlink_path)
        print("Existing softlink with UUID removed")

    subprocess.run(["ln", "-s", checkpoint_path, softlink_path])
    print(f"Softlinked user checkpoint to {softlink_path}")

    return softlink_path, model_name


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


def handle_checkpoint(json_data):
    if 'override_settings' not in json_data or 'sd_model_checkpoint' not in json_data.get('override_settings'):
        return json_data, None

    checkpoint_path = json_data.get(
        "override_settings").get("sd_model_checkpoint")

    if 'witit-custom' not in checkpoint_path:
        print("Not a custom checkpoint, skipping softlink")
        return json_data, checkpoint_path

    softlink_path, model_name = softlink_checkpoint(checkpoint_path)
    checkpoints = refresh_checkpoints()

    match = None
    for c in checkpoints:
        if c['model_name'] == model_name:
            match = c
            print("Found matching checkpoint:")
            print(match)
            break

    if match is not None:
        json_data['override_settings']['sd_model_checkpoint'] = model_name
        return json_data, softlink_path
    else:
        print(f"Checkpoint {model_name} not found")
        os.remove(softlink_path)
        raise Exception(f"Checkpoint {model_name} not found")
