import requests
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


def generate(json_data):
    result = {}

    try:
        print("Generating...")
        api_name = json_data["api_name"]
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        json_data = hotswap_resolution(json_data)
        response = automatic_session.post(url, json=json_data, timeout=600)
        result = response.json()

    except Exception as err:
        print("Error: ", err)
        result = {"error": str(err), "json": json_data}

    if 'webhook' in json_data:
        send_webhook_notification(json_data['webhook'], {
                                  "json": json_data, "result": result})

    return result
