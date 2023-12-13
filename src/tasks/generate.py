import os
import requests
import subprocess
from requests.adapters import HTTPAdapter, Retry
from utils.size import size_config
from utils.webhooks import send_webhook_notification


LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


def hotswap_resolution(json):
    if 'witit_size' not in json:
        return json
    if 'witit_ar' not in json:
        return json

    size = json['witit_size']
    ar = json['witit_ar']
    print(f"Setting resolution to {size} {ar}")

    if size not in size_config:
        raise Exception(f"Invalid size: {size}")
    if ar not in size_config[size]:
        raise Exception(f"Invalid aspect ratio: {ar}")

    resolution = size_config[size][ar]
    json['height'] = resolution['height']
    json['width'] = resolution['width']
    return json


def softlink_checkpoint(checkpoint_path):
    softlink_path = "/workspace/stable-diffusion-webui/models/Stable-diffusion/user.safetensors"

    if os.path.islink(softlink_path):
        os.unlink(softlink_path)
        print("Existing softlink removed")

    subprocess.run(["ln", "-s", checkpoint_path, softlink_path])
    print("Softlinked user checkpoint")


def refresh_checkpoints():
    try:
        response = automatic_session.post(
            f'{LOCAL_URL}/sdapi/v1/refresh-checkpoints')
        response.raise_for_status()

        checkpoints = automatic_session.get(
            f'{LOCAL_URL}/sdapi/v1/sd-models').json()
        print("Checkpoints: ", checkpoints)
    except Exception as err:
        print("Error: ", err)
        return None


def generate_handler(json_data):
    result = {}

    print("Generating...")
    api_name = json_data["api_name"]
    checkpoint_path = json_data.get(
        "override_settings").get("sd_model_checkpoint")

    softlink_checkpoint(checkpoint_path)
    chkpt = refresh_checkpoints()

    if chkpt:
        print("Checkpoint: ", chkpt)
        json_data['override_settings']['sd_model_checkpoint'] = chkpt['title']

    try:
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        json_data = hotswap_resolution(json_data)
        response = automatic_session.post(url, json=json_data, timeout=600)
        result = response.json()
    except Exception as err:
        print("Error: ", err)
        result = {"error": str(err), "json": json_data}

    if chkpt:
        os.remove(chkpt['path'])

    if 'webhook' in json_data:
        send_webhook_notification(json_data['webhook'], {
                                  "json": json_data, "result": result})

    return result
