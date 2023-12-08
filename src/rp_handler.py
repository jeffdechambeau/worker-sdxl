from tasks.generate import generate, wait_for_service
from tasks.train import run_training

import requests
import runpod

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()


def handle_get_request(endpoint):
    if not endpoint:
        return {"error": "No endpoint specified for GET request."}

    uri = f'{LOCAL_URL}/{endpoint}'
    try:
        response = automatic_session.get(uri, timeout=600)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def validate_data(data):
    if not isinstance(data, dict):
        return False, {"error": "Input data is not a valid dictionary."}

    if 'api_name' not in data or 'username' not in data:
        return False, {"error": "Missing required fields in the data."}

    return True, None


def handle_post_request(data):
    is_valid, error_response = validate_data(data)
    if not is_valid:
        return error_response

    api_name = data['api_name']
    username = data['username']

    print(f"{username} requested {api_name}")

    if api_name == 'dreambooth':
        result = run_training(data)
    elif api_name in ['txt2img', 'img2img']:
        result = generate(data)
    else:
        return {"error": f"Unknown API name: {api_name}"}

    if not isinstance(result, dict):
        return {"error": "The API function did not return a valid dictionary."}

    return result


def handler(event):
    method = event.get("method", "").upper()

    if method == "GET":
        return handle_get_request(event.get("endpoint", ""))

    return handle_post_request(event.get('input', {}))


if __name__ == "__main__":
    wait_for_service()

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True})
