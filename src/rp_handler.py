
from tasks.generate import generate, wait_for_service
from tasks.train import run_training

import requests
import runpod

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()


def handler(event):
    if event["method"].upper() == "GET":
        endpoint = event.get("endpoint", "")
        uri = f'{LOCAL_URL}/{endpoint}'
        response = automatic_session.get(uri, timeout=600)
        return response.json()

    data = event.get('input', {})
    api_name = data['api_name']

    print(f"Received API call: {api_name}")

    if api_name == 'dreambooth':
        return run_training(data)

    return generate(data)


if __name__ == "__main__":
    # wait_for_service()

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True})
