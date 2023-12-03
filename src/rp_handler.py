from tasks.generate import generate, wait_for_service
from tasks.train import run_training

import requests
import runpod

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()


def handler(event):
    print(event)
    method = event.get("method", "").upper()
    if method == "GET":
        endpoint = event.get("endpoint", "")
        if not endpoint:
            return {"error": "No endpoint specified for GET request."}

        uri = f'{LOCAL_URL}/{endpoint}'
        try:
            response = automatic_session.get(uri, timeout=600)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    data = event.get('input', {})
    api_name = data.get('api_name', '')
    if not api_name:
        return {"error": "No API name specified in the request data."}

    print(f"Received API call: {api_name}")

    if api_name == 'dreambooth':
        return run_training(data)

    return generate(data)


if __name__ == "__main__":
    # wait_for_service()

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True})
