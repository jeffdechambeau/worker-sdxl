
from tasks.generate import generate, wait_for_service
from tasks.train import run_training
import runpod


def handler(event):
    data = event.get('input', {})
    api_name = data['api_name']
    print(f"Received API call: {api_name}")
    if api_name == 'dreambooth':
        return run_training(data)

    json = generate(event)
    return json


if __name__ == "__main__":
    # wait_for_service()

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True})
