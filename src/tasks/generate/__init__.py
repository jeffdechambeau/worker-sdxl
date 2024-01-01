import os
import json

from utils.constants import LOCAL_URL
from utils.webhooks import send_webhook_notification

from .session import automatic_session
from .checkpoints import handle_checkpoint, refresh_vae
from .payload.stablediffusion import assemble_payload


def generate_handler(json_data):
    result = {}

    print("Generating...")
    api_name = json_data["api_name"]
    json_data, softlink_path = handle_checkpoint(json_data)
    refresh_vae()

    try:
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        json_data = assemble_payload(json_data)
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
