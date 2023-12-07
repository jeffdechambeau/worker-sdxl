import time
import requests
from requests.adapters import HTTPAdapter, Retry

LOCAL_URL = "http://127.0.0.1:3000"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


def generate(data):
    api_name = data["api_name"]
    response = automatic_session.post(
        f'{LOCAL_URL}/{api_name}', json=data.get("input", {}), timeout=600)
    result = response.json()
    print("Generating...")
    print("data:", data)
    print("result:", result)
    return result


def wait_for_service(url=f'{LOCAL_URL}/sdapi/v1/txt2img'):
    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(2)
