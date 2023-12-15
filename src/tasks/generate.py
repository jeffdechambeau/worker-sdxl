import uuid
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
    unique_id = str(uuid.uuid4())
    softlink_path = f"/workspace/stable-diffusion-webui/models/Stable-diffusion/{unique_id}.safetensors"

    if os.path.exists(softlink_path):
        os.remove(softlink_path)
        print("Existing softlink with UUID removed")

    subprocess.run(["ln", "-s", checkpoint_path, softlink_path])
    print(f"Softlinked user checkpoint to {softlink_path}")

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


def handle_checkpoint(json_data):
    checkpoint_path = json_data.get(
        "override_settings").get("sd_model_checkpoint")
    if not checkpoint_path:
        return json_data

    softlink_path = softlink_checkpoint(checkpoint_path)
    checkpoints = refresh_checkpoints()
    print(checkpoints)
    [match] = [c for c in checkpoints if c['filename'] == softlink_path] or [None]

    if not match:
        raise Exception("Checkpoint not found")

    print("Checkpoint: ", match)
    json_data['override_settings']['sd_model_checkpoint'] = softlink_path
    return json_data, softlink_path


def generate_handler(json_data):
    result = {}

    print("Generating...")
    api_name = json_data["api_name"]
    json_data, softlink_path = handle_checkpoint(json_data)

    try:
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        json_data = hotswap_resolution(json_data)
        response = automatic_session.post(url, json=json_data, timeout=600)
        result = response.json()
    except Exception as err:
        print("Error: ", err)
        result = {"error": str(err), "json": json_data}

    if softlink_path and os.path.exists(softlink_path):
        os.remove(softlink_path)

    if 'webhook' in json_data:
        send_webhook_notification(json_data['webhook'], {
                                  "json": json_data, "result": result})

    return result
