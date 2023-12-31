import os
from utils.webhooks import send_webhook_notification
from .session import automatic_session, LOCAL_URL
from .checkpoints import handle_checkpoint, refresh_vae
from .payloads import build_adetailer_payload, hotswap_resolution
import json


def tidy_json(json):

    to_delete = []
    for key in json:
        if key.startswith("witit_"):
            to_delete.append(key)

    for key in to_delete:
        del json[key]


def generate_handler(json_data):
    result = {}

    print("Generating...")
    api_name = json_data["api_name"]
    json_data, softlink_path = handle_checkpoint(json_data)
    refresh_vae()

    try:
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        build_adetailer_payload(json_data)
        hotswap_resolution(json_data)
        tidy_json(json_data)

        print("url", url)
        print(json.dumps(json_data, indent=4))

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
