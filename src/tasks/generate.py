import os
import time
import requests
from requests.adapters import HTTPAdapter, Retry
from utils.size import size_config

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


is_training_pod_only = os.environ.get(
    'IS_TRAINING_POD_ONLY', 'False').lower() == 'true'


def generate(json):
    print("Generating...")
    api_name = json["api_name"]
    url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
    if 'witit_size' and 'witit_ar' in json:

        size = json['witit_size']
        ar = json['witit_ar']

        if size not in size_config:
            raise Exception(f"Invalid size: {size}")
        if ar not in size_config[size]:
            raise Exception(f"Invalid aspect ratio: {ar}")

        resolution = size_config[size][ar]
        json['height'] = resolution['height']
        json['width'] = resolution['width']

    response = automatic_session.post(url, json, timeout=600)
    result = response.json()
    print("Generated.")
    return result


def wait_for_service(url=f'{LOCAL_URL}/sdapi/v1/options'):

    if is_training_pod_only:
        return
    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(5)
