import time

import runpod
import requests
from requests.adapters import HTTPAdapter, Retry

LOCAL_URL = "http://127.0.0.1:7860/sdapi/v1"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


def wait_for_service(url):
    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(0.2)


def run_inference(inference_request):
    print("Got request", inference_request)
    api_name = inference_request['api_name'] or 'txt2img'
    response = automatic_session.post(url=f'{LOCAL_URL}/{api_name}',
                                      json=inference_request, timeout=600)
    return response.json()


def handler(event):

    json = run_inference(event["input"])
    return json


if __name__ == "__main__":
    wait_for_service(url=f'{LOCAL_URL}/txt2img')

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True
                             })
