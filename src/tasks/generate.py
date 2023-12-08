import os
import time
import requests
from requests.adapters import HTTPAdapter, Retry
from utils.size import size_config
from pprint import pprint

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


is_training_pod_only = os.environ.get(
    'IS_TRAINING_POD_ONLY', 'False').lower() == 'true'


def hotswap_resolution(json):
    if 'witit_size' and 'witit_ar' not in json:
        return json

    size = json['witit_size']
    ar = json['witit_ar']

    if size not in size_config:
        raise Exception(f"Invalid size: {size}")
    if ar not in size_config[size]:
        raise Exception(f"Invalid aspect ratio: {ar}")

    resolution = size_config[size][ar]
    json['height'] = resolution['height']
    json['width'] = resolution['width']
    return json


def generate(json):
    try:
        print("Generating...")
        pprint(json)
        api_name = json["api_name"]
        url = f'{LOCAL_URL}/sdapi/v1/{api_name}'
        response = automatic_session.post(url, json=json, timeout=600)
        print(response)
        result = response.json()
        print("Generated.", result)
        return result
    except Exception as err:
        print("Error: ", err)
        return {"error": str(err)}


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
