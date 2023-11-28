import time
import runpod
import requests
from requests.adapters import HTTPAdapter, Retry

LOCAL_URL = "http://127.0.0.1:3000"

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


def run_inference(event):
    if event["method"].upper() == "GET":
        endpoint = event.get("endpoint", "")
        response = automatic_session.get(
            f'{LOCAL_URL}/{endpoint}', timeout=600)
    else:  # Default to POST
        api_name = event.get("api_name", "sdapi/txt2img")
        response = automatic_session.post(
            f'{LOCAL_URL}/{api_name}', json=event.get("input", {}), timeout=600)
    return response.json()


def handler(event):
    json = run_inference(event)
    return json


if __name__ == "__main__":
    wait_for_service(url=f'{LOCAL_URL}/txt2img')

    print("WebUI API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler,
                             "return_aggregate_stream": True})
